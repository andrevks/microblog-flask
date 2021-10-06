from flask import render_template
from app import app_obj, db

@app_obj.errorhandler(404)
def not_found_error(error):
  return render_template('404.html'), 404

@app_obj.errorhandler(500)
def internal_error(error):
  #To not have a problem with the db.
  #This resets the session to a clean state.
  db.session.rollback()
  return render_template('500.html'), 500