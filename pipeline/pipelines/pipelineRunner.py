import sys,os

from pipeline.util.ec2 import ec2

class PipelineRunner(object):
    
    def __init__(self,path):
        '''Handles running pipelines. Pipeline classes must have the same file
            and class name.
            Inputs: 
                path = path to python pipeline script'''
        psplit = os.path.split(path)
        self.path = psplit[0]
        self.name = psplit[1].replace(".py","")
    
    def loadPipeline(self):
        '''Load the pipeline'''
        sys.path.append(self.path)
        return __import__(self.name)
    
    # TODO : there is no way to set start point to something other than the start
    #    and inject results from a previous stage. For example, if pipeline crashed
    #    in stage 2, still would have stage 1 results, but can't give these results
    #    to stage 2 and start from there
    def runPipeline(self,startPoint=0,addArgs=[]):
        '''Run the pipeline. Returns True if pipeline completed successfully.'''
        module = self.loadPipeline()
        pipeline = module.__getattribute__(self.name)(addArgs)
        return pipeline.run(startPoint)
    
if __name__ == "__main__":
    pass