from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError
from wtforms.fields import DateField
from app.models import User
from app.utils import add_personality_questions, load_questions

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    birth_date = DateField('BirthDate', format='%Y-%m-%d', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = RadioField('Gender', choices=[('Male', 'Male'), ('Female', 'Female')], validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class EditBirthdayForm(FlaskForm):
    birth_date = DateField('Birthdate', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Save')

class EditGenderPronounsForm(FlaskForm):
    gender = StringField('Gender', render_kw={'readonly': True})
    pronouns = StringField('Pronouns')
    submit = SubmitField('Save')

class LoginForm(FlaskForm):
    user_id = StringField('Username/Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class ChatForm(FlaskForm):
    message = StringField('Message', validators=[DataRequired()])
    send = SubmitField('Send')

class PersonalityForm(FlaskForm):
    submit = SubmitField('Submit')

# Dynamically adds test questions from JSON (utils.py)
questions = load_questions()
add_personality_questions(PersonalityForm, questions)