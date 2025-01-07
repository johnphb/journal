from dotenv import load_dotenv
from os import environ
import os

load_dotenv()

SQLALCHEMY_DATABASE_URI = environ.get('DATABASE_URL')

class Config:
    # Configuration Variables:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')