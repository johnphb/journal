from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from . import simple_pages
from app.extensions.database import db
from app.simple_pages.models import User

# Load .env variables
load_dotenv() 

def create_app():
    # Create Flask app instance
    app = Flask(__name__)
    
    # Load configuration the config module
    app.config.from_object('app.config.Config')

    # Register extensions and blueprints
    register_extensions(app)
    register_blueprints(app)

    # Create DB tables if dont exist
    with app.app_context():
        db.create_all()

    return app

def register_blueprints(app: Flask):
    # Register blueprints 
    app.register_blueprint(simple_pages.routes.blueprint)

def register_extensions(app: Flask):
    ## Initialize extensions

    # Initialize the SQLAlchemy DB
    db.init_app(app)

    # Initialize Flask-Login 
    login_manager = LoginManager()
    login_manager.login_view = "simple_pages.login"  # Redirect if not logged in to login page
    login_manager.init_app(app)

    # Load a user from the database by their user ID.
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))