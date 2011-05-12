import sys,os

from aws_tools.ec2 import ec2,VALID_IMGS,INSTANCE_SIZES

class PipelineRunner(object):
    
    def __init__(self,path):
        '''Handles running pipelines. Pipeline classes must have the same file
            and class name.
            Inputs: 
                path = path to python pipeline script'''
        psplit = os.path.split(path)
        self.path = psplit[0]
        self.name = psplit[1].replace(".py","")
    
    def loadPipeline(self):
        '''Load the pipeline'''
        sys.path.append(self.path)
        return __import__(self.name)
    
    def runPipeline(self,startPoint=0,pipeline_args=None):
        '''Run the set pipeline
            Inputs:
                startPoint = stage to start pipeline at
                pipeline_args = string to pass to pipeline as arguments'''
        module = self.loadPipeline()
        pipeline = module.__getattribute__(self.name)()
        return pipeline.run(startPoint,pipeline_args)
    
    def runPipelineOnEc2(self,size=INSTANCE_SIZES.T1MICRO,
                         startPoint=0,pipeline_args=None):
        '''Run the set pipeline on ec2
            Inputs:
                size = size of instance, taken from ec2.INSTANCES_SIZES
                startPoint = stage to start pipeline at
                pipeline_args = string to pass to pipeline as arguments'''
        
        inst_name = "pipeline"
        
        ec2conn = ec2()
        dns_name = ec2conn.startInstance(inst_name,VALID_IMGS['baxicLinuxx32'],size)
        prepared = ec2conn.prepareAndRunInstance(dns_name,self.path,self.name,
                                                pipeArgs=pipeline_args)
        
        if not prepared:
            print("Error: Instance didn't prepare properly, shutting it down")
            ec2conn.stopInstance(inst_name)
            return False
        return True

if __name__ == "__main__":
    pass
