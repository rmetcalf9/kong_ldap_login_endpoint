from TestHelperSuperClass import testHelperSuperClass
from GlobalParamaters import GlobalParamatersClass, getInvalidEnvVarParamaterException

class testHelperSuperClass(testHelperSuperClass):
  def test_badParams(self):
    env = {
      'APIAPP_MODE': 'DEVELOPER',
      'APIAPP_VERSION': 'TEST-1.2.3',
      'APIAPP_FRONTEND': '_',
      'APIAPP_APIURL': 'http://apiurl',
      'APIAPP_APIACCESSSECURITY': '[]',
    }
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass(env)
    self.checkGotRightException(context,getInvalidEnvVarParamaterException('LOGINEP_VERSION'))

  def test_goodParams(self):
    env = {
      'LOGINEP_VERSION': 'TestRun',
      'LOGINEP_LDAP_TIMEOUT': '60',
      'LOGINEP_LDAP_HOST': 'unixldap.somehost.com',
      'LOGINEP_LDAP_PORT': '123',
      'LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX': 'ldap_',
      'LOGINEP_USER_BASE_DN': 'ou=People,ou=everyone,dc=somehost,dc=com',
      'LOGINEP_USER_ATTRIBUTE': 'uid',
      'LOGINEP_GROUP_BASE_DN': 'ou=Group,ou=everyone,dc=somehost,dc=com',
      'LOGINEP_GROUP_ATTRIBUTE': 'cn',
      'LOGINEP_GROUP_MEMBER_FIELD': 'memberUid',
      'LOGINEP_KONG_ADMINAPI_URL': 'http://kong:8001',
      'LOGINEP_SYNCACL': 'group1,group2,group3',
      'LOGINEP_JWT_TOKEN_TIMEOUT': '60'
    }
    gp = GlobalParamatersClass(env)

  def test_emptyParamsNotExcepted(self):
    env = {
      'LOGINEP_VERSION': 'TestRun',
      'LOGINEP_LDAP_TIMEOUT': '60',
      'LOGINEP_LDAP_HOST': 'unixldap.somehost.com',
      'LOGINEP_LDAP_PORT': '123',
      'LOGINEP_LDAP_CONSUMERCLIENTID_PREFIX': 'ldap_',
      'LOGINEP_USER_BASE_DN': 'ou=People,ou=everyone,dc=somehost,dc=com',
      'LOGINEP_USER_ATTRIBUTE': '',
      'LOGINEP_GROUP_BASE_DN': 'ou=Group,ou=everyone,dc=somehost,dc=com',
      'LOGINEP_GROUP_ATTRIBUTE': 'cn',
      'LOGINEP_GROUP_MEMBER_FIELD': 'memberUid',
      'LOGINEP_KONG_ADMINAPI_URL': 'http://kong:8001',
      'LOGINEP_SYNCACL': 'group1,group2,group3',
      'LOGINEP_JWT_TOKEN_TIMEOUT': '60'
    }
    with self.assertRaises(Exception) as context:
      gp = GlobalParamatersClass(env)
    self.checkGotRightException(context,getInvalidEnvVarParamaterException('LOGINEP_USER_ATTRIBUTE'))
