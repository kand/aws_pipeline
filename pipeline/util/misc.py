import os

def getDir(file):
    '''Get the directory that a script is contained in. File should be the
        __file__ variable.'''
    return os.path.split(os.path.abspath(file))[0]

def getPath(file,relPath):
    '''Get the path of a file relative to the directory a script is contained
        in. file should be the __file__ variable. relPath should be the path
        of said file relative to script.'''
    return os.path.join(getDir(file),relPath)