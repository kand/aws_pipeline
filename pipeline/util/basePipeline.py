import subprocess,os

from util.environment import Environment

class RunOrderFunction():
    '''A function to put into RUN_ORDER collection.'''
    
    def __init__(self,func,*args,**kwargs):
        '''Initialize function
            Inputs:
                func = function in pipeline to run
                args = arguments to func
                kwargs = keyword arguments to func'''

        self.func = func
        self.args = args
        self.kwargs = kwargs
        
    def __call__(self):
        '''Calls function with given arguments and keyword arguments.'''
        return self.func(*self.args,**self.kwargs)

class BasePipeline(object):
    '''Base for all other python pipeline scripts.'''
    
    def __init__(self,addArgs=[]):
        self.RUN_ORDER = []     # ordered list of functions to run
        
        self.outputDir = ""     # pipeline output directory
        self.logPath = ""       # path to log file
        self.logFile = None     # log file object
        self.env = Environment()# environment variables
        self.name = ""          # name of pipeline
        self.result = None      # stores result from last RUN_ORDER function call
    
    def handleOutput(self,pout,perr):
        '''Overridable function to handle shell script output.
            Inputs:
                pout = proccess out stream
                perr = process error stream'''
        pass
    
    def construct(self):
        '''Construct pipeline parameters based on set variables. Called before
            pipeline is run. Override to use own parameters.'''
        self.outputDir = self.name + "_results"
        if not os.path.isdir(self.outputDir):
            os.mkdir(self.outputDir)
            
        self.logPath = os.path.join(self.outputDir,self.name + "_log")
        self.logFile = open(self.logPath,"w")
    
    def run(self,startPoint=0):
        '''Run RUN_ORDER functions from startPoint.'''
        self.construct()
        
        for i in range(startPoint,len(self.RUN_ORDER)):
            self.result = self.RUN_ORDER[i]()
            
            path = os.path.join(self.outputDir,self.name + "_results_" + str(i))
            
            f = open(path,"w")
            f.write(str(self.result))
            f.close()
        
        print("log at:'" + self.logPath + "'")
        self.logFile.close()
    
    def execComm(self,commStr,handleOutFunc=None):
        '''Run a command line command and log its output to self.log
            Inputs:
                commStr = command exactly as you would enter it from 
                    command line
                handleOutFunc = function to be called to handle any output from
                    process, this function must take 2 inputs (outstring,errorstring)'''     
        command = commStr.split(" ")
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        pout,perr = process.communicate()
        
        if handleOutFunc is not None:
            handleOutFunc(pout,perr)
        else:
            self.handleOutput(pout,perr)
        
        self.logFile.write(perr)
        self.logFile.write(pout)
    
    def execScript(self,script,*args):
        '''Run a shell script and log its output to self.log
            Inputs:
                script = absolute path to script
                args = command line arguments to give script'''
        
        self.execComm("chmod +x %s" % script)    
        self.execComm("sudo %s %s" % (script," ".join(str(a) for a in args)),self.handleOutput)

if __name__ == "__main__":
    pass
