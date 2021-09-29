'''
The application will exist in a package. 

In Python, a sub-directory that includes a __init__.py 
file is considered a package, and can be imported. 

So the app is the package that will host the application.
'''

from flask import Flask
from config import Config

#App object from the Class Flask
app_obj = Flask(__name__)
#Config file necessary in flask app
app_obj.config.from_object(Config)

#The bottom import is a workaround to circular imports.
#This happens whenever there are multiple references
#between files.
from app import routes