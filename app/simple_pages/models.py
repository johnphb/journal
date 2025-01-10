from flask_login import UserMixin
from sqlalchemy.orm import relationship
from app.extensions.database import db
from datetime import datetime, timezone

class User(UserMixin, db.Model):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  uname = db.Column(db.String(15), unique=True)
  pword = db.Column(db.String(20))
  created_at = db.Column(db.DateTime, default=datetime.now(timezone.utc))

  # Ensures that Entries are deleted with User
  entries = relationship('Entries', backref='user', cascade='all, delete-orphan')


class Entries(db.Model):
  __tablename__ = 'entries'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='CASCADE'), nullable=False) # Ensures that Entries are deleted with User
  date = db.Column(db.Date, nullable=False) 
  title = db.Column(db.String(20))
  content = db.Column(db.String)