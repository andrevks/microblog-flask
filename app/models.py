
from datetime import datetime
from app import db

#Inherts from db.Model base class for all models
#flask db migrate -m "users table"
#flask db upgrade
class User(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(64), index=True, unique=True)
  email = db.Column(db.String(120), index=True, unique=True)
  password_hash = db.Column(db.String(128))
  #Post is the model class that represents the 'many' side
  #
  posts = db.relationship('Post', backref='author', lazy='dynamic')

  def __repr__(self):
    #Tells how to print objects of this class
    return '<User {}>'.format(self.username)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(140))
  #This ensures that you are using uniform timestamps regardless
  # of where the users are located. These timestamps will 
  # be converted to the user's local time when they are 
  # displayed.
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Post {}>'.format(self.body)

