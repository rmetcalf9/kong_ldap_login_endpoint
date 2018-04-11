

exceptions = dict()
def getInvalidEnvVarPAramaterException(envVarName):
  if envVarName not in exceptions:
    exceptions[envVarName] = InvalidEnvVarParamaterExecption(envVarName)
  return exceptions[envVarName]

class InvalidEnvVarParamaterExecption(Exception):
  def __init__(self, envVarName):
    message = 'Invalid value for ' + envVarName
    super(InvalidEnvVarParamaterExecption, self).__init__(message)

class GlobalParamatersClass():
  LOGINEP_LDAP_TIMEOUT = None
  LOGINEP_LDAP_HOST = None
  LOGINEP_LDAP_PORT = None
  LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX = None
  LOGINEP_USER_BASE_DN = None
  LOGINEP_USER_ATTRIBUTE = None
  LOGINEP_KONG_ADMINAPI_URL = None
  LOGINEP_SYNCACL = None
  LOGINEP_JWT_TOKEN_TIMEOUT = None


  #Read environment variable or raise an exception if it is missing and there is no default
  def readFromEnviroment(self, env, envVarName, defaultValue, acceptableValues):
    try:
      val = env[envVarName]
      if (acceptableValues != None):
        if (val not in acceptableValues):
          raise getInvalidEnvVarPAramaterException(envVarName)
      if val == '':
        raise getInvalidEnvVarPAramaterException(envVarName)
      return val
    except KeyError:
      if (defaultValue == None):
        raise getInvalidEnvVarPAramaterException(envVarName)
      return defaultValue

  def __init__(self, env):
    self.LOGINEP_LDAP_TIMEOUT = self.readFromEnviroment(env, 'LOGINEP_LDAP_TIMEOUT', None, None)
    self.LOGINEP_LDAP_HOST = self.readFromEnviroment(env, 'LOGINEP_LDAP_HOST', None, None)
    self.LOGINEP_LDAP_PORT = self.readFromEnviroment(env, 'LOGINEP_LDAP_PORT', None, None)
    self.LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX = self.readFromEnviroment(env, 'LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX', None, None)
    self.LOGINEP_USER_BASE_DN = self.readFromEnviroment(env, 'LOGINEP_USER_BASE_DN', None, None)
    self.LOGINEP_USER_ATTRIBUTE = self.readFromEnviroment(env, 'LOGINEP_USER_ATTRIBUTE', None, None)
    self.LOGINEP_KONG_ADMINAPI_URL = self.readFromEnviroment(env, 'LOGINEP_KONG_ADMINAPI_URL', None, None)
    self.LOGINEP_SYNCACL = self.readFromEnviroment(env, 'LOGINEP_SYNCACL', None, None)
    self.LOGINEP_JWT_TOKEN_TIMEOUT = self.readFromEnviroment(env, 'LOGINEP_JWT_TOKEN_TIMEOUT', None, None)
