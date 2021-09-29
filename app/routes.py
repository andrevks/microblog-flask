'''
 In Flask, handlers for the application routes 
 are written as Python functions, called view functions.

 View functions are mapped to one or more route URLs
 so that Flask knows what logic to execute when 
 a client requests a given URL.
'''
from flask import render_template, flash, redirect, url_for
from app import app_obj
from app.forms import LoginForm


#First View Function
@app_obj.route('/')
@app_obj.route('/index')
def index():
  user = {'username':'Andre'}
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
  return render_template('index.html', title='Home', user=user, posts=posts)

@app_obj.route('/login', methods=['GET', 'POST'])
def login():
  form = LoginForm()
  if form.validate_on_submit():
    # When the browser sends the POST request
    #and everything is all right in the form.
    flash('Login requested user {}, remember_me={}'.format(
      form.username.data,form.remember_me.data))
    return redirect(url_for('index'))
  return render_template('login.html', title='Sign in', form=form) 