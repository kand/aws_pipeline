import sys

from util.uploader import AccessGrant,Uploader
from util.environment import *
from util.pipelineRunner import PipelineRunner

CONFIG_FILE = "../config"

def printUsage():
    readme = open("../README","r")
    print(readme.read())
    readme.close()

if __name__ == "__main__":
    arglen = len(sys.argv)
    if arglen < 2:
        printUsage()
    elif sys.argv[1] == "set" and arglen == 4:
        if not envSet(CONFIG_FILE,sys.argv[2],sys.argv[3]):
            print("variable '" + sys.argv[2] + "' not found")
        else:
            print("variable '" + sys.argv[2] + "' set to '" + sys.argv[3] + "'")
    elif sys.argv[1] == "get" and arglen == 3:
        val = envGet(CONFIG_FILE,sys.argv[2])
        if val is None:
            print("variable '" + sys.argv[2] + "' not found")
        else:
            print("variable '" + sys.argv[2] + "' = '" + val + "'")
    elif sys.argv[1] == "run" and arglen >= 3:
        print("Running pipeline...")
        print("")
        pipe = PipelineRunner(sys.argv[2])
        if (arglen == 4 and not pipe.runPipeline(int(sys.argv[3]))) or not pipe.runPipeline():
            print("")
            print("Pipeline did not complete successfully.")
        else:
            print("")
            print("Pipeline completed successfully.")
    else:
        printUsage()