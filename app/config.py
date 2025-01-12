from dotenv import load_dotenv
import os

# Load vars from .env file
load_dotenv()

# DB configuration
SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')

class Config:
    # Configuration Variables:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'default_secret_key')