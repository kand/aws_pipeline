import os,sys

from util.uploader import AccessGrant,Uploader
from util.environment import Environment
from util.pipelineRunner import PipelineRunner

CONFIG_FILE = os.path.join(os.path.split(os.path.abspath(__file__))[0],
                           "../config")

def printUsage():
    readme = open("../README","r")
    print(readme.read())
    readme.close()

if __name__ == "__main__":
    env = Environment()
    env.load(CONFIG_FILE)
    arglen = len(sys.argv)
    if arglen < 2:
        printUsage()
    elif sys.argv[1] == "set" and arglen == 4:
        if not env.set(sys.argv[2],sys.argv[3]):
            print("variable '" + sys.argv[2] + "' not found")
        else:
            print("variable '" + sys.argv[2] + "' set to '" + sys.argv[3] + "'")
    elif sys.argv[1] == "get" and arglen == 3:
        val = env.get(sys.argv[2])
        if val is None:
            print("variable '" + sys.argv[2] + "' not found")
        else:
            print("'" + sys.argv[2] + "' = '" + val + "'")
    elif sys.argv[1] == "run" and arglen >= 3:
        print("Running pipeline...")
        print("")
        pipe = PipelineRunner(sys.argv[2])
        addArgs = []
        if arglen >= 5 and sys.argv[3] == "-s":
            for i in range(5,len(sys.argv)):
                addArgs.append(sys.argv[i])
            pipe.runPipeline(int(sys.argv[4]),addArgs=addArgs)
        else:
            for i in range(3,len(sys.argv)):
                addArgs.append(sys.argv[i])
            pipe.runPipeline(addArgs=addArgs)
        print("Pipeline complete.")
    else:
        printUsage()
    env.save()
