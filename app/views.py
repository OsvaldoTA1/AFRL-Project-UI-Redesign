from flask import render_template, url_for, flash, redirect, request, Flask
from flask import current_app as app
from app import db, bcrypt
from app.forms import RegistrationForm, LoginForm, PersonalityForm
from app.models import User
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
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
        user = User.query.filter_by(username=form.user_id.data).first() # assume user_id is a username
        if user is None:
            user = User.query.filter_by(email=form.user_id.data).first() # assume user_id is an email
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check your username/email and password', 'danger')
    for field, errors in form.errors.items():
        for error in errors:
            flash(f"Error in {getattr(form, field).label.text}: {error}", 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/profile/<username>")
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', title='Profile', user=user)

# personality_test helper
def get_form_field(form, field_name):
    return getattr(form, field_name)

@app.route("/personality_test", methods=['GET', 'POST'])
@login_required
def personality_test():
    form = PersonalityForm()
    if form.validate_on_submit():
        for trait in form.questions:
            question_fields = [q for _, q in form.questions[trait]]
            trait_score = sum(int(getattr(form, field).data) for field in question_fields)
            setattr(current_user, trait, trait_score)
        db.session.commit()
        flash('Your personality test is submitted!', 'success')
        return redirect(url_for('home'))
    # here you should pass the new get_form_field function to your template
    return render_template('personality_test.html', title='Personality Test', form=form, get_form_field=get_form_field)

@app.route("/logout")
def logout():
   logout_user()
   return redirect(url_for('home'))
