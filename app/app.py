
from flask import Flask
from . import simple_pages
from app.extensions.database import db, migrate



def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config')

    register_extensions(app)
    register_blueprints(app)

    return app

def register_blueprints(app: Flask):
    app.register_blueprint(simple_pages.routes.blueprint)

def register_extensions(app: Flask):
    db.init_app(app)
    migrate.init_app(app, db, compare_type=True)



