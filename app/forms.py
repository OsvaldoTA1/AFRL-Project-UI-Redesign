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

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    user_id = StringField('Username/Email', validators=[DataRequired()])  # replaced username with user_id
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError('That username does not exist. Please choose a different one or register.')

class PersonalityForm(FlaskForm):
    questions = {
        'openness': [
            ('I have a rich vocabulary.', 'openness_q1'),
            ('I have a vivid imagination.', 'openness_q2'),
            # Add more questions here
        ],
        'conscientiousness': [
            ('I am always prepared.', 'conscientiousness_q1'),
            ('I pay attention to details.', 'conscientiousness_q2'),
            # Add more questions here
        ],
        'extraversion': [
            ('I am the life of the party.', 'extraversion_q1'),
            ("I don't mind being the center of attention.", 'extraversion_q2'),
            #Add more questions here
        ],
        'agreeableness': [
            ('I find interest in people.', 'agreeableness_q1'),
            ("I feel others' emotions.", 'agreeableness_q2'),
            #Add more questions here
        ],
        'neuroticism': [
            ('I am easily disturbed.', 'neuroticism_q1'),
            ('I get upset easily.', 'neuroticism_q2'),
        ]
        # Add other traits
    }

    for trait, qs in questions.items():
        for text, field_name in qs:
            locals()[field_name] = RadioField(
                text,
                choices=[('5', 'Strongly Agree'), ('4', 'Agree'), ('3', 'Neutral'), ('2', 'Disagree'), ('1', 'Strongly Disagree')],
                validators=[DataRequired()]
            )
    submit = SubmitField('Submit')