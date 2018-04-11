

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
  LOGINEP_VERSION = None
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
    self.LOGINEP_VERSION = self.readFromEnviroment(env, 'LOGINEP_VERSION', None, None)
    self.LOGINEP_LDAP_TIMEOUT = self.readFromEnviroment(env, 'LOGINEP_LDAP_TIMEOUT', None, None)
    self.LOGINEP_LDAP_HOST = self.readFromEnviroment(env, 'LOGINEP_LDAP_HOST', None, None)
    self.LOGINEP_LDAP_PORT = self.readFromEnviroment(env, 'LOGINEP_LDAP_PORT', None, None)
    self.LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX = self.readFromEnviroment(env, 'LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX', None, None)
    self.LOGINEP_USER_BASE_DN = self.readFromEnviroment(env, 'LOGINEP_USER_BASE_DN', None, None)
    self.LOGINEP_USER_ATTRIBUTE = self.readFromEnviroment(env, 'LOGINEP_USER_ATTRIBUTE', None, None)
    self.LOGINEP_KONG_ADMINAPI_URL = self.readFromEnviroment(env, 'LOGINEP_KONG_ADMINAPI_URL', None, None)
    self.LOGINEP_SYNCACL = self.readFromEnviroment(env, 'LOGINEP_SYNCACL', None, None)
    self.LOGINEP_JWT_TOKEN_TIMEOUT = self.readFromEnviroment(env, 'LOGINEP_JWT_TOKEN_TIMEOUT', None, None)

  def getStartupOutput(self):
    r = 'Starting kong_ldap_login_endpoint vertion:' + self.LOGINEP_VERSION + '\n'
    r += 'LOGINEP_LDAP_TIMEOUT:' + self.LOGINEP_LDAP_TIMEOUT + '\n'
    r += 'LOGINEP_LDAP_HOST:' + self.LOGINEP_LDAP_HOST + '\n'
    r += 'LOGINEP_LDAP_PORT:' + self.LOGINEP_LDAP_PORT + '\n'
    r += 'LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX:' + self.LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX + '\n'
    r += 'LOGINEP_USER_BASE_DN:' + self.LOGINEP_USER_BASE_DN + '\n'
    r += 'LOGINEP_USER_ATTRIBUTE:' + self.LOGINEP_USER_ATTRIBUTE + '\n'
    r += 'LOGINEP_KONG_ADMINAPI_URL:' + self.LOGINEP_KONG_ADMINAPI_URL + '\n'
    r += 'LOGINEP_SYNCACL:' + self.LOGINEP_SYNCACL + '\n'
    r += 'LOGINEP_JWT_TOKEN_TIMEOUT:' + self.LOGINEP_JWT_TOKEN_TIMEOUT + '\n'
    return r