from flask import Blueprint, request
from werkzeug.exceptions import Unauthorized, BadRequest
import re
from base64 import b64decode

login_api_blueprint = Blueprint('login_api_blueprint',__name__)

@login_api_blueprint.route('/', methods=['GET'])
def login():
  authHeader = request.headers.get('Authorization')
  if authHeader is None:
    raise BadRequest('Missing Authorization Header')
  authHeader = authHeader.strip()
  base64Str = ''
  if re.match('basic ', authHeader, re.I):
    base64Str = authHeader[6:]
  elif re.match('ldap ', authHeader, re.I):
    base64Str = authHeader[5:]
  if base64Str == '':
    raise BadRequest('Invalid Authorization Header')
  try:
    decoded = b64decode(base64Str).decode()
  except:
    raise BadRequest('Invalid Authorization Header (encoding)')

  arr = decoded.split(':')
  if len(arr) != 2:
    raise BadRequest('Invalid Authorization Header (value)')
  username = arr[0]
  password = arr[1]

  print(username)
  print(password)



  #raise BadRequest('Not Implemented')
  raise Exception('TODO')

def registerAPI(appObj):
  appObj.flaskAppObject.register_blueprint(login_api_blueprint, url_prefix='/login')
