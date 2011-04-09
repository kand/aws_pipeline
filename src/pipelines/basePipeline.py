import subprocess,os

from util.environment import Environment
from util.uploader import AccessGrant,Uploader

class RunOrderFunction():
    '''A funciton to put into RUN_ORDER collection.'''
    
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
    
    def __init__(self):
        self.RUN_ORDER = []     # ordered list of functions to run
        self.outputDir = None   # pipeline output directory
        self.logPath = None     # path to log file
        self.logFile = None     # log file object
        self.env = Environment()# environment variables
        self.name = None        # name of pipeline
        self.result = None      # stores result from last RUN_ORDER function call
    
    def construct(self):
        '''Construct pipeline parameters based on set variables. Called before
            pipeline is run. Override to use own parameters.'''
        # TODO : figure out bucket name and s3Filename, not sure that I want 
        #    to do this here, since what if the pipeline is going to use 
        #    something that's not s3, or ec2?
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
            f = open(os.path.join(self.outputDir,self.name + "_results_" + str(i)),"w")
            f.write(str(self.result))
            f.close()
        
        print("log at:'" + self.logPath + "'")
        self.logFile.close()
    
    def execScript(self,script):
        '''Run a shell script and log its output to self.log'''
        command = ["chmod","+x",script]
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        pout,perr = process.communicate()
        self.logFile.write(perr)
        self.logFile.write(pout)

        command = ["sudo",script]
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        pout,perr = process.communicate()
        self.logFile.write(perr)
        self.logFile.write(pout)
            
if __name__ == "__main__":
    pass
