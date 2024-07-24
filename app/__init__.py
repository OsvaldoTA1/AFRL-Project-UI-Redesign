from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
import cred

socketio = SocketIO()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
csrf = CSRFProtect()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with secure key in production
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['RECAPTCHA_PUBLIC_KEY'] = cred.RECAPTCHA_PUBLIC_KEY
    app.config['RECAPTCHA_PRIVATE_KEY'] = cred.RECAPTCHA_PRIVATE_KEY


    app.static_folder = 'static'
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)

    with app.app_context():
        from . import views

    return app