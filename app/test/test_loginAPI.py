from TestHelperSuperClass import testHelperAPIClient
from base64 import b64encode
from unittest.mock import patch
import ldap
import json

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