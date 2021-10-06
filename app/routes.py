'''
 In Flask, handlers for the application routes 
 are written as Python functions, called view functions.

 View functions are mapped to one or more route URLs
 so that Flask knows what logic to execute when 
 a client requests a given URL.
'''
from datetime import datetime
from flask.templating import render_template_string
from app import db
import app
from app.forms import EditProfileForm, RegistrationForm
from flask import request 
from werkzeug.urls import url_parse
from flask_login import logout_user, login_required
from flask_login import current_user, login_user
from app.models import User 
from flask import render_template, flash, redirect, url_for
from app import app_obj
from app.forms import LoginForm


#First View Function
@app_obj.route('/')
@app_obj.route('/index')
@login_required
def index():
  posts = [
    {
      'author':{'username': 'John'},
      'body': 'Beautiful day in Portland!'
    },
    {
      'author':{'username': 'Susan'},
      'body': 'The Avengers movie was so cool!'
    },
    {
      'author':{'username': 'Kaylee'},
      'body': '“Happiness is found in doing, not merely possessing.” - Napoleon Hill, Think and Grow Rich'
    },
    {
      'author':{'username': 'Ada'},
      'body': '“Who you are, what you think, feel, and do, what you love—is the sum of what you focus on.” - Cal Newport, Deep Work'
    }
  ]
  return render_template('index.html', title='Home Page', posts=posts)

@app_obj.route('/login', methods=['GET', 'POST'])
def login():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = LoginForm()
  if form.validate_on_submit():
    # When the browser sends the POST request
    #and everything is all right in the form.
    #Load the user from the db
    user = User.query.filter_by(username=form.username.data).first()
    if user is None or not user.check_password(form.password.data):
      flash('Invalid username or password')
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(url_for('index'))
  return render_template('login.html', title='Sign in', form=form) 

@app_obj.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app_obj.route('/register', methods=['GET','POST'])
def register():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = RegistrationForm()
  if form.validate_on_submit():
    user = User(username=form.username.data, email=form.email.data)
    user.set_password(form.password.data)
    db.session.add(user)
    db.session.commit()
    flash('Congratulations, you are now a registered user!')
    return redirect(url_for('login'))
  return render_template('register.html', title='Register', form=form)
  
@app_obj.route('/user/<username>')
@login_required
def user(username):
  #It sends automatically a 404 error back to the client
  #in case the user hasn't been found.
  user = User.query.filter_by(username=username).first_or_404()
  #Fake list of the user's post 
  posts = [
    {
      'author': user,
      'body': 'Test post #1'
    },
    {
      'author': user,
      'body': 'Test post #2'
    },
  ]
  return render_template('user.html', user=user, posts=posts)

@app_obj.before_request
def before_request():
  if current_user.is_authenticated:
    #There's no db.session.add() bf
    #bc the the user is loaded already
    current_user.last_seen = datetime.utcnow()
    db.session.commit()

@app_obj.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
  form = EditProfileForm()
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash('Your changes have been saved.')
    return redirect(url_for('edit_profile'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', title='Edit Profile',
                         form=form)