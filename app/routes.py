'''
 In Flask, handlers for the application routes 
 are written as Python functions, called view functions.

 View functions are mapped to one or more route URLs
 so that Flask knows what logic to execute when 
 a client requests a given URL.
'''
from datetime import datetime
from flask.templating import render_template_string
from flask_wtf import form
from app import db
from app import email
from app.forms import EditProfileForm, PostForm, RegistrationForm
from app.forms import ResetPasswordRequestForm, EmptyForm, PostForm, ResetPasswordForm
from flask import request 
from werkzeug.urls import url_parse
from flask_login import logout_user, login_required
from flask_login import current_user, login_user
from app.models import User, Post
from flask import render_template, flash, redirect, url_for, g
from app import app_obj
from app.forms import LoginForm, ResetPasswordForm
from app.email import send_password_reset_email
from flask_babel import _, get_locale



#First View Function
@app_obj.route('/', methods=['GET', 'POST'])
@app_obj.route('/index', methods=['GET', 'POST'])
@login_required
def index():
  form = PostForm()
  if form.validate_on_submit():
    post = Post(body=form.post.data, author=current_user)
    db.session.add(post)
    db.session.commit()
    flash(_('Your post is now live!'))
    #To prevent the post request to be done once more
    #the best practice is to redirect the page. This means to make a 
    #get request and doing so prevents an annoyance
    #with how the refresh command is implemented in web 
    #browsers.
    return redirect(url_for('index'))
  page = request.args.get('page', 1, type=int)
  posts = current_user.followed_posts().paginate(
    page, app_obj.config['POSTS_PER_PAGE'], False)
  next_url = url_for('index', page=posts.next_num) \
    if posts.has_next else None
  prev_url = url_for('index', page=posts.prev_num) \
    if posts.has_prev else None
  return render_template('index.html', title=_('Home Page'), form=form,
   posts=posts.items, next_url=next_url, prev_url=prev_url)

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
      flash(_('Invalid username or password'))
      return redirect(url_for('login'))
    login_user(user, remember=form.remember_me.data)
    next_page = request.args.get('next')
    if not next_page or url_parse(next_page).netloc != '':
      next_page = url_for('index')
    return redirect(url_for('index'))
  return render_template('login.html', title=_('Sign in'), form=form) 

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
    flash(_('Congratulations, you are now a registered user!'))
    return redirect(url_for('login'))
  return render_template('register.html', title=_('Register'), form=form)
  
@app_obj.route('/user/<username>')
@login_required
def user(username):
  #It sends automatically a 404 error back to the client
  #in case the user hasn't been found.
  user = User.query.filter_by(username=username).first_or_404()
  page = request.args.get('page', 1, type=int)
  posts = user.posts.order_by(Post.timestamp.desc()).paginate(
    page, app_obj.config['POSTS_PER_PAGE'], False)
  next_url = url_for('user', username=user.username, page=posts.next_num) \
    if posts.has_next else None
  prev_url = url_for('index', username=user.username, page=posts.prev_num) \
    if posts.has_prev else None
  form = EmptyForm()
  return render_template('user.html', user=user, posts=posts.items,
                        next_url=next_url,prev_url=prev_url, 
                        form=form)

@app_obj.before_request
def before_request():
  if current_user.is_authenticated:
    #There's no db.session.add() bf
    #bc the the user is loaded already
    current_user.last_seen = datetime.utcnow()
    db.session.commit()
  g.locale = str(get_locale())

@app_obj.route('/edit_profile', methods=['GET','POST'])
@login_required
def edit_profile():
  form = EditProfileForm(current_user.username)
  if form.validate_on_submit():
    current_user.username = form.username.data
    current_user.about_me = form.about_me.data
    db.session.commit()
    flash(_('Your changes have been saved.'))
    return redirect(url_for('edit_profile'))
  elif request.method == 'GET':
    form.username.data = current_user.username
    form.about_me.data = current_user.about_me
  return render_template('edit_profile.html', title=_('Edit Profile'),
                         form=form)

@app_obj.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
  form = EmptyForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=username).first()
    if user is None:
      flash(_('User %(username)s not found.', username=username))
      return redirect(url_for('index'))
    elif user == current_user:
      flash(_('You cannot follow yourself!'))
      return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('user', username=username))
  else:
    return redirect(url_for('index'))
  
@app_obj.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
  form = EmptyForm()
  if form.validate_on_submit():
    user = User.query.filter_by(username=username).first()
    if user is None:
      flash(_('User %(username)s not found.', username=username))
      return redirect(url_for('index'))
    elif user == current_user:
      flash(_('You cannot unfollow yourself!'))
      return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('user', username=username))
  else:
    return redirect(url_for('index'))

@app_obj.route('/explore')
@login_required
def explore():
  page = request.args.get('page', 1, type=int)
  posts = Post.query.order_by(Post.timestamp.desc()).paginate(
    page, app_obj.config['POSTS_PER_PAGE'], False)
  next_url = url_for('index', page=posts.next_num) \
    if posts.has_next else None
  prev_url = url_for('index', page=posts.prev_num) \
    if posts.has_prev else None
  #The template here is similar to index except there's no form
  return render_template('index.html', title=_('Explore'), posts=posts.items,
                         next_url=next_url, prev_url=prev_url)


@app_obj.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  form = ResetPasswordRequestForm()
  if form.validate_on_submit():
    user = User.query.filter_by(email=form.email.data).first()
    if user:
      send_password_reset_email(user)
    flash(_('Check your email for the instructions to reset your password'))
    return redirect(url_for('login'))
  return render_template('reset_password_request.html',
                        title=_('Reset Password'), form=form)

@app_obj.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
  if current_user.is_authenticated:
    return redirect(url_for('index'))
  user = User.verify_reset_password_token(token)
  if not user:
    return redirect(url_for('index'))
  form = ResetPasswordForm()
  if form.validate_on_submit():
    user.set_password(form.password.data)
    db.session.commit()
    flash(_('Your password has been reset.'))
    return redirect(url_for('login'))
  return render_template('reset_password.html',form=form)