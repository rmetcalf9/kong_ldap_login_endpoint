from appObj import appObj
import os
import sys

appObj.init(os.environ)

expectedNumberOfParams = 0
if ((len(sys.argv)-1) != expectedNumberOfParams):
  raise Exception('Wrong number of paramaters passed (Got ' + str((len(sys.argv)-1)) + " expected " + str(expectedNumberOfParams) + ")")

appObj.run()
