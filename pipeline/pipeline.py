# main entry point for program

import sys,argparse

from pipelines.pipelineRunner import PipelineRunner
from util.environment import Environment
from util.misc import getDir,getPath

def start(sys_args):
    '''Start pipeline with sys_args'''
    env = Environment()
    
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
    
    showAll_parser = sub_parsers.add_parser('showAll',
                                            description='show all environment variables and their values')

    vals = vars(parent_parser.parse_args([sys_args[i] for i in range(1,len(sys_args))]))
    
    # TODO : need to test, not using start_at yet
    if vals['subparser_name'] == 'run':
        runner = PipelineRunner(vals['path'])
        if vals['use_ec2']:
            runner.runPipelineOnEc2()
        else:
            runner.runPipeline()
        
    elif vals['subparser_name'] == 'set':
        env.set(vals['name'],vals['value'])
    
    elif vals['subparser_name'] == 'get':
        val = env.get(vals['name'])
        if val is not None:
            print(val)
            
    elif vals['subparser_name'] == 'showAll':
        env.showAll()

    env.save()

if __name__ == "__main__":
    start(sys.argv)
    