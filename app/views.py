from flask import render_template, url_for, flash, redirect, request, jsonify
from flask import current_app as app
from app import db, bcrypt, socketio
from app.forms import RegistrationForm, LoginForm, PersonalityForm, EditBirthdayForm, EditGenderPronounsForm, ChatForm
from app.models import User, ChatMessage
from flask_login import login_user, current_user, logout_user, login_required
from datetime import datetime, timezone
from flask_socketio import emit
from app.ollama import generate_ai_response
from app.utils import load_questions

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

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter((User.username == form.user_id.data) | (User.email == form.user_id.data)).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
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
    logout_user()
    return redirect(url_for('login'))

# Profile routes
@app.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', title='Profile', user=user)

@app.route("/edit_profile", methods=['GET', 'POST'])
@login_required
def edit_profile():
    form_birthday = EditBirthdayForm()
    form_gender_pronouns = EditGenderPronounsForm()

    if form_birthday.validate_on_submit():
        current_user.birth_date = form_birthday.birth_date.data
        current_user.is_profile_complete = True
        db.session.commit()
        flash('Your birthdate has been updated!', 'success')

    if form_gender_pronouns.validate_on_submit():
        current_user.pronouns = form_gender_pronouns.pronouns.data
        db.session.commit()
        flash('Your pronouns have been updated!', 'success')

    if request.method == 'GET':
        form_birthday.birth_date.data = current_user.birth_date
        form_gender_pronouns.gender.data = current_user.gender
        form_gender_pronouns.pronouns.data = current_user.pronouns

    return render_template('edit_profile.html', title='Edit Profile', form_birthday=form_birthday, form_gender_pronouns=form_gender_pronouns)

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
@app.route("/personality_test", methods=['GET', 'POST'])
@login_required
def personality_test():
    form = PersonalityForm()
    questions = load_questions()

    if form.validate_on_submit():
        traits = {
            'openness': 0,
            'conscientiousness': 0,
            'extraversion': 0,
            'agreeableness': 0,
            'neuroticism': 0,
        }

        # Calculate scores based on the form inputs
        for trait, question_pairs in questions.items():
            trait_score = sum(int(getattr(form, field).data) for _, field in question_pairs)
            traits[trait] = trait_score

        # Save the trait scores to user profile.
        current_user.openness = traits['openness']
        current_user.conscientiousness = traits['conscientiousness']
        current_user.extraversion = traits['extraversion']
        current_user.agreeableness = traits['agreeableness']
        current_user.neuroticism = traits['neuroticism']

        # Determine the investment profile
        O, C, E, A, N = traits['openness'], traits['conscientiousness'], traits['extraversion'], traits['agreeableness'], traits['neuroticism']
        if 6 <= O <= 12 and 6 <= C <= 12 and 3 <= E <= 5 and 6 <= A <= 12 and 10 <= N <= 12:
            profile_type = 'over_controlled_1'
        elif 6 <= O <= 9 and 10 <= C <= 12 and 6 <= E <= 9 and 10 <= A <= 12 and 3 <= N <= 5:
            profile_type = 'resilient_2'
        elif 3 <= O <= 9 and 6 <= C <= 9 and 10 <= E <= 12 and 3 <= A <= 9 and 3 <= N <= 12:
            profile_type = 'under_controlled_3'
        else:
            profile_type = 'over_controlled_1'

        current_user.investment_profile = profile_type
        db.session.commit()

        flash('Your investment profile is now available.\nYou can always review it from the profile tab!', 'success')
        return redirect(url_for(profile_type))

    return render_template('personality_test.html', title='Personality Test', form=form, questions=questions, enumerate=enumerate)

@app.route('/investment_profile/over_controlled_1')
@login_required
def over_controlled_1():
    return render_template('investment_profile/over_controlled_1.html')

@app.route('/investment_profile/resilient_2')
@login_required
def resilient_2():
    return render_template('investment_profile/resilient_2.html')

@app.route('/investment_profile/under_controlled_3')
@login_required
def under_controlled_3():
    return render_template('investment_profile/under_controlled_3.html')