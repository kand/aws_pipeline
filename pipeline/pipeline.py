import sys

from pipelines.pipelineRunner import PipelineRunner
from util.uploader import AccessGrant,Uploader
from util.environment import Environment
from util.misc import getDir,getPath

THIS_DIR = getDir(__file__)
CONFIG_FILE = getPath(__file__,"config")
USAGE_FILE = getPath(__file__,"usage")

def printUsage():
    readme = open(USAGE_FILE,"r")
    print(readme.read())
    readme.close()

def start(sys_args):
    '''Start pipeline with sys_args'''
    env = Environment()
    env.load(CONFIG_FILE)
    arglen = len(sys_args)
    if arglen < 2:
        printUsage()
        
    elif sys_args[1] == "set" and arglen == 4:
        if not env.set(sys_args[2],sys_args[3]):
            print("variable '" + sys_args[2] + "' not found")
        else:
            print("variable '" + sys_args[2] + "' set to '" + sys_args[3] + "'")
            
    elif sys_args[1] == "get" and arglen == 3:
        val = env.get(sys_args[2])
        if val is None:
            print("variable '" + sys_args[2] + "' not found")
        else:
            print("'" + sys_args[2] + "' = '" + val + "'")
            
    elif sys_args[1] == "run" and arglen >= 3:
        print("Running pipeline...")
        print("")
        pipe = PipelineRunner(sys_args[2])
        addArgs = []
        if arglen >= 5 and sys_args[3] == "-s":
            for i in range(5,len(sys_args)):
                addArgs.append(sys_args[i])
            pipe.runPipeline(int(sys_args[4]),addArgs=addArgs)
        else:
            for i in range(3,len(sys_args)):
                addArgs.append(sys_args[i])
            pipe.runPipeline(addArgs=addArgs)
        print("Pipeline complete.")
    else:
        printUsage()
    env.save()

if __name__ == "__main__":
    start(sys.argv)
    