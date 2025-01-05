from app.extensions.database import db
from datetime import datetime, timezone

class User(db.Model):
  __tablename__ = 'user'

  id = db.Column(db.Integer, primary_key=True)
  uname = db.Column(db.String(15), unique=True)
  pword = db.Column(db.String(20))

class Entries(db.Model):
  __tablename__ = 'entries'

  id = db.Column(db.Integer, primary_key=True)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
  date = db.Column(db.Date, nullable=False) #default=datetime.now(timezone.utc))
  title = db.Column(db.String(20))
  content = db.Column(db.String)