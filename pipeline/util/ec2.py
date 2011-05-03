import sys,os,socket,time

from boto.ec2.connection import EC2Connection
from fabric.api import run,sudo,settings,env

from pipeline.util.environment import Environment

VALID_IMGS = {"basicLinuxx32":{"imageid":"ami-76f0061f",
                              "supported_instances":["t1.micro","m1.small","c1.medium"],
                              "username":"root"}}

SECURITY_GROUPS = {"vertex":{"ssh":[22,22,"0.0.0.0/0"],
                             "http":[80,80,"0.0.0.0/0"]}}

class ec2(object):
    '''Methods to use aws ec2 instances'''
    
    def __init__(self,aws_access_key=Environment().get("ACCESS_KEY"),
                 aws_secret_key=Environment().get("SECRET_KEY"),region=None):
        '''Default constructor.
        
            Inputs:  
                aws_access_key = access key provided by aws
                aws_secret_key = secret key associated with access key'''
        self.__access_key = aws_access_key
        self.__secret_key = aws_secret_key
        self.__region = region
        self.__conn = EC2Connection(aws_access_key_id = self.__access_key, 
                                    aws_secret_access_key = self.__secret_key)
        self.__runningInstances = {}

    def getAvailImages(self):
        '''Get all available images that an ec2 instance can be started up with.'''
        return self.__conn.get_all_images()
    
    def getRunningInstances(self):
        return self.__runningInstances

    def startInstance(self,name,imageName,instanceType,keyPairName):
        '''Start up a new ec2 instance.
        
            Inputs:
                name = name to associate with instance
                imageName = name of image from VALID_IMGS
                instanceType = type of instance to start up, must be in the
                    list for the given VALID_IMGS
                keyPairName = key pair to associate with this image
            Returns: 
                dns to server if server successfully starts up'''
        
        if instanceType not in VALID_IMGS[imageName]["supported_instances"]:
            raise Exception("'" + instanceType + "' is not a valid type for '" + VALID_IMGS[imageName]["ami-76f0061f"] + "'")        

        image = self.__conn.get_image(VALID_IMGS[imageName]["imageid"])
                
        reservation = image.run(instance_type=instanceType,key_name=keyPairName)#,
                                #security_groups=["vertex"])
        instance = reservation.instances[0]
        
        instance.update()
        while instance.state != u'running':
            instance.update()
            
        self.__runningInstances[name] = instance
        return instance.dns_name
    
    # TODO : might want to have a full list of installable software somewhere
    def prepareInstance(self,dnsName,keyPairName,softwareList):
        '''Set up instance software.
        
            Inputs:
                dnsName = dns name of server
                keyPairAbsPath = keyPairName used with startInstance
                softwareList = a list of software to install, must be accessible
                    by yum on an ec2 instance. Best tested by running an ec2
                    instance and trying yum search or yum list all
            
            Returns:
                True if instance is set up properly'''
        
        with settings(host_string="ec2-user@%s" % dnsName,
                      key_filename="/home/kos/.ssh/%s.pem" % keyPairName,
                      warn_only=True):
            if not self._port_open(dnsName,22):
                print("FATAL: counld not connect to ec2 instance. Try increasing number of retries?")
                return False
            
            # TODO : might want to have the dist package somewhere online to just download
            sudo("wget https://github.com/kand/aws_pipeline/blob/master/dist/vertex_pipeline-1.0.tar.gz?raw=true --no-check-certificate")
            sudo("tar xvf vertex_pipeline-1.0.tar.gz")
            
            for s in softwareList:
                sudo("yum install -y %s" % s)
            
            return True
    
    def stopInstance(self,name):
        '''Stop an instance. This does not terminate an instance, however, as boto
            doesn't seem to have a way to do this...
            
            Inputs:
                name = name associated with instance to stop, set when using
                    startInstance()
            Returns:
                True if instance was successfully stopped.'''
        if name not in self.__runningInstances.keys():
            print("Name not found in dict of running instances")
            return False
        
        instance = self.__runningInstances[name]
        instance.stop()
        
        instance.update()
        while instance.state != u'stopped':
            print(instance.state)
            instance.update()
            
        self.__runningInstances.pop(name)
        return True

    # this function errors out in boto
    #def close(self):a.close()
    #    '''Close ec2 connection'''
    #    
    #    if not self.__checkConn(): return
    #    self.__conn.close()'''
    #    pass
    
    def _port_open(self,host,port,retries=Environment().get("MAX_SSH_RETRIES")):
        '''Test if a port is open on host.
            
            Inputs:
                host = host to attempt to connect to
                port = port to attempt to connect on
                retries = number of retries to attempt, with a 1 second pause between
                
            Returns:
                True if connected, False if failed'''
        sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        print("attempting to connect")
        for i in range(0,retries):
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
    pass
