import sys,os

sys.path.append("/media/files/docs/research/pipeline/src/")
from pipelines.basePipeline import RunOrderFunction,BasePipeline
from util.uploader import AccessGrant,Uploader
from util.environment import Environment

# TODO : make this script take results from one function and modify in next

class test_save_state(BasePipeline):
    
    def __init__(self):
        BasePipeline.__init__(self)
        
        self.RUN_ORDER = [RunOrderFunction(self.stage1),
                          RunOrderFunction(self.stage2,50),
                          RunOrderFunction(self.stage3)]
        
        self.dir = os.path.split(os.path.abspath(__file__))[0]
        self.name = "test_save_state"
        
    def stage1(self):
        print("stage 1: doing stage 1 stuff")
        self.execScript(os.path.join(self.dir,"test_save_state_1"))
        return 10
    
    def stage2(self,maxCount):
        print("stage 2: counting from " + str(self.result) + " to " + str(maxCount))
        self.execScript(os.path.join(self.dir,"test_save_state_2"),self.result,maxCount)
        return maxCount
    
    def stage3(self):
        print("stage 3: doing stage 3 stuff")
        self.execScript(os.path.join(self.dir,"test_save_state_3"),self.result)
        return "Done"
    
if __name__ == "__main__":
    pass
