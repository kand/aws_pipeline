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
        
        self.outputDir = ""     # pipeline output directory
        self.logPath = ""       # path to log file
        self.logFile = None     # log file object
        self.env = Environment()# environment variables
        self.name = ""          # name of pipeline
        self.result = None      # stores result from last RUN_ORDER function call
        
        self.uploader = None    # file uploader
        self.bucketName = ""    # name of s3 bucket
        self.accessGrants = []  # access grant list for output
        self.metadata = {}
    
    def construct(self):
        '''Construct pipeline parameters based on set variables. Called before
            pipeline is run. Override to use own parameters.'''
        self.outputDir = self.name + "_results"
        if not os.path.isdir(self.outputDir):
            os.mkdir(self.outputDir)
            
        self.logPath = os.path.join(self.outputDir,self.name + "_log")
        self.logFile = open(self.logPath,"w")
        
        self.uploader = Uploader(self.env.get("ACCESS_KEY"),self.env.get("SECRET_KEY"))
        self.bucketName = self.name + "_results"
    
    def run(self,startPoint=0):
        '''Run RUN_ORDER functions from startPoint.'''
        self.construct()
        
        for i in range(startPoint,len(self.RUN_ORDER)):
            self.result = self.RUN_ORDER[i]()
            
            path = os.path.join(self.outputDir,self.name + "_results_" + str(i))
            
            f = open(path,"w")
            f.write(str(self.result))
            f.close()
            
            self.save(path)
        
        print("log at:'" + self.logPath + "'")
        self.logFile.close()
        
        self.save(self.logPath)
    
    #TODO : add a custom output processing function to execScript so pipelines
    #     can do custom output processing
    
    def handleOutput(self,pout,perr):
        '''Overriadable function to handle shell script output.
            Inputs:
                pout = proccess out stream
                perr = process error stream'''
        pass
    
    def execScript(self,script,*args):
        '''Run a shell script and log its output to self.log
            Inputs:
                script = absolute path to script
                args = command line arguments to give script'''
        command = ["chmod","+x",script]
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        pout,perr = process.communicate()
        
        self.logFile.write(perr)
        self.logFile.write(pout)

        command = ["sudo",script]
        for a in args:
            command.append(str(a))
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        pout,perr = process.communicate()
        
        self.handleOutput(pout,perr)
        
        self.logFile.write(perr)
        self.logFile.write(pout)
        
    def save(self,path):
        '''Saves file to s3.'''
        print("File saved on s3 at: " + 
              self.uploader.upload(path,self.bucketName,os.path.split(path)[1],
                                   self.accessGrants,self.metadata))

if __name__ == "__main__":
    pass
