import sys,os

sys.path.append("/media/files/docs/research/pipeline/src/")
from pipelines.basePipeline import RunOrderFunction,BasePipeline

class test_save_state(BasePipeline):
    
    def __init__(self,addArgs=[]):
        BasePipeline.__init__(self)
        
        for i in range(0,len(addArgs)):
            print("Got arg: " + addArgs[i])
        
        self.RUN_ORDER = [RunOrderFunction(self.stage1),
                          RunOrderFunction(self.stage2,50),
                          RunOrderFunction(self.stage3)]
        
        self.dir = os.path.split(os.path.abspath(__file__))[0]
        self.name = "test_save_state"
        
    def handleOutput(self,pout,perr):
        if len(pout) > 0: print("[OUT]" + pout)
        if len(perr) > 0: print("[ERR]" + perr)
        
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
