import subprocess,sys

sys.path.append("/media/files/docs/research/pipeline/src/pipelines/")
from basePipeline import RunOrderFunction,BasePipeline

class test_save_state(BasePipeline):
    
    def __init__(self):
        self.RUN_ORDER = [RunOrderFunction(self.stage1),
                          RunOrderFunction(self.stage2,"arg1","arg2",keywarg="this is the kwarg"),
                          RunOrderFunction(self.stage3)]
    
    #def run(self):
    #    print("Pipeline '" + self.SHELL_SCRIPT + "' starting..."),
    #    
    #    command = ["chmod","+x",self.SHELL_SCRIPT]
    #    process = subprocess.Popen(command)
    #    while process.poll() is None: pass
    #    
    #    command = ["sudo",self.SHELL_SCRIPT]
    #    process = subprocess.Popen(command,stdout=subprocess.PIPE,
    #                               stderr=subprocess.PIPE)
    #    
    #    while process.poll() is None:
    #        pout = process.stdout.read()
    #        perr = process.stderr.read()
    #        
    #        if pout == "save_state()":
    #            process.communicate("continue")
    #       
    #   print("Complete.")
        
    def stage1(self):
        print("stage 1: doing stage 1 stuff")
        return True
    
    def stage2(self,haz,args,keywarg="I'm a keyword arg"):
        print("stage 2: '" + haz + "' '" + args + "' '" + keywarg + "'")
        return True
    
    def stage3(self):
        print("stage 3: doing stage 3 stuff")
        return True
    
if __name__ == "__main__":
    pass