
#Icludes generic implementations for most users models classes
from time import time
import jwt
from app import app_obj
from hashlib import md5
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from app import db
from app import login

#Association table that has no data other than 
#the foreign keys (No associated model class)
follower = db.Table('follower',
  db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
  db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)
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
  #Extra info for the profile
  about_me = db.Column(db.String(140))
  last_seen = db.Column(db.DateTime, default=datetime.utcnow)
  followed = db.relationship(
    #Right side entity of the relationship
    'User', secondary=follower,
    #Left side of the relationship is (follower -> id)
    primaryjoin=(follower.c.follower_id == id),
    #Right side of the relationship (followed -> id)
    secondaryjoin=(follower.c.followed_id == id),
    #How thi
    backref=db.backref('follower', lazy='dynamic'),
    lazy='dynamic'
  )

  def __repr__(self):
    #Tells how to print objects of this class
    return '<User {}>'.format(self.username)
  
  def set_password(self, password):
    self.password_hash = generate_password_hash(password)
  
  def check_password(self, password):
    return check_password_hash(self.password_hash, password)

  def avatar(self, size):
    digest = md5(self.email.lower().encode('utf-8')).hexdigest()
    return f'https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}'

  def follow(self, user):
    if not self.is_following(user):
      self.followed.append(user)

  def unfollow(self, user):
    if self.is_following(user):
      self.followed.remove(user)

  def is_following(self, user):
    return self.followed.filter( 
      follower.c.followed_id == user.id).count() > 0
  
  def followed_posts(self):
    followed = Post.query.join(
      follower, (follower.c.followed_id == Post.user_id)).filter(
        follower.c.follower_id == self.id)
    own = Post.query.filter_by(user_id=self.id)
    #Combined into one, before the sorting is applied
    return followed.union(own).order_by(Post.timestamp.desc()) 

  def get_reset_password_token(self, expires_in=600):
    return jwt.encode(
      {'reset_password': self.id, 'exp': time()+expires_in},
      app_obj.config['SECRET_KEY'], algorithm='HS256')

  @staticmethod #Can be invoked directly from the class
  def verify_reset_password_token(token):
    try:
      id = jwt.decode(token, app_obj.config['SECRET_KEY'],
                     algorithms=['HS256'])['reset_password']
    except:
      return 
    return User.query.get(id)

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
