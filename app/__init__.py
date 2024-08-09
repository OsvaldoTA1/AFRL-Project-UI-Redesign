from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_socketio import SocketIO
from flask_mailman import Mail
from datetime import timedelta
import cred

socketio = SocketIO()
db = SQLAlchemy()
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
csrf = CSRFProtect()
mail = Mail()

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key'  # Replace with secure key in production
    app.config['WTF_CSRF_ENABLED'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    
    # Keys necessary for running the reCaptcha
    app.config['RECAPTCHA_PUBLIC_KEY'] = cred.RECAPTCHA_PUBLIC_KEY
    app.config['RECAPTCHA_PRIVATE_KEY'] = cred.RECAPTCHA_PRIVATE_KEY

    # Configuration for Session Management
    app.config['REMEMBER_COOKIE_SECURE'] = True # Persistant Cookies can only be sent through secure HTTPS connections
    app.config['REMEMBER_COOKIE_DURATION'] = timedelta(days = 7) # Persistant cookies expires within 7 days of creation

    app.config['SESSION_COOKIE_SECURE'] = True # Session Cookies can only be sent through secure HTTPS connection

    # Session cookies expire after 10 minutes or if the browser is closed, but gets automatically renewed if persistant cookie is active by Flask Login 
    # or if there is user activity
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes = 10) 

    # Configuration for Flask Mailman
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_USERNAME'] = cred.MAIL_USERNAME
    app.config['MAIL_PASSWORD'] = cred.MAIL_PASSWORD
    app.config['MAIL_DEFAULT_SENDER'] = cred.MAIL_USERNAME
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True

    app.static_folder = 'static'
    
    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    socketio.init_app(app)
    mail.init_app(app)

    with app.app_context():
        from . import views

    return app