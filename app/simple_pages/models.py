from app.extensions.database import db

class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  uname = db.Column(db.String(15), unique=True)
  pword = db.Column(db.String(20))
