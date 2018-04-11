from TestHelperSuperClass import testHelperAPIClient

class test_loginAPI(testHelperAPIClient):
  def test_loginNoAuthCredentials(self):
    result = self.testClient.get('/login/')
    self.assertEqual(result.status_code, 400)

  def test_loginBadCredentials(self):
    result = self.testClient.get('/login/')
    self.assertEqual(result.status_code, 401)
