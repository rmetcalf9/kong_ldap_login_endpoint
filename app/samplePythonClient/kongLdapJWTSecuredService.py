
import requests
from requests.auth import _basic_auth_str
import json

class kongLdapJWTSecuredServiceClass:
  loginurl = None
  username = None
  password = None
  securityToken = None

  def __init__(self, loginurl, username, password):
    self.loginurl = loginurl
    self.username = username
    self.password = password

  def _getSecurityToken(self, output):
    loginResult = requests.get(self.loginurl, headers={'Authorization': _basic_auth_str(self.username, self.password)})
    if loginResult.status_code != 200:
      print(loginResult.text)
      raise Exception("Login Failed with status " + str(loginResult.status_code))
    loginResultJSON = json.loads(loginResult.text)
    if 'JWTToken' not in loginResultJSON:
      raise Exception('Login response missing JWTToken')
    self.securityToken = loginResultJSON
    if output:
      print("Recieved the token: " + self.securityToken['JWTToken'])
      print("It will expire: " + self.securityToken['TokenExpiry'])
      print("\n")
    return

  def get(self, url, output):
    if self.securityToken is None:
      self._getSecurityToken(output)
    result = requests.get(url, headers={'Authorization': 'Bearer ' + self.securityToken['JWTToken']})
    if result.status_code == 401:
      # token might have expired - retry
      if output:
        print("Token may have expired trying to get a new one...", end='')
      self._getSecurityToken(output)
      result = requests.get(url, headers={'Authorization': 'Bearer ' + self.securityToken['JWTToken']})
    return result
