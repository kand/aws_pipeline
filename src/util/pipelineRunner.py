import sys

class PipelineRunner(object):
    
    def __init__(self,path,name):
        '''Handles running pipelines
            Inputs: 
                path = path to python script
                name = name of the BasePipeline class to run'''
        self.path = path
        self.name = name
    
    def loadPipeline(self):
        sys.path.append(self.path)
        return __import__(self.name)
    
    def runPipeline(self,startPoint=0):
        module = self.loadPipeline()
        pipeline = module.__getattribute__(self.name)()
        pipeline.run(startPoint) 
    
if __name__ == "__main__":
    #a = PipelineRunner("../pipelines/test_save_state/","test_save_state")
    #a.runPipeline()
    pass