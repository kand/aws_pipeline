
class RunOrderFunction():
    '''A funciton to put into RUN_ORDER collection.'''
    
    def __init__(self,func,*args,**kwargs):
        self.func = func
        self.args = args
        self.kwargs = kwargs
        
    def __call__(self):
        return self.func(*self.args,**self.kwargs)

class BasePipeline(object):
    '''Base for all other python pipeline scripts.'''
    
    def __init__(self):
        self.RUN_ORDER = [] # ordered list of functions to run
    
    def run(self,startPoint=0):
        '''Run RUN_ORDER functions from startPoint'''
        for i in range(startPoint,len(self.RUN_ORDER)):
            self.RUN_ORDER[i]()
            
if __name__ == "__main__":
    pass