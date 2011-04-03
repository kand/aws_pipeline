import subprocess

from basePipeline import RunOrderFunction,BasePipeline

class TestSaveState(BasePipeline):
    
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
        pass
    
    def stage2(self,haz,args,keywarg="I'm a keyword arg"):
        print("'" + haz + "' '" + args + "' '" + keywarg + "'")
        pass
    
    def stage3(self):
        pass
    
if __name__ == "__main__":
    TestSaveState().run()