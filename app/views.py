from flask import render_template, url_for, flash, redirect, request, jsonify, g, session, current_app as app
from flask_login import login_user, current_user, logout_user, login_required, fresh_login_required
from flask_socketio import emit
from datetime import datetime, timezone, timedelta
from app import db, bcrypt, socketio, csrf, mail
from app.forms import RegistrationForm, LoginForm, PersonalityForm, EditBirthdayForm, EditGenderPronounsForm, ChatForm, PreTestAcknowledgementForm, EditLoginForm, TwoFactorSetupForm, TwoFactorVerifyForm
from app.models import User, ChatMessage, TestSession
from app.ollama import generate_ai_response
from app.utils import load_questions, calculate_trait_scores, determine_investment_profile
from flask_mailman import EmailMessage
import pyotp
import time
import random
import cred

# Toggle language route
@app.before_request
def set_language():
    g.language = session.get('language', 'en')

@app.route('/toggle_language', methods=['POST'])
@csrf.exempt  # To exempt this route from CSRF protection
def toggle_language():
    data = request.get_json()
    new_language = data.get('language')
    if new_language:
        session['language'] = new_language
        return jsonify({'status': 'success'})
    return jsonify({'status': 'failure'}), 400

# Home route
@app.route("/")
@app.route("/home", methods=['GET'])
def home():
    return render_template('home.html', title='Home')

# Authentication routes (register, login, logout)
@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, birth_date=form.birth_date.data,
                    gender=form.gender.data,
                    password=hashed_password, is_profile_complete=bool(form.birth_date.data))
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
    return render_template('register.html', title='Register', form=form)

@app.route("/two_factor_setup", methods = ['GET', 'POST'])
def two_factor_setup():
    # Partial Authenication
    user_id = session.get('user_id')
    if user_id == None:
        return redirect(url_for("login"))
    user = User.query.filter(User.id == user_id).first()

    form = TwoFactorSetupForm()
    if form.validate_on_submit():
        # Enabling 2FA
        if form.enable.data == "Yes":
            user.tf_active = True 
            user.totp_secret = pyotp.random_base32()   
            db.session.commit()
            return redirect(url_for('two_factor_verify'))
        else:
        # Disabling 2FA
            user.tf_active = False
            user.is_tf_complete = True
            db.session.commit()
            login_user(user, remember = session.get('remember'))
            if not user.is_profile_complete:
                    flash('Please complete your profile.', 'warning')
                    return redirect(url_for('edit_profile'))
            next_page = request.args.get('next')
            return redirect(next_page) if next_page and next_page.startswith('/') else redirect(url_for('home'))

    return render_template('two_factor_setup.html', title = 'Two Factor Setup', form = form)

@app.route("/two_factor_verify", methods = ['GET', 'POST'])
def two_factor_verify():
    if 'verify' in session:
        return redirect(url_for('home'))

    # Partial Authenication
    user_id = session.get('user_id')
    if user_id == None:
        return redirect(url_for("login"))
    user = User.query.filter(User.id == user_id).first()
    
    # Generating TOTP Object and Code
    if "totp" not in session:
        session["totp"] = True
        send_email()

    # Verification Code expires after 5 minutes.
    totp_object = pyotp.TOTP(user.totp_secret, interval = 300)

    # Confirm it is the correct code
    form = TwoFactorVerifyForm()
    if form.validate_on_submit():
        if form.submit.data:
            if totp_object.verify(form.token.data, valid_window = 1):
                login_user(user, remember=session.get('remember'))
                user.last_tf = datetime.utcnow()
                user.is_tf_complete = True
                db.session.commit()
                session['verify'] = True
                session.pop("remember")
                session.pop("user_id")
                session.pop("totp")
                return redirect(url_for('home'))
            else:
                form.token.data = ""
                flash('Verification Unsuccessful. Please either re-enter your verification code.', 'danger')
        
        if form.resend.data:
            send_email()
            flash('Verification Code has been sent to your email!', 'success')
            return redirect(url_for('two_factor_verify'))

    return render_template('two_factor_verify.html', title = "Two Factor Verify", form = form)

@app.route("/send_verification_code", methods = ['GET'])
def send_email():
    user_id = session.get('user_id')
    if user_id == None:
        return redirect(url_for("home"))
    user = User.query.filter(User.id == user_id).first()

    email = user.email
    totp = pyotp.TOTP(user.totp_secret, interval = 300)
    verification_code = totp.now()

    # Design for Email
    emailContent = f"""
    <html>
        <body>
            <h3>Your Verification Code:</h3>
            <h2 style = "color: red;">{verification_code}</h2>
            <p>This is your verification code for your TrustVest Media account. Please make sure to verify within 5 minutes. Please do not reply to this automatically generated email.
            </p>
            <p>Sincerely,</p>
            <p>TrustVest Media Support</p>
        </body>
    </html>
    """

    # Constructing EmailMessage Object
    msg = EmailMessage(
        subject="Your TrustVest Media Verification Code",
        body=emailContent,
        to=[email],
    )
    msg.content_subtype = "html"

    # Send email and check for errors
    try:
        msg.send()
    except Exception as e:
        return f"Failed to send email: {e}"        
    

@app.route("/login", methods=['GET', 'POST'])
def login():
    # Checking if the user is authenticated
    if current_user.is_authenticated:
        # Check to see if the 2FA setup is complete
        if not current_user.is_tf_complete:
            session['user_id'] = current_user.id
            session['remember'] = False
            return redirect(url_for('two_factor_setup'))
        else:
            return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username == form.user_id.data) | (User.email == form.user_id.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            # If User's 2FA is not completely setup
            if not user.is_tf_complete:
                session['user_id'] = user.id
                session['remember'] = form.remember.data
                return redirect(url_for('two_factor_setup'))
            # If 2FA is active and it has been 14 days since the last verify
            elif user.tf_active and datetime.utcnow() - user.last_tf > timedelta(days = 14) :
                session['user_id'] = user.id
                session['remember'] = form.remember.data
                return redirect(url_for('two_factor_verify'))
            else:
                login_user(user, remember=form.remember.data)
                if not user.is_profile_complete:
                    flash('Please complete your profile.', 'warning')
                    return redirect(url_for('edit_profile'))
                next_page = request.args.get('next')
                return redirect(next_page) if next_page and next_page.startswith('/') else redirect(url_for('home'))
        flash('Login Unsuccessful. Please check your username/email and password', 'danger')
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/logout")
def logout():
    ChatMessage.query.filter_by(user_id=current_user.id).delete()
    db.session.commit()
    if 'verify' in session:
        session.pop('verify')
    logout_user()
    return redirect(url_for('login'))

# Profile routes
@app.route("/profile")
@login_required
def profile():
    user = current_user
    return render_template('profile.html', title='Profile', user=user)

@app.route("/edit_profile", methods=['GET', 'POST'])
@fresh_login_required
def edit_profile():
    form_birthday = EditBirthdayForm()
    form_gender_pronouns = EditGenderPronounsForm()
    form_login = EditLoginForm()

    if form_login.validate_on_submit():
        current_user.username = form_login.username.data
        current_user.email = form_login.email.data
        if bcrypt.check_password_hash(current_user.password, form_login.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form_login.new_password.data).decode('utf-8')
            current_user.password = hashed_password
            db.session.commit()
            flash('Your login information has been updated!', 'success')
        else:
            flash("Incorrect previous password. Please enter again.")

    if form_birthday.validate_on_submit():
        current_user.birth_date = form_birthday.birth_date.data
        current_user.is_profile_complete = True
        db.session.commit()
        flash('Your birthdate has been updated!', 'success')
        return redirect(url_for('edit_profile'))

    if form_gender_pronouns.validate_on_submit() and form_gender_pronouns.pronouns.data != None:
        current_user.pronouns = form_gender_pronouns.pronouns.data
        db.session.commit()
        flash('Your pronouns have been updated!', 'success')
        return redirect(url_for('edit_profile'))

    if request.method == 'GET':
        form_login.username.data = current_user.username
        form_login.email.data = current_user.email
        form_birthday.birth_date.data = current_user.birth_date
        form_gender_pronouns.gender.data = current_user.gender
        form_gender_pronouns.pronouns.data = current_user.pronouns

    return render_template('edit_profile.html', title='Edit Profile', form_birthday=form_birthday, form_gender_pronouns=form_gender_pronouns, form_login=form_login)

# Chat routes
@app.route("/chat", methods=['GET', 'POST'])
@login_required
def chat():
    form = ChatForm()
    messages = ChatMessage.query.filter_by(user_id=current_user.id).order_by(ChatMessage.timestamp.asc()).all()
    return render_template('chat.html', title='Chat', form=form, messages=messages)

@app.route('/get_ai_response', methods=['POST'])
@login_required
def get_ai_response():
    data = request.get_json()

    if not data or 'message' not in data:
        return jsonify(error="Missing 'message' parameter in JSON data."), 400
    
    user_message = data['message']
    previous_messages = ChatMessage.query.filter_by(user_id=current_user.id).order_by(ChatMessage.timestamp.asc()).all()
    
    chat_history = [{'role': 'user' if msg.is_user else 'assistant', 'content': msg.message} for msg in previous_messages]
    chat_history.append({"role": "user", "content": user_message})

    try:
        ai_response = generate_ai_response(chat_history)
    except Exception as e:
        return jsonify(error=str(e)), 500

    try:
        user_chat_message = ChatMessage(username=current_user.username, message=user_message, is_user=True, user_id=current_user.id)
        ai_chat_message = ChatMessage(username='AI', message=ai_response, is_user=False, user_id=current_user.id)
        
        db.session.add(user_chat_message)
        db.session.add(ai_chat_message)
        db.session.commit()

        return jsonify(ai_response=ai_response)
    except Exception as e:
        db.session.rollback()
        return jsonify(error=str(e)), 500

# Socket.IO event handler
@socketio.on('message')
@login_required
def handleMessage(msg):
    msg = msg.strip()
    if msg:
        emit('message', {
            'username': current_user.username,
            'message': msg,
            'timestamp': datetime.now(timezone.utc).strftime("%H:%M")
        }, broadcast=True)
        chat_message = ChatMessage(username=current_user.username, message=msg, is_user=True, user_id=current_user.id)
        db.session.add(chat_message)
        db.session.commit()

# Personality test route
@app.route("/pre_test", methods=['GET', 'POST'])
@login_required
def pre_test():
    form = PreTestAcknowledgementForm()
    if form.validate_on_submit():
        if form.acknowledge.data:
            new_session = TestSession(user_id=current_user.id, acknowledgement=True)
            db.session.add(new_session)
            db.session.commit()
            flash('Thank you for acknowledging the terms. You may now proceed with the test.', 'success')
            return redirect(url_for('personality_test', session_id=new_session.id))
    return render_template('pre_test.html', title='Pre-Test Acknowledgement', form=form)

@app.route("/personality_test", methods=['GET', 'POST'])
@login_required
def personality_test():
    form = PersonalityForm()

    # Use the loaded questions from utils
    questions = load_questions()
    
    # Flatten and randomize questions
    all_questions = [(trait, q, field) for trait, qs in questions.items() for q, field in qs]
    random.shuffle(all_questions)
    
    # Group questions into sets of three
    question_groups = [all_questions[i:i+3] for i in range(0, len(all_questions), 3)]

    if form.validate_on_submit():
        # Calculate scores based on the form inputs
        traits = calculate_trait_scores(all_questions, form)

        # Save the trait scores to user profile
        for trait, score in traits.items():
            setattr(current_user, trait, score)

        # Determine the investment profile
        profile_type = determine_investment_profile(traits)

        # Gender routing
        gender_suffix = '1' if current_user.gender == 'Male' else '2'
        profile_route = profile_type + '_' + gender_suffix

        current_user.investment_profile = profile_route
        db.session.commit()

        flash('Your investment profile is now available. You can always review it from the profile tab!', 'success')
        return redirect(url_for(profile_route))

    return render_template('personality_test.html', title='Personality Test', form=form, question_groups=question_groups, enumerate=enumerate)

# The 1 represents user is Male.
@app.route('/investment_profile/over_controlled_1')
@login_required
def over_controlled_1():
    return render_template('investment_profile/over_controlled_1.html')

@app.route('/investment_profile/resilient_1')
@login_required
def resilient_1():
    return render_template('investment_profile/resilient_1.html')

@app.route('/investment_profile/under_controlled_1')
@login_required
def under_controlled_1():
    return render_template('investment_profile/under_controlled_1.html')

# The 2 represents user is Female.
@app.route('/investment_profile/over_controlled_2')
@login_required
def over_controlled_2():
    return render_template('investment_profile/over_controlled_2.html')

@app.route('/investment_profile/resilient_2')
@login_required
def resilient_2():
    return render_template('investment_profile/resilient_2.html')

@app.route('/investment_profile/under_controlled_2')
@login_required
def under_controlled_2():
    return render_template('investment_profile/under_controlled_2.html')

# Renewing the persistant cookie every 2 days while there is user activity
@app.before_request
def renew_persistent_cookies():
    session.modified = True
    if current_user.is_authenticated and request.cookies.get("remember-token"):
        last_renewal = session.get("last_renewal")
        if last_renewal:
            last_renewal = datetime.fromisoformat(last_renewal) 

            if datetime.utcnow() - last_renewal > timedelta(days = 2):
                login_user(user, remember=True)

        session['last_renewal'] = datetime.utcnow().isoformat()