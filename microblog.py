'''
  In the first time, Flask needs to be told
  how to import the application, by setting
  the FLASK_APP environment variable:

  (venv) $ export FLASK_APP=microblog.py
  
  or 

  (venv) $ set FLASK_APP=microblog.py
'''
from app import app_obj, db, cli
from app.models import User, Post

#Sheel context with the db and models
#This decorator registers the function as a shell 
#context function.
@app_obj.shell_context_processor
def make_shell_context():
  return {'db': db, 'User': User, 'Post': Post}