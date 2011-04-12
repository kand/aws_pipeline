import sys,os

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
    
    #TODO : start point isn't working
    def runPipeline(self,startPoint=0,addArgs=[]):
        '''Run the pipeline. Returns True if pipeline completed successfully.'''
        module = self.loadPipeline()
        pipeline = module.__getattribute__(self.name)(addArgs)
        return pipeline.run(startPoint) 
    
if __name__ == "__main__":
    pass