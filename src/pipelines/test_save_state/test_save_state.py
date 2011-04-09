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
                          RunOrderFunction(self.stage2,"arg1","arg2",keywarg="this is the kwarg"),
                          RunOrderFunction(self.stage3)]
        
        self.name = "test_save_state"
        
        self.uploader = Uploader(self.env.get("ACCESS_KEY"),self.env.get("SECRET_KEY"))
        self.bucketName = "test_bucket"
        self.s3FileName = "test_output"
        self.accessGrants = []
        self.metadata = {"Content-Type":"text/html"}
        
    def stage1(self):
        print("stage 1: doing stage 1 stuff")
        script = os.path.join(os.path.split(os.path.abspath(__file__))[0],
                              "test_save_state_1")

        self.execScript(script)
        
        print("script done. Uploading to s3...")
        
        print(self.uploader.upload(self.logPath,self.bucketName,
                                   self.s3FileName,self.accessGrants,
                                   self.metadata))
        
        print("done")
        
        return True
    
    def stage2(self,haz,args,keywarg="I'm a keyword arg"):
        print("stage 2: '" + haz + "' '" + args + "' '" + keywarg + "'")
        return True
    
    def stage3(self):
        print("stage 3: doing stage 3 stuff")
        return True
    
if __name__ == "__main__":
    pass
