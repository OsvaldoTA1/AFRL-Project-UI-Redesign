from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from app.models import User
from flask import flash

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    email = StringField('Email', validators=[DataRequired(), Email()])

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            flash('That email is taken. Please choose a different one.', 'danger')
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

class PersonalityForm(FlaskForm):
    # Openness
    q1 = RadioField('I have a rich vocabulary.', choices=[('5', 'Strongly Agree'), ('4', 'Agree'),
        ('3', 'Neutral'), ('2', 'Disagree'), ('1', 'Strongly Disagree')])
    q2 = RadioField('I have a vivid imagination.', choices=[('5', 'Strongly Agree'), ('4', 'Agree'),
        ('3', 'Neutral'), ('2', 'Disagree'), ('1', 'Strongly Disagree')])
    # Repeat for other traits