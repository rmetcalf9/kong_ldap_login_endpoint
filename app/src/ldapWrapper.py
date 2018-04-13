import ldap


class ldapClass():
  appObj = None
  def __init__(self, appObj):
    self.appObj = appObj

  def isUserInGroup(self,username,curGroup,ldap_connection):
    ldapStr = self.appObj.globalParamObject.LOGINEP_GROUP_ATTRIBUTE + "=" + curGroup + "," + self.appObj.globalParamObject.LOGINEP_GROUP_BASE_DN
    print(ldapStr)
    ldap_result_id = ldap_connection.search(ldapStr, ldap.SCOPE_SUBTREE, None, [self.appObj.globalParamObject.LOGINEP_GROUP_MEMBER_FIELD])
    result_set = []
    while 1:
      try:
        result_type, result_data = ldap_connection.result(ldap_result_id, 0)
      except ldap.NO_SUCH_OBJECT:
        return False
      if (result_data == []):
        break
      else:
        if result_type == ldap.RES_SEARCH_ENTRY:
          result_set.append(result_data)
    print(result_set)

    #TODO Determine if this user is a member of this group
    return True

  falseReturn = { 'Authed': False, 'Groups': []}
  def verifyCredentials(self,username,password):
    if username is None:
      return self.falseReturn
    if password is None:
      return self.falseReturn
    username = username.strip()
    password = password.strip()
    if username == "":
      return self.falseReturn
    if password == "":
      return self.falseReturn

    ldap_connection = ldap.initialize("ldaps://" + self.appObj.globalParamObject.LOGINEP_LDAP_HOST + ":" + self.appObj.globalParamObject.LOGINEP_LDAP_PORT)
    ldap_connection.protocol_version = ldap.VERSION3
    try:
      ldap_connection.simple_bind_s(self.appObj.globalParamObject.LOGINEP_USER_ATTRIBUTE + "=" + username + "," + self.appObj.globalParamObject.LOGINEP_USER_BASE_DN, password)
    except ldap.INVALID_CREDENTIALS:
      return self.falseReturn

    # User is authed. Now go through all whitelisted groups and verify which they are members of
    groups = []
    for curGroup in self.appObj.globalParamObject.LOGINEP_SYNCACL.split(','):
      curGroup = curGroup.strip()
      try:
        if self.isUserInGroup(username,curGroup,ldap_connection):
          groups.append(curGroup)
      except:
        print('Error querying for group ' + curGroup)
        raise

    return { 'Authed': True, 'Groups': groups}
