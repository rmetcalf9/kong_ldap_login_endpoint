import ldap


class ldapClass():
  appObj = None
  def __init__(self, appObj):
    self.appObj = appObj

  def verifyCredentials(self,username,password):

    con = ldap.initialize("ldaps://" + self.appObj.globalParamObject.LOGINEP_LDAP_HOST + ":" + self.appObj.globalParamObject.LOGINEP_LDAP_PORT)
    try:
      con.simple_bind_s(self.appObj.globalParamObject.LOGINEP_USER_ATTRIBUTE + "=" + username + "," + self.appObj.globalParamObject.LOGINEP_USER_BASE_DN, password)
    except ldap.INVALID_CREDENTIALS:
      return False

    return True
