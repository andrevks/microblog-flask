'''
 In Flask, handlers for the application routes 
 are written as Python functions, called view functions.

 View functions are mapped to one or more route URLs
 so that Flask knows what logic to execute when 
 a client requests a given URL.
'''
from flask import render_template
from app import app_obj


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