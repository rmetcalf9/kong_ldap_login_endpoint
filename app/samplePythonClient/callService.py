import argparse
import getpass
import time
import sys
from kongLdapJWTSecuredService import kongLdapJWTSecuredServiceClass

def serviceReturnOK(request):
  if request.status_code < 200:
    return False
  if request.status_code > 299:
    return False
  return True

print("Sample client for kong_ldap_login_endpoint")

parser = argparse.ArgumentParser(description='Test login service')
parser.add_argument('loginEP', help='Login Endpoint')
parser.add_argument('serviceEP', help='Service Endpoint')

args = parser.parse_args()

continous = False
stopOnException = True

ldapUsername = input("Please enter your LDAP username: ")
ldapPassword = getpass.getpass(prompt="Please enter your password: ")
continousSTR = input("Continous run (N): ")
if len(continousSTR)>0:
  continousSTR = continousSTR[0].upper()
  if continousSTR == 'Y':
    continous = True
if continous:
  stopOnExceptionSTR = input("Halt on Exception? (Y): ")
  if len(stopOnExceptionSTR)>0:
    stopOnExceptionSTR = stopOnExceptionSTR[0].upper()
    if stopOnExceptionSTR == 'N':
      stopOnException = False

serv = kongLdapJWTSecuredServiceClass(args.loginEP, ldapUsername, ldapPassword)

callnum = 0
running = True
while running:
  callnum = callnum + 1
  print("%03d" % (callnum,), end='')
  print(". Now calling service...", end='')
  serviceResult = serv.get(args.serviceEP, True)
  sys.stdout.flush()
  if not serviceReturnOK(serviceResult):
    print("\nEXCEPTION!!!\n")
    print(serviceResult.text)
    if stopOnException:
      raise Exception("Service call Failed with status " + str(serviceResult.status_code))

  print('sucessful:', end='')
  print(serviceResult.text, end='')
  sys.stdout.flush()
  
  if not continous:
    running = False
  else:
    time.sleep(1) #sleep for one second before trying again
    print("")

print("\nComplete\n")

