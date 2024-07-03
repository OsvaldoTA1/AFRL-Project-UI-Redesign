from wtforms.validators import DataRequired
from wtforms import RadioField
import json

# utility for fetching questions.json properties - forms.py, views.py
def load_questions(file_path='questions.json'):
    """Load questions from a JSON file."""
    with open(file_path) as f:
        return json.load(f)

# Question score depending on input
def add_personality_questions(form_class, questions):
    """Add personality test questions to a form class."""
    for trait, qs in questions.items():
        for text, field_name in qs:
            setattr(form_class, field_name, RadioField(
                text,
                choices=[('4', 'Strongly Agree'), ('3', 'Agree'), ('2', 'Disagree'), ('1', 'Strongly Disagree')],
                validators=[DataRequired()]
            ))


def calculate_trait_scores(all_questions, form):
    """Calculate personality traits based on form responses."""
    traits = {
        'openness': 0,
        'conscientiousness': 0,
        'extraversion': 0,
        'agreeableness': 0,
        'neuroticism': 0,
    }
    
    for trait, _, field in all_questions:
        traits[trait] += int(getattr(form, field).data)
    
    return traits

def determine_investment_profile(traits):
    """Determine the investment profile based on traits."""
    O, C, E, A, N = traits.values()
    if 6 <= O <= 12 and 6 <= C <= 12 and 3 <= E <= 5 and 6 <= A <= 12 and 10 <= N <= 12:
        profile_type = 'over_controlled'
    elif 6 <= O <= 9 and 10 <= C <= 12 and 6 <= E <= 9 and 10 <= A <= 12 and 3 <= N <= 5:
        profile_type = 'resilient'
    elif 3 <= O <= 9 and 6 <= C <= 9 and 10 <= E <= 12 and 3 <= A <= 9 and 3 <= N <= 12:
        profile_type = 'under_controlled'
    else:
        profile_type = 'over_controlled'
    
    return profile_type
