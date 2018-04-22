from TestHelperSuperClass import testHelperAPIClient, envWithNoGroups
from base64 import b64encode, b64decode
from unittest.mock import patch, call
import ldap
import json
from appObj import appObj
import jwt


from requests._internal_utils import to_native_string
def _basic_auth_str(prefix, username, password):
    if isinstance(username, str):
        username = username.encode('latin1')

    if isinstance(password, str):
        password = password.encode('latin1')

    authstr = prefix + to_native_string(
        b64encode(b':'.join((username, password))).strip()
    )

    return authstr

class okrequestresp():
  status_code = 200
  text = ''
  def __init__(self, text):
    self.text = text


class test_loginAPI(testHelperAPIClient):
  def test_healthcheck(self):
    result = self.testClient.get('/login/healthy')
    self.assertEqual(result.status_code, 200)

  def test_loginNoAuthCredentials(self):
    result = self.testClient.get('/login/')
    self.assertEqual(result.status_code, 400)

  def test_loginBadAuthHeader(self):
    result = self.testClient.get('/login/',headers={'Authorization': 'BadAuthHeader'})
    self.assertEqual(result.status_code, 400)

  def test_loginAuthNotBase64(self):
    username = 'TestUser'
    password = 'TestPassword'
    combined = username + ':' + password
    result = self.testClient.get('/login/',headers={'Authorization': 'Basic ' + combined})
    self.assertEqual(result.status_code, 400)

  @patch('ldap.ldapobject.SimpleLDAPObject.simple_bind_s', return_value=None, side_effect=ldap.INVALID_CREDENTIALS)
  def test_loginBadCredentials(self, x):
    username = 'TestBadUser'
    password = 'TestBadPassword'
    result = self.testClient.get('/login/',headers={'Authorization': _basic_auth_str('Basic ', username, password)})
    self.assertEqual(result.status_code, 401)

  @patch('ldap.ldapobject.SimpleLDAPObject.simple_bind_s', return_value=None)
  @patch('ldap.ldapobject.SimpleLDAPObject.search', return_value=123)
  @patch('ldap.ldapobject.SimpleLDAPObject.result', side_effect=[
    (ldap.RES_SEARCH_ENTRY, ["('cn=group1,ou=Group,ou=everyone,dc=somehost,dc=com', {'memberUid': [b'TestUser', b'TestUser2', b'TestUser3']})"]),
    (ldap.RES_SEARCH_ENTRY, []),
    (ldap.RES_SEARCH_ENTRY, ["('cn=group2,ou=Group,ou=everyone,dc=somehost,dc=com', {'memberUid': [b'TestUser', b'TestUser2', b'TestUser3']})"]),
    (ldap.RES_SEARCH_ENTRY, []),
    (ldap.RES_SEARCH_ENTRY, ["('cn=group3,ou=Group,ou=everyone,dc=somehost,dc=com', {'memberUid': [b'TestUser', b'TestUser2', b'TestUser3']})"]),
    (ldap.RES_SEARCH_ENTRY, [])
  ])
  @patch('requests.get', side_effect=[
    okrequestresp(text='{"id": "123"}'), #get consumer
    okrequestresp(text='{"data": []}'),  #get consumer acl list
    okrequestresp(text='{"key": "some_key", "secret": "some_secretxx"}')   #get consumer jwt token
  ])
  @patch('requests.put', side_effect=[
    okrequestresp(text='{"id": "123"}'), #try and insert group1
    okrequestresp(text='{"id": "123"}'), #try and insert group2
    okrequestresp(text='{"id": "123"}') #try and insert group3
  ])
  def test_loginGoodConsumerPresent(self, x1, x2, mockResult, mockRequestsGet, mockRequestsPut):
    username = 'TestUser'
    password = 'TestPassword'
    result = self.testClient.get('/login/',headers={'Authorization': _basic_auth_str('Basic ', username, password)})
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    print(resultJSON['JWTToken'])
    self.assertNotEqual(resultJSON['JWTToken'],'')

  @patch('ldap.ldapobject.SimpleLDAPObject.simple_bind_s', return_value=None)
  @patch('requests.get', side_effect=[
    okrequestresp(text='{"id": "123"}'), #get consumer
    okrequestresp(text='{"data": []}'),  #get consumer acl list
    okrequestresp(text='{"key": "some_key", "secret": "some_secretxx"}')   #get consumer jwt token
  ])
  def test_loginGoodConsumerNoGroupsPresent(self, mockLdapSimpleBind, mockKongGet):
    appObj.init(envWithNoGroups, testingMode = True)
    self.testClient = appObj.flaskAppObject.test_client()
    self.testClient.testing = True 

    username = 'TestUser'
    password = 'TestPassword'
    result = self.testClient.get('/login/',headers={'Authorization': _basic_auth_str('Basic ', username, password)})
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    #print(resultJSON['JWTToken'])
    #print(resultJSON['TokenExpiry'])
    self.assertNotEqual(resultJSON['JWTToken'],'')
    decoded = jwt.decode(resultJSON['JWTToken'], b64decode("some_secretxx"), algorithms=['HS256'])
    self.assertEqual(decoded['iss'],"some_key")
    self.assertEqual(decoded['groups'],[])
    self.assertEqual(decoded['username'],username)

  @patch('ldap.ldapobject.SimpleLDAPObject.simple_bind_s', return_value=None)
  @patch('requests.get', side_effect=[
    okrequestresp(text='{"id": "123"}'), #get consumer
    okrequestresp(text='{"data": []}'),  #get consumer acl list
    okrequestresp(text='{"key": "some_key", "secret": "some_secretxx"}'),   #get consumer jwt token
    okrequestresp(text='{"id": "123"}'), #get consumer
    okrequestresp(text='{"data": []}'),  #get consumer acl list
    okrequestresp(text='{"key": "some_key", "secret": "some_secretxx"}')   #get consumer jwt token
  ])
  def test_loginTwoConsumersLoginNoGroupsPresent(self, mockKongGet, mockLdapSimpleBind):
    appObj.init(envWithNoGroups, testingMode = True)
    self.testClient = appObj.flaskAppObject.test_client()
    self.testClient.testing = True 

    username = 'TestUser001'
    password = 'TestPassword'
    result = self.testClient.get('/login/',headers={'Authorization': _basic_auth_str('Basic ', username, password)})
    self.assertEqual(result.status_code, 200)
    resultJSON = json.loads(result.get_data(as_text=True))
    #print(resultJSON['JWTToken'])
    #print(resultJSON['TokenExpiry'])
    self.assertNotEqual(resultJSON['JWTToken'],'')
    decoded = jwt.decode(resultJSON['JWTToken'], b64decode("some_secretxx"), algorithms=['HS256'])
    self.assertEqual(decoded['iss'],"some_key")
    self.assertEqual(decoded['groups'],[])
    self.assertEqual(decoded['username'],username)

    #Now log in as a second user
    username2 = 'TestUser002'
    password2 = 'TestPassword'
    result = self.testClient.get('/login/',headers={'Authorization': _basic_auth_str('Basic ', username2, password2)})
    self.assertEqual(result.status_code, 200)

    get_expected_calls = [
      call('http://kong:8001/consumers/ldap_TestUser001'),
      call('http://kong:8001/consumers/ldap_TestUser001/acls'),
      call('http://kong:8001/consumers/ldap_TestUser001/jwt/ldap_TestUser001_kong_ldap_login_endpoint_jwtkey'),
      call('http://kong:8001/consumers/ldap_TestUser002'),
      call('http://kong:8001/consumers/ldap_TestUser002/acls'),
      call('http://kong:8001/consumers/ldap_TestUser002/jwt/ldap_TestUser002_kong_ldap_login_endpoint_jwtkey')
    ]
    mockKongGet.assert_has_calls(get_expected_calls)
