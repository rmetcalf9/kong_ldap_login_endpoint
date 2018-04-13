import requests
import json

# Class to encapsulate all calls ot the kong admin API

class kongAdminAPIWrapperClass():
  appObj = None
  def __init__(self, appObj):
    self.appObj = appObj

  def c_get(self,api):
    return requests.get(self.appObj.globalParamObject.LOGINEP_KONG_ADMINAPI_URL + api)
  def c_put(self,api, msgData):
    return requests.put(self.appObj.globalParamObject.LOGINEP_KONG_ADMINAPI_URL + api, data=json.dumps(msgData), headers={'content-type': 'application/json'})

  def consumerExists(self,username):
    r = self.c_get('/consumers/' + username)
    if r.status_code == 404:
      return False
    if r.status_code == 200:
      return True
    raise Exception('Unexpected response from Kong')
  def createConsumer(self,username):
    msgData = { 'username': username }
    r = self.c_put('/consumers/',msgData)
    if r.status_code == 201:
      return
    raise Exception('Unexpected response from Kong consumer Put ' + str(r.status_code))
  def getACL(self,username):
    raise Exception('getACL Not Implemented')
  def removeacl(self,username):
    raise Exception('removeacl Not Implemented')
  def addacl(self,username):
    raise Exception('addacl Not Implemented')
  
  def ensureUserExistsWithACL(self,username, aclList):
    if not self.consumerExists(username):
      self.createConsumer(username)
    
    cur_acls = getACL(username)

    # Remove all acls not in list
    for acl in cur_acls:
      if acl not in aclList:
        self.removeacl(username,acl)
    # Add acls not already there
    for acl in aclList:
      if acl not in cur_acls:
        self.addacl(username,acl)
