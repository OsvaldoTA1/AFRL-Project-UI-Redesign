import json
from wtforms import RadioField
from wtforms.validators import DataRequired


def load_questions(file_path='questions.json'):
    """Load questions from a JSON file."""
    with open(file_path) as f:
        return json.load(f)


def add_personality_questions(form_class, questions):
    """Add personality test questions to a form class."""
    for trait, qs in questions.items():
        for text, field_name in qs:
            setattr(form_class, field_name, RadioField(
                text,
                choices=[('4', 'Strongly Agree'), ('3', 'Agree'), ('2', 'Disagree'), ('1', 'Strongly Disagree')],
                validators=[DataRequired()]
            ))

questions = load_questions()