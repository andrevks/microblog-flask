
#Icludes generic implementations for most users models classes
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from app import login

#Inherts from db.Model base class for all models
#flask db migrate -m "users table"
#flask db upgrade
class User(UserMixin, db.Model):
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
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

class Post(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  body = db.Column(db.String(140))
  #This ensures that you are using uniform timestamps regardless
  # of where the users are Located. These timestamps will 
  # be converted to the user's local time when they are 
  # displayed.
  timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
  user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

  def __repr__(self):
    return '<Post {}>'.format(self.body)

#Loader Function
@login.user_loader
def load_user(id):
  return User.query.get(int(id))