import ldap
from ast import literal_eval

class ldapClass():
  appObj = None
  def __init__(self, appObj):
    self.appObj = appObj

  def isUserInGroup(self,username,curGroup,ldap_connection):
    ldapStr = self.appObj.globalParamObject.LOGINEP_GROUP_ATTRIBUTE + "=" + curGroup + "," + self.appObj.globalParamObject.LOGINEP_GROUP_BASE_DN
    ldap_result_id = ldap_connection.search(ldapStr, ldap.SCOPE_SUBTREE, None, [self.appObj.globalParamObject.LOGINEP_GROUP_MEMBER_FIELD])
    result_set = []
    numRes = 0
    while 1:
      numRes = numRes + 1
      if numRes > 9999:
        raise Exception('LDAP query returned to many results')
      try:
        result_type, result_data = ldap_connection.result(ldap_result_id, 0)
      except ldap.NO_SUCH_OBJECT:
        return False
      if (result_data == []):
        break
      else:
        if result_type == ldap.RES_SEARCH_ENTRY:
          result_set.append(result_data)
    if len(result_set) != 1:
      raise Exception('LDAP query returned result set size of ' + len(result_set) + ' expected 1')

    #Verify Group Membership
    tuple = literal_eval(str(result_set[0][0]))
    if len(tuple) != 2:
      raise Exception('Did not understand group query result ' + result_set[0][0])
    for curMember in tuple[1][self.appObj.globalParamObject.LOGINEP_GROUP_MEMBER_FIELD]:
      if curMember.decode("utf-8")==username:
        return True

    #did not find them in the group
    return False

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
    ldap.OPT_NETWORK_TIMEOUT = self.appObj.globalParamObject.LOGINEP_LDAP_TIMEOUT
    try:
      ldap_connection.simple_bind_s(self.appObj.globalParamObject.LOGINEP_USER_ATTRIBUTE + "=" + username + "," + self.appObj.globalParamObject.LOGINEP_USER_BASE_DN, password)
    except ldap.INVALID_CREDENTIALS:
      return self.falseReturn

    groups = []
    if self.appObj.globalParamObject.LOGINEP_SYNCACL is None:
      return { 'Authed': True, 'Groups': groups}
    if self.appObj.globalParamObject.LOGINEP_SYNCACL == '':
      return { 'Authed': True, 'Groups': groups}

    # User is authed. Now go through all whitelisted groups and verify which they are members of
    for curGroup in self.appObj.globalParamObject.LOGINEP_SYNCACL.split(','):
      curGroup = curGroup.strip()
      try:
        if self.isUserInGroup(username,curGroup,ldap_connection):
          groups.append(curGroup)
      except:
        print('Error querying for group ' + curGroup)
        raise

    return { 'Authed': True, 'Groups': groups}
