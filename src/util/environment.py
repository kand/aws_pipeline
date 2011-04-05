import re

def envSet(configFile,name,value):
    '''Find and set an environment variable in config file
        Inputs:
            configFile = path to configuration file
            name = name of a variable to change
            value = value of a variable to change
        Returns: True if variable successfully changed'''
    replaced = False
    
    def _valRep(match):
        return match.group(1) + "=" + value + "\n"
    
    f = open(configFile,"r")
    oldf = f.read()
    newf = re.sub(r"(" + name + r")=(.*)\n",_valRep,oldf)
    if oldf is not newf: replaced = True 
    f.close()
    f = open(configFile,"w")
    f.write(newf)
    f.close()
    
    return replaced

def envGet(configFile,name):
    '''Find an environment variable in config file
        Inputs:
            configFile = path to configuration file
            name = name of variable to get'''        
    f = open(configFile,"r")
    match = re.search(r"(" + name + r")=(.*)\n",f.read())
    f.close()
    if match is not None:
        return match.group(2)
    return None