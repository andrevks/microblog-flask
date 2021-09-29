'''
 In Flask, handlers for the application routes 
 are written as Python functions, called view functions.

 View functions are mapped to one or more route URLs
 so that Flask knows what logic to execute when 
 a client requests a given URL.
'''

from app import app_obj


#First View Function
@app_obj.route('/')
@app_obj.route('/index')
def index():
  return "Hello, world! let\'s do this "