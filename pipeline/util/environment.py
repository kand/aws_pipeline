import re

from util.misc import getPath

CONFIG_FILE = getPath(__file__,'../config')

class _Environment(object):
    '''Class that stores/loads/saves environment variables in the config file.'''
    
    def __init__(self):
        self.vars = {}
        self.loaded = False
        self.load()
        
    def load(self,fileName=CONFIG_FILE):
        '''Load environment variables from specified config file.'''
        
        self.configFile = fileName
        self.vars = {}
        
        f = open(fileName,"r")
        matches = re.finditer(r"(?P<key>\w+)=(?P<val>.*)\n?",f.read())
        f.close()

        for m in matches:
            self.vars[m.group("key")] = m.group("val")
        
        self.loaded = True
        
    def getVarList(self):
        '''Get a list of environment variables'''
        if not self.loaded:
            raise Exception('Environment must be loaded before calling getVarList')
        return self.vars.keys()
            
    def set(self,name,value):
        '''Set the value of an environment variable.'''
        if not self.loaded:
            raise Exception('Environment must be loaded before calling set')
        
        if name not in self.vars.keys():
            return False
        self.vars[name] = value
        return True
            
    def get(self,name):
        '''Get the value of an environment variable.'''
        if not self.loaded:
            raise Exception('Environment must be loaded before calling get')
        
        if name not in self.vars.keys():
            print('Error: name provided does not exist in the environment')
            return None
            
        return self.vars[name]
    
    def showAll(self):
        '''Display all environment vairables.'''
        if not self.loaded:
            raise Exception('Environment must be loaded before calling showAll')
    
        for k in self.vars.keys():
            print('%s \t %s' % (k,self.vars[k]))
    
    def save(self):
        '''Save environment variables to config file.'''
        if not self.loaded:
            raise Exception('Environment must be loaded before calling save')
        
        f = open(self.configFile,"w")
        for k in self.vars:
            f.write(k + "=" + self.vars[k] + "\n")
        f.close()

_environment = _Environment()

def Environment(): return _environment
