import argparse
import requests
from requests.auth import _basic_auth_str
import getpass
import json
import time
import sys

def serviceRetuenOK(request):
  if request.status_code < 200:
    return False
  if request.status_code > 299:
    return False
  return True
  
def callGetService(url, securityToken):
  return requests.get(url, headers={'Authorization': 'Bearer ' + securityToken['JWTToken']})

print("Sample client for kong_ldap_login_endpoint")

parser = argparse.ArgumentParser(description='Test login service')
parser.add_argument('loginEP', help='Login Endpoint')
parser.add_argument('serviceEP', help='Service Endpoint')

args = parser.parse_args()

continous = False

ldapUsername = input("Please enter your LDAP username: ")
ldapPassword = getpass.getpass(prompt="Please enter your password: ")
continousSTR = input("Continous run (N): ")
if len(continousSTR)>0:
  continousSTR = continousSTR[0].upper()
  if continousSTR == 'Y':
    continous = True

##loginResult = self.testClient.get(args.loginEP,headers={'Authorization': _basic_auth_str('Basic ', ldapUsername, ldapPassword)})

loginResult = requests.get(args.loginEP, headers={'Authorization': _basic_auth_str(ldapUsername, ldapPassword)})
if loginResult.status_code != 200:
  print(loginResult.text)
  raise Exception("Login Failed with status " + str(loginResult.status_code))

loginResultJSON = json.loads(loginResult.text)

print("Recieved the token: " + loginResultJSON['JWTToken'])
print("It will expire: " + loginResultJSON['TokenExpiry'])
print("\n")

callnum = 0
running = True
while running:
  callnum = callnum + 1
  print("%03d" % (callnum,), end='')
  print(". Now calling service...", end='')
  serviceResult = callGetService(args.serviceEP, loginResultJSON)
  sys.stdout.flush()
  if not serviceRetuenOK(serviceResult):
    print("\nEXCEPTION!!!\n")
    print(serviceResult.text)
    raise Exception("Service call Failed with status " + str(loginResult.status_code))

  print('sucessful:', end='')
  print(serviceResult.text, end='')
  sys.stdout.flush()
  
  if not continous:
    running = False
  else:
    time.sleep(1) #sleep for one second before trying again
    print("")

print("\nComplete\n")

