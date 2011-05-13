import subprocess,sys,os,argparse

from util.environment import Environment

class BasePipeline(object):
    '''Base for all other python pipeline scripts.'''
    
    def __init__(self):
        self.RUN_ORDER = []     # ordered list of functions to run
        
        self.outputDir = ""     # pipeline output directory
        self.logPath = ""       # path to log file
        self.logFile = None     # log file object
        self.env = Environment()# environment variables
        self.name = ""          # name of pipeline
        self.desc = ""          # description of pipeline
        
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
    
    def run(self,startPoint=0,prev_result=None):
        '''Run RUN_ORDER functions from startPoint.
            Inputs:
                startPoint = stage to start at
                prev_result = result from previous stage to pass to start stage'''
        self.construct()
        
        for i in range(startPoint,len(self.RUN_ORDER)):
            if i == startPoint and prev_result is not None:
                self.result = self.RUN_ORDER[i](prev_result)
            else:
                self.result = self.RUN_ORDER[i](self.result)
            
            path = os.path.join(self.outputDir,self.name + "_results_" + str(i))
            
            f = open(path,"w")
            f.write(str(self.result))
            f.close()
        
        print("log at:'" + self.logPath + "'")
        self.logFile.close()
        
    def runFromCommandLine(self):
        '''This should be placed at the footer of the pipeline after an if 
            __name__ == "__main__" so that the pipeline can be called from 
            the command line'''
        parser = argparse.ArgumentParser(prog=self.name,
                                         description=self.desc)
        parser.add_argument('-s','--start_at',metavar=('s'),type=int,
                            choices=range(0,len(self.RUN_ORDER)),
                            help='set a start point (s) to begin running pipeline at')
        parser.add_argument('pipeline_argument',nargs='*',
                            help='argument to pass to pipeline')
        
        vals = vars(parser.parse_args([sys.argv[i] for i in range(1,len(sys.argv))]))
        self.run(vals['start_at'],vals['pipeline_argument'])
    
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
        
        # TODO : need to flush err and out before next comm runs
        
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
