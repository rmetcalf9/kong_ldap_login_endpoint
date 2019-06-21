import requests
import json

# Class to encapsulate all calls ot the kong admin API

class kongAdminAPIWrapperClass():
  appObj = None
  jwtTokenKey = 'kong_ldap_login_endpoint_jwtkey'
  def __init__(self, appObj):
    self.appObj = appObj

  def c_get(self,api,expected_responses):
    r = requests.get(self.appObj.globalParamObject.LOGINEP_KONG_ADMINAPI_URL + api)
    if r.status_code in expected_responses:
      return r
    raise Exception('Unexpected response from get:' + api + ' (' + str(r.status_code) + ')')
  def c_delete(self,api,expected_responses):
    r = requests.delete(self.appObj.globalParamObject.LOGINEP_KONG_ADMINAPI_URL + api)
    if r.status_code in expected_responses:
      return r
    raise Exception('Unexpected response from delete:' + api + ' (' + str(r.status_code) + ')')
  def c_put(self,api, msgData,expected_responses):
    r = requests.put(self.appObj.globalParamObject.LOGINEP_KONG_ADMINAPI_URL + api, data=json.dumps(msgData), headers={'content-type': 'application/json'})
    if r.status_code in expected_responses:
      return r
  def c_post(self,api, msgData,expected_responses):
    r = requests.post(self.appObj.globalParamObject.LOGINEP_KONG_ADMINAPI_URL + api, data=json.dumps(msgData), headers={'content-type': 'application/json'})
    if r.status_code in expected_responses:
      return r
    raise Exception('Unexpected response from post:' + api + ' (' + str(r.status_code) + ')')

  def consumerExists(self,username):
    r = self.c_get('/consumers/' + username, [404, 200])
    if r.status_code == 404:
      return (False, '')
    #must be 200 as the get funciton will except if anything other than 404 or 200 is returned
    resultJSON = json.loads(r.text)
    return (True, resultJSON['id'])
  def createConsumer(self,username):
    r = self.c_put('/consumers/' + username, {}, [200, 201])
    resultJSON = json.loads(r.text)
    return resultJSON['id']

  def getACLListForConsumer(self,username):
    grps = self.fetchGroups('/consumers/' + username + '/acls', [])
    return grps

  def fetchGroups(self, url, groups):
    r = self.c_get(url, [200])
    resultJSON = json.loads(r.text)

    mergedlist = []
    mergedlist.extend(groups)
    mergedlist.extend(self.addGroups(resultJSON['data']))

    if resultJSON['next']:
      mergedlist = self.fetchGroups(resultJSON['next'], mergedlist)

    return mergedlist

  def addGroups(self, groups):
    grps = []
    for grp in range(len(groups)):
      grps.append(groups[grp]["group"])
    return grps

  def removeacl(self,username,acl):
    r = self.c_delete('/consumers/' + username + '/acls/' + acl, [204])
  def addacl(self,username,acl):
    msgData = { 'group': acl }
    r = self.c_post('/consumers/' + username + '/acls',msgData, [200, 201])
  
  def ensureUserExistsWithACL(self,username, aclList):
    conExists, consumerID = self.consumerExists(username)
    if not conExists:
      consumerID = self.createConsumer(username)
    cur_acls = self.getACLListForConsumer(username)

    # Remove all acls not in list
    for acl in cur_acls:
      if acl not in aclList:
        self.removeacl(username,acl)
    # Add acls not already there
    for acl in aclList:
      if acl not in cur_acls:
        self.addacl(username,acl)

  def getJWTToken(self, username):
    r = self.c_get('/consumers/' + username + '/jwt/' + username + '_' + self.jwtTokenKey, [200, 404])
    if r.status_code == 200:
      resultJSON = json.loads(r.text)
      return resultJSON
    # jwt credential dosen't exist - create if
    msgData = { 'key': username + '_' + self.jwtTokenKey }
    r = self.c_post('/consumers/' + username + '/jwt/',msgData, [201])
    resultJSON = json.loads(r.text)
    return resultJSON
