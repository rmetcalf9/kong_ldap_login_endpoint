import signal
from flask import Flask, Blueprint
from GlobalParamaters import GlobalParamatersClass
from ldap import ldapClass

from loginAPI import registerAPI as registerLoginApi

class appObj():
  flaskAppObject = None
  globalParamObject = None
  isInitOnce = False
  ldap = None
  def init(self, envirom, testingMode = False):
    self.globalParamObject = GlobalParamatersClass(envirom)
    self.ldap = ldapClass()
    if (self.isInitOnce):
      return
    self.isInitOnce = True
    self.initOnce()

  def initOnce(self):
    self.flaskAppObject = Flask(__name__)
    registerLoginApi(self)
    signal.signal(signal.SIGINT, self.exit_gracefully)
    signal.signal(signal.SIGTERM, self.exit_gracefully) #sigterm is sent by docker stop command

  # called by app.py to run the application
  def run(self):
    if (self.isInitOnce == False):
      raise Exception('Trying to run app without initing')
    print(self.globalParamObject.getStartupOutput())

    #appObj.flaskAppObject.config['SERVER_NAME'] = 'servername:123'
    try:
      self.flaskAppObject.run(host='0.0.0.0', port=80, debug=False)
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