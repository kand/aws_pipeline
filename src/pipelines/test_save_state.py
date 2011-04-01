import subprocess

#from threading import Thread

class TestSaveState(object):
    
    SHELL_SCRIPT = "../../shell_scripts/test_save_state"
    
    def __init__(self):
        pass
    
    def run(self):
        print("Pipeline '" + self.SHELL_SCRIPT + "' starting..."),
        
        command = ["chmod","+x",self.SHELL_SCRIPT]
        process = subprocess.Popen(command)
        while process.poll() is None: pass
        
        command = ["sudo",self.SHELL_SCRIPT]
        process = subprocess.Popen(command,stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        
        while process.poll() is None:
            pout = process.stdout.read()
            perr = process.stderr.read()
            
            if pout == "save_state()":
                process.communicate("continue")
            
        print("Complete.")
    
if __name__ == "__main__":
    TestSaveState().run()