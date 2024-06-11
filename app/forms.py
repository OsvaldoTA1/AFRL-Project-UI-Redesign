from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from wtforms.fields import DateField
from app.models import User
import json

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    birth_date = DateField('BirthDate', format='%Y-%m-%d', validators=[DataRequired()]) # New birth-date field
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
        
# Separate form for birthdate
class EditBirthdayForm(FlaskForm):
    birth_date = DateField('Birthdate', format='%Y-%m-%d', validators=[DataRequired()])
    submit = SubmitField('Save')

# Separate form for Gender and Pronouns
class EditGenderPronounsForm(FlaskForm):
    gender = StringField('Gender', validators=[DataRequired()])
    pronouns = StringField('Pronouns', validators=[DataRequired()])
    submit = SubmitField('Save')

class LoginForm(FlaskForm):
    user_id = StringField('Username/Email', validators=[DataRequired()])  # replaced username with user_id
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('That username does not exist. Please choose a different one or register.')

# Moved hardcoded questions to questions.jason file.
with open('questions.json') as f:
    questions = json.load(f)

class PersonalityForm(FlaskForm):
    for trait, qs in questions.items():
        for text, field_name in qs:
            locals()[field_name] = RadioField(
                text,
                choices=[('5', 'Strongly Agree'), ('4', 'Agree'), ('3', 'Neutral'), ('2', 'Disagree'), ('1', 'Strongly Disagree')],
                validators=[DataRequired()]
            )
    submit = SubmitField('Submit')