from flask import Blueprint
from werkzeug.exceptions import Unauthorized, BadRequest

login_api_blueprint = Blueprint('login_api_blueprint',__name__)

@login_api_blueprint.route('/', methods=['GET'])
def login():
  raise Unauthorized('Not Implemented')

def registerAPI(appObj):
  appObj.flaskAppObject.register_blueprint(login_api_blueprint, url_prefix='/login')
