import sys

from util.uploader import AccessGrant,Uploader
from util.environment import *

CONFIG_FILE = "../config"

def printUsage():
    readme = open("../README","r")
    print(readme.read())
    readme.close()

if __name__ == "__main__":
    arglen = len(sys.argv)
    if arglen < 2:
        printUsage()
    elif sys.argv[1] == "set":
        if arglen < 4:
            printUsage()
        else:
            if not envSet(CONFIG_FILE,sys.argv[2],sys.argv[3]):
                print("variable '" + sys.argv[2] + "' not found")
            else:
                print("variable '" + sys.argv[2] + "' set to '" + sys.argv[3] + "'")
    else:
        printUsage()