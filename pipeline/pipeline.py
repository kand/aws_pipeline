# main entry point for program

import sys,argparse

from pipelines.pipelineRunner import PipelineRunner
from util.environment import Environment
from util.misc import getDir,getPath

THIS_DIR = getDir(__file__)
CONFIG_FILE = getPath(__file__,'config')
USAGE_FILE = getPath(__file__,'usage')

def start(sys_args):
    '''Start pipeline with sys_args'''
    env = Environment()
    env.load(CONFIG_FILE)
    
    # TODO : this parser needs a lot of work
    
    parent_parser = argparse.ArgumentParser(prog="vertex_pipeline",
                                            description='commands to manipulate vertex pipelines')
    sub_parsers = parent_parser.add_subparsers(dest='subparser_name')
    
    run_parser = sub_parsers.add_parser('run',
                                        description='run a pipeline script')
    run_parser.add_argument('path',
                            help='path to pipeline to run')
    run_parser.add_argument('-e','--use_ec2',action='store_true',
                            help='use this option to run pipeline on an ec2 instance')
    run_parser.add_argument('-s','--start_at',metavar=('s'),
                            help='set a start point (s) to begin running pipeline at')
    run_parser.add_argument('pipeline_argument',nargs='*',
                            help='argument to pass to the pipeline')
    
    set_parser = sub_parsers.add_parser('set',
                                        description='set an environment variable')
    set_parser.add_argument('name',
                            help='environment variable to set')
    set_parser.add_argument('value',
                            help='value to set for environment variable')
    
    get_parser = sub_parsers.add_parser('get',
                                        description='get an environment variable')
    get_parser.add_argument('name',
                            help='environment variable to set')
    get_parser.add_argument('value',
                            help='value to set for environment variable')
    
    vals = vars(parent_parser.parse_args([sys_args[i] for i in range(1,len(sys_args))]))
    
    # TODO : finish this parser
    if vals['subparser_name'] == 'run':
        #run command
        pass
    elif vals['subparser_name'] == 'set':
        #set command
        pass
    elif vals['subparser_name'] == 'get':
        #get command
        pass
    
    # TODO : remove all this stuff
        #env.set(sys_args[2],sys_args[3]):
        #val = env.get(sys_args[2])
            #pipe = PipelineRunner(sys_args[2],False)
            #pipe = PipelineRunner(sys_args[2])
            #pipe.runPipeline(int(sys_args[4]),addArgs=addArgs)
            #pipe.runPipeline(addArgs=addArgs)

    env.save()

if __name__ == "__main__":
    start(sys.argv)
    