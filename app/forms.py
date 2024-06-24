from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields import DateField
from app.models import User
import json

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    birth_date = DateField('BirthDate', format='%Y-%m-%d', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    gender = StringField('Gender')
    pronouns = StringField('Pronouns')
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
    gender = StringField('Gender', validators=[DataRequired()])
    pronouns = StringField('Pronouns', validators=[DataRequired()])
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

with open('questions.json') as f:
    questions = json.load(f)

for trait, qs in questions.items():
    for text, field_name in qs:
        setattr(PersonalityForm, field_name, RadioField(
            text,
            choices=[('4', 'Strongly Agree'), ('3', 'Agree'), ('2', 'Disagree'), ('1', 'Strongly Disagree')],
            validators=[DataRequired()]
        ))