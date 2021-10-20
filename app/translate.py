import json 
import requests
from flask_babel import _
from app import app_obj

def translate(text, source_language, dest_language):
  if 'MS_TRANSLATOR_KEY' not in app_obj.config or \
    not app_obj.config['MS_TRANSLATOR_KEY']:
    return _('Error: the translation service is not configure.')
  auth = {
    'Ocp-Apim-Subscription-Key': app_obj.config['MS_TRANSLATOR_KEY'],
    'Ocp-Apim-Subscription-Region': 'global'
  }
  r = requests.post(

    'https://api.cognitive.microsofttranslator.com'
    f'/translate?api-version=3.0&from={source_language}&to={dest_language}',
    headers=auth,
    json=[{'Text': text}])
  
  if r.status_code != 200:
    return _('Error: the translation service failed.')
  return r.json()[0]['translations'][0]['text']
