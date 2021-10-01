'''
The application will exist in a package. 

In Python, a sub-directory that includes a __init__.py 
file is considered a package, and can be imported. 

So the app is the package that will host the application.
'''
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


#App object from the Class Flask
app_obj = Flask(__name__)
#Config file necessary in flask app
app_obj.config.from_object(Config)
#DB-ORM
db = SQLAlchemy(app_obj)
migrate = Migrate(app_obj, db)

#The bottom import is a workaround to circular imports.
#This happens whenever there are multiple references
#between files.
#models = define the structure of the db
from app import routes, models