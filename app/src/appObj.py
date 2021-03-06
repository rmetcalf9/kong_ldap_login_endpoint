import signal
from flask import Flask, Blueprint
from GlobalParamaters import GlobalParamatersClass
from ldapWrapper import ldapClass
from kongAdminAPIWrapper import kongAdminAPIWrapperClass

from loginAPI import registerAPI as registerLoginApi

class appObj():
  flaskAppObject = None
  globalParamObject = None
  isInitOnce = False
  ldapObj = None
  kongObj = None
  def init(self, envirom, testingMode = False):
    self.globalParamObject = GlobalParamatersClass(envirom)
    self.ldapObj = ldapClass(self)
    self.kongObj = kongAdminAPIWrapperClass(self)
    if (self.isInitOnce):
      return
    self.isInitOnce = True
    self.initOnce()

  def initOnce(self):
    self.flaskAppObject = Flask(__name__)
    registerLoginApi(self)
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully) #sigterm is sent by docker stop command

    #Development code required to add CORS allowance in developer mode
    @self.flaskAppObject.after_request
    def after_request(response):
      if (self.globalParamObject.getDeveloperMode()):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
      return response

      
  # called by app.py to run the application
  def run(self):
    if (self.isInitOnce == False):
      raise Exception('Trying to run app without initing')
    print(self.globalParamObject.getStartupOutput())

    #appObj.flaskAppObject.config['SERVER_NAME'] = 'servername:123'
    try:
      self.flaskAppObject.run(host='0.0.0.0', port=self.globalParamObject.LOGINEP_PORT, debug=False)
    except self.ServerTerminationError as e:
      print("Stopped")

  def exit_gracefully(self, signum, frame):
    print("Exit Gracefully called")
    raise self.ServerTerminationError()

  class ServerTerminationError(Exception):
    def __init__(self):
      pass
    def __str__(self):
      return "Server Terminate Error"

appObj = appObj()