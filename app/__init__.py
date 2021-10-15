'''
The application will exist in a package. 

In Python, a sub-directory that includes a __init__.py 
file is considered a package, and can be imported. 

So the app is the package that will host the application.
'''
import os
import logging
from logging.handlers import SMTPHandler,RotatingFileHandler
from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail
from flask_bootstrap import Bootstrap
#App object from the Class Flask
app_obj = Flask(__name__)
#Config file necessary in flask app
app_obj.config.from_object(Config)
#DB-ORM
db = SQLAlchemy(app_obj)
migrate = Migrate(app_obj, db)
login = LoginManager(app_obj)
#To force the login in certain pages
login.login_view = 'login'
#Mail
mail = Mail(app_obj)
#CSS Framework
bootstrap = Bootstrap(app_obj)

if not app_obj.debug:
  #Email Errors Notifications:
  if app_obj.config['MAIL_SERVER']:
    auth = None
    if app_obj.config['MAIL_USERNAME'] or app_obj.config['MAIL_PASSWORD']:
      auth = (app_obj.config['MAIL_USERNAME'], app_obj.config['MAIL_PASSWORD'])
    secure = None
    if app_obj.config['MAIL_USE_TLS']:
      secure = ()
    mail_handler = SMTPHandler(
      mailhost= (app_obj.config['MAIL_SERVER'], app_obj.config['MAIL_PORT']),
      fromaddr='no-reply@' + app_obj.config['MAIL_SERVER'],
      toaddrs=app_obj.config['ADMINS'], 
      subject='Microblog Failure',
      credentials=auth, secure=secure
    )
    #So that it only reports errors
    mail_handler.setLevel(logging.ERROR)
    #And attaches it to the app.logger object
    app_obj.logger.addHandler(mail_handler)
  #End_EMAIl
  if not os.path.exists('logs'):
    os.mkdir('logs')
  file_handler = RotatingFileHandler('logs/microblog.log', maxBytes=10240,
                                    backupCount=10)
  file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
  ))
  file_handler.setLevel(logging.INFO)
  app_obj.logger.addHandler(file_handler)

  app_obj.logger.setLevel(logging.INFO)
  app_obj.logger.info('Microblog startup')

#The bottom import is a workaround to circular imports.
#This happens whenever there are multiple references
#between files.
#models = define the structure of the db
from app import routes, models, errors