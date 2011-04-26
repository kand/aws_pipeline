import sys,os,socket,time

from boto.ec2.connection import EC2Connection
from fabric.api import run,sudo,settings,env

#import ssh_tools

sys.path.append("/media/files/docs/research/pipeline/src")
from pipelines.basePipeline import RunOrderFunction,BasePipeline
from util.environment import Environment

SECURITY_GROUPS = {"vertex":{"ssh":[22,22,"0.0.0.0/0"],
                             "http":[80,80,"0.0.0.0/0"]}}

class load_instance(BasePipeline):
    '''Load an ec2 instance and run a pipeline on it'''
    
    def __init__(self,addArgs=[]):
        BasePipeline.__init__(self)
        
        self.keyPair = addArgs[0]
        
        #aws keys
        #pem file name
        #pipeline name
        #pipeline parameters

        self.RUN_ORDER = [RunOrderFunction(self.startEc2),
                          RunOrderFunction(self.prepareInstance),
                          RunOrderFunction(self.loadPipeline),
                          RunOrderFunction(self.runPipeline)]
        self.name = "load_instance"
        
        self.dir = os.path.split(os.path.abspath(__file__))[0]
        self.ec2 = EC2Connection(Environment().get("ACCESS_KEY"),
                                 Environment().get("SECRET_KEY"))
        
    def handleOutput(self,pout,perr):
        if len(pout) > 0: print("STDOUT:{" + pout + "}")
        if len(perr) > 0: print("STDERR:{" + perr + "}")
        
    def startEc2(self):
        '''Start an ec2 instance'''
        image = self.ec2.get_image("ami-76f0061f")
        reservation = image.run(instance_type="t1.micro",key_name=self.keyPair)
        instance = reservation.instances[0]
        
        print("Instance starting up..."),
        
        instance.update()
        while instance.state != u'running':
            instance.update()
            
        print("Complete. user='root' dns='%s'" % instance.dns_name)
        
        return instance.dns_name
   
    def prepareInstance(self):
        '''Set up instance software'''

        with settings(host_string="ec2-user@%s" % self.result,
                      key_filename="/home/kos/.ssh/%s.pem" % self.keyPair,
                      warn_only=True):
            
            if not self._port_open(self.result,22):
                print("FATAL: could not connect to ec2 instance")
                sys.exit(0)
            
            sudo("yum install -y git")
            sudo("yum install -y python-boto.noarch")
            run("git clone git://github.com/kand/aws_pipeline.git")
            run("echo -e 'ACCESS_KEY=%s\nSECRET_KEY=%s\n' > aws_pipeline/config" 
                % (Environment().get("ACCESS_KEY"),
                   Environment().get("SECRET_KEY")))
            run("python2.6 aws_pipeline/src/pipeline.py run pipelines/test_save_state/test_save_state.py")
    
    def loadPipeline(self):
        '''Get and prepare pipeline'''
        pass
    
    def runPipeline(self):
        '''Run pipeline'''
        pass
    
    # TODO : need a maximum number of retries
    def _port_open(self,host,port):
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        i = 0
        while True:
            i += 1
            try:
                sock.connect((host,port))
                sock.close()
                print("connected")
                return True
            except Exception as e:
                print("."),
                time.sleep(1)
                continue
        print("connected")
        return False
        
if __name__ == "__main__":
    #TODO : need to add command line functionality to the script
    pass
    