from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
from . import simple_pages
from app.extensions.database import db, migrate

# Some Commands to Remember:
# % flask db init
# % flask db migrate
# % flask db upgrade
# % sqlite3 ./instance/database.db
# % git add .
# % git commit -m ""

from app.simple_pages.models import User, Entries
from sqlalchemy import inspect

load_dotenv() # Load .env variables

def log_database_info(app):
    with app.app_context():
        inspector = inspect(db.engine)

        # Log table schema
        for table_name in inspector.get_table_names():
            app.logger.info(f"Schema for table {table_name}:")
            for column in inspector.get_columns(table_name):
                app.logger.info(f"Column: {column['name']}, Type: {column['type']}")

        # Log some content from the tables
        users = User.query.limit(5).all()
        for user in users:
            app.logger.info(f"User: {user.uname}, Created At: {user.created_at}")

        entries = Entries.query.limit(5).all()
        for entry in entries:
            app.logger.info(f"Entry: {entry.title}, Date: {entry.date}")


def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')

    app.config.from_object('app.config.Config') # load Config Variables

    register_extensions(app)
    register_blueprints(app)

    return app

def register_blueprints(app: Flask):
    app.register_blueprint(simple_pages.routes.blueprint)

def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = "simple_pages.login"  # Tells Flask-login where users login
    login_manager.init_app(app)

    # User loader callback
    from app.simple_pages.models import User  # Import User model
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    