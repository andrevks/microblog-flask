'''
  In the first time, Flask needs to be told
  how to import the application, by setting
  the FLASK_APP environment variable:

  (venv) $ export FLASK_APP=microblog.py
  
  or 

  (venv) $ set FLASK_APP=microblog.py
'''
from app import app_obj