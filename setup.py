import os

from distutils.core import setup

def getDir():
    '''Get the directory that a script is contained in. File should be the
        __file__ variable.'''
    return os.path.split(os.path.abspath(__file__))[0]

def getPath(relPath):
    '''Get the path of a file relative to the directory a script is contained
        in. file should be the __file__ variable. relPath should be the path
        of said file relative to script.'''
    return os.path.join(getDir(),relPath)

files = ["util/*","pipelines/*","config","usage"]

setup(name = "vertex_pipeline",
      version = "1.0",
      description = "commands to use and manipulate vertex pipelines",
      author = "kand",
      author_email = "akos123@gmail.com",
      url = "https://github.com/kand/aws_pipeline.git",
      packages = [getPath("pipeline")],
      package_data = {getPath("pipeline"):files},
      scripts = [getPath("vertex_pipeline")],
      long_description = '''commands to use and manipulate vertex pipelines''',
      #classifiers = []
      )