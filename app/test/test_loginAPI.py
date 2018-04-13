from TestHelperSuperClass import testHelperAPIClient
from base64 import b64encode
from unittest.mock import patch
import ldap

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
  @patch('ldap.ldapobject.SimpleLDAPObject.search', return_value=123)
  @patch('ldap.ldapobject.SimpleLDAPObject.result', side_effect=[(ldap.RES_SEARCH_ENTRY, ["('cn=group1,ou=Group,ou=everyone,dc=somehost,dc=com', {'memberUid': [b'TestUser', b'TestUser2', b'TestUser3']})"]),(ldap.RES_SEARCH_ENTRY, [])])
  def test_loginGood(self, x1, x2, x3, mockResult):
    username = 'TestUser'
    password = 'TestPassword'
    result = self.testClient.get('/login/',headers={'Authorization': _basic_auth_str('Basic ', username, password)})
    self.assertEqual(result.status_code, 200)
    #TODO Check we have jwt token
