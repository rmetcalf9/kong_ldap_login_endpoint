import unittest
from appObj import appObj

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

class testHelperSuperClass(unittest.TestCase):
  def checkGotRightException(self, context, ExpectedException):
    if (context.exception != None):
      if (context.exception != ExpectedException):
        print("**** Wrong exception raised:")
        print("      expected: " + type(ExpectedException).__name__ + ' - ' + str(ExpectedException));
        print("           got: " + type(context.exception).__name__ + ' - ' + str(context.exception));
        raise context.exception
    self.assertTrue(ExpectedException == context.exception)


#helper class with setup for an APIClient
class testHelperAPIClient(testHelperSuperClass):
  testClient = None

  def setUp(self):
    # curDatetime = datetime.datetime.now(pytz.utc)
    # for testing always pretend the server started at a set datetime
    appObj.init(env, testingMode = True)
    self.testClient = appObj.flaskAppObject.test_client()
    self.testClient.testing = True 
  def tearDown(self):
    self.testClient = None