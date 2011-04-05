import re

def envSet(configFile,name,value):
    '''Find and set an environment variable in .config file
        Inputs:
            name = name of a variable to change
            value = value of a variable to change
        Returns: True if variable successfully changed'''
    
    replaced = False
    
    def _valRep(match):
        print(replaced)
        return match.group(1) + "=" + value + "\n"
    
    f = open(configFile,"r")
    newf = re.sub(r"(" + name + r")=(.*)\n",_valRep,f.read())
    f.close()
    f = open(configFile,"w")
    f.write(newf)
    f.close()
    
    return replaced
