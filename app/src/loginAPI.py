from flask import Blueprint, request, Response
from werkzeug.exceptions import Unauthorized, BadRequest
import re
from base64 import b64decode, urlsafe_b64decode
import jwt
import datetime
import json

login_api_blueprint = Blueprint('login_api_blueprint',__name__)


def registerAPI(appObj):
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

    ldapResult = appObj.ldapObj.verifyCredentials(username,password)
    if not ldapResult['Authed']:
      raise Unauthorized('Invald Credentials')

    kongusername = appObj.globalParamObject.LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX + username
    appObj.kongObj.ensureUserExistsWithACL(kongusername, ldapResult['Groups'])
    jwtToken = appObj.kongObj.getJWTToken(kongusername)

    encodedJWT = jwt.encode({
      'iss': jwtToken['key'],
      'exp': datetime.datetime.utcnow() + datetime.timedelta(seconds=int(appObj.globalParamObject.LOGINEP_JWT_TOKEN_TIMEOUT)),
      'username': username,
      'groups': ldapResult['Groups']
    }, b64decode(jwtToken['secret']), algorithm='HS256')
    return Response(json.dumps({'JWTToken': encodedJWT.decode('utf-8') }), status=200, mimetype='application/json')

  appObj.flaskAppObject.register_blueprint(login_api_blueprint, url_prefix='/login')
