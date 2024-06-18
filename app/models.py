from datetime import datetime
from app import db, login_manager
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    birth_date = db.Column(db.Date)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    gender = db.Column(db.String(10))
    pronouns = db.Column(db.String(30))
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    messages = db.relationship('ChatMessage', backref='author', lazy=True)
    is_profile_complete = db.Column(db.Boolean, default=False)
    openness = db.Column(db.Integer, nullable=True)
    conscientiousness = db.Column(db.Integer, nullable=True)
    extraversion = db.Column(db.Integer, nullable=True)
    agreeableness = db.Column(db.Integer, nullable=True)
    neuroticism = db.Column(db.Integer, nullable=True)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class ChatMessage(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(140), nullable=False)  # adjusted line
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    username = db.Column(db.String(80))  # added line

    def __repr__(self):
        return f"ChatMessage('{self.message}', '{self.timestamp}')"
    
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(140), nullable=False)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return f"Post('{self.content}', '{self.timestamp}')"