from TestHelperSuperClass import testHelperAPIClient
from base64 import b64encode

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

  def test_loginBadCredentials(self):
    username = 'TestBadUser'
    password = 'TestBadPassword'
    result = self.testClient.get('/login/',headers={'Authorization': _basic_auth_str('Basic ', username, password)})
    self.assertEqual(result.status_code, 401)

  def test_loginGiid(self):
    username = 'TestUser'
    password = 'TestPassword'
    result = self.testClient.get('/login/',headers={'Authorization': _basic_auth_str('Basic ', username, password)})
    self.assertEqual(result.status_code, 500)
