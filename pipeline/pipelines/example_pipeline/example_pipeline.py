import sys,os

# TODO : this doesn't seem like the best way to import necessary libraries...
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../.."))

from pipelines.basePipeline import BasePipeline
from util.misc import getPath

class example_pipeline(BasePipeline):
    '''This is an example pipeline'''
    
    def __init__(self):
        '''Needed to initialize pipeline'''
        
        #call base setup
        BasePipeline.__init__(self)
        
        #set the order of functions to run
        self.RUN_ORDER = [self.stage1,
                          self.stage2,
                          self.stage3]
        
        self.name = "pipeline_name"
        self.desc = "this is an example pipeline"
        
    def handleOutput(self,pout,perr):
        '''A custom definition for handleOutput, if you want to handle output
            in a way specific to this pipeline'''
        print('here is pout:{%s}' % pout)
        print('here is perr:{%s}' % perr)
        
    #define functions used in RUN_ORDER, each one of these needs:
    #    1. the def needs at least 1 argument, called prev_result here, so it
    #        can take in the result of the last function
    #    2. to return a value of some sort that will be passed to next stage
    
    def stage1(self,prev_result=None):
     	print(prev_result)
     	
        print("stage 1: doing stage 1 stuff")
        script = getPath(__file__,"example_script_1")

        self.execScript(script)
        
        return True
    
    def stage2(self,prev_result):
        print("stage 2 got: '" + str(prev_result) + "'")
        return True
    
    def stage3(self,prev_result):
        print("stage 3: doing stage 3 stuff")
        return True

# this section needs to be here to allow this script to be called directly from
#	the command line
if __name__ == "__main__":
    example_pipeline().runFromCommandLine()
    
