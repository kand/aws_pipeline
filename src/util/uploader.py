import urllib,urlparse,os,tempfile

from boto.exception import S3ResponseError
from boto.s3.connection import S3Connection
from boto.s3.key import Key

class AccessGrant():
    READ = "READ"
    WRITE = "WRITE"
    READ_ACP = "READ_ACP"
    WIRTE_ACP = "WRITE_ACP"
    FULL_CONTROL = "FULL_CONTROL"
    
    def __init__(self,email="",access=""):
        self.email = email
        self.access = access

class Uploader(object):
    '''Take a file at url and put it in an aws s3 bucket'''
    
    def __init__(self,access,secret):
        self.__access_key = access
        self.__secret_key = secret
        self.__conn = S3Connection(access,secret)
        
    def __bname(self,bucketName):
        '''Prefix bucketName with access key and make lower case so it can be
        used in boto's interface and will not suffer any name collisions in s3's
        flat namespace.'''
        return str(self.__access_key + "_" + bucketName).lower()
        
    def upload(self,url,bucketName,s3FileName,accessGrants=None,metadata={}):
        '''Download a file from url, upload it to an s3 bucket.
            
            Inputs:
                url = url of file to upload, or absolute path to local flie
                bucketName = name of bucket to create/put file on, will be made
                    lower case and prefixed with '<access_key>_'
                s3FileName = name of file, will be made lower case
                accessGrant = a list of AccessGrant instances that will give the 
                    specified level of access to specified user emails. Setting
                    this to None will not make the file public. Setting this to
                    an empty list will make the file completely public.
                metadata = a dictionary of metadata to apply to file, can use
                    this to set Content-Type
                
            Returns: returns the url of the file on s3'''
        
        #TODO : make more robust???
        
        file = self.parseUrl(url) 
        bucket = self.getBucket(bucketName)
        key = self.setKey(bucket,s3FileName,file,metadata)
        self.changeAccess(key,accessGrants)
        
        file.close()
        return "https://s3.amazonaws.com/" + bucket.name + "/" + s3FileName
    
    def getBucket(self,bucketName,failOnNoSuchBucket=False):
        '''Create or get bucket.
        
            Input:
                bucketName = name of bucket on s3. Will be prefixed with access
                    key to avoid naming collisions 
                failOnNoSuchBucket = True if function should throw an error if
                    bucket name provided does not exist. If this is False, will just 
                    create a new bucket or return the bucket with provided name.
                    
            Returns: an boto.s3 Bucket object'''
        bucketName = self.__bname(bucketName)
        if failOnNoSuchBucket:
            try:
                return self.__conn.get_bucket(bucketName)
            except S3ResponseError as e:
                raise Exception(e.error_message)
            
        return self.__conn.create_bucket(bucketName)
    
    def setKey(self,bucketObj,fileName,fStream,metadata={}):
        '''Set a key on a bucket to a file.
        
            Input:
                bucketObj = a boto.s3 Bucket object
                filename = name of file on 
                fStream = a file stream to upload to key
                
            Returns: a boto key object'''
        k = bucketObj.new_key(fileName)
        self.setMetadata(k,metadata)
        k.set_contents_from_file(fStream)
        return k
    
    def getKey(self,bucketObj,keyName):
        '''Get a boto key object from a bucket.'''
        k = bucketObj.get_key(keyName)
        if not k:
            raise Exception("key '" + keyName + "' does not exist")
        return k
    
    # TODO : this doesn't work...
    def setMetadata(self,key,metadata={}):
        '''Set metadata for a key.
            
            Inputs:
                key = a boto s3 key object
                metadata = a dictionary of metadata keys and values to add to
                    the key'''
        for k in metadata:
            key.set_metadata(k,metadata[k])
            # TODO : this doesn't work if key is already created
            print("set metadata of file '" + k + "' = '" + metadata[k] + "'")

    def changeAccess(self,key,accessGrants=None):
        '''Change access to a file on s3.
        
            Input:
                key = boto s3 key object to change access to
                accessGrants = list of AccessGrant objects that provide info on 
                    which users on s3 to provide access. If this is left as None,
                    the file will be made completely private. If left as an empty
                    list, will make the file completely public.
                    
            Returns: a boto key object'''
        if isinstance(accessGrants,list):
            if len(accessGrants) == 0:
                key.set_acl('public-read')
                print("File set to be publicly read")
            else:
                for g in accessGrants:
                    key.add_email_grant(g.access,g.email)
                    print("user '" + g.email + "' granted permission '" + g.access + "'")
        else:
            key.set_acl('private')
            print("File set to private")
        return key
    
    def parseUrl(self,url):
        '''Parse and grab a file object on file at url.
        
            Inputs:
                    url = path or url where file is located
                    
            Returns: File object at url'''
        retFile = None
        purl = urlparse.urlparse(url)
        if purl[0] == "http":
            furl = urllib.urlopen(url)
            if furl.getcode() != 200:
                raise Exception("got a '" + str(furl.getcode()) + "' response code for: '" + url + "'")
            retFile = tempfile.TemporaryFile()
            retFile.write(furl.read())
            furl.close()
        elif purl[0] == "":
            path = purl[2]
            try:
                retFile = open(path,"r")
            except IOError:
                raise Exception("file not found at path: '" + url + "'")
        else:
            raise Exception("url input not formatted properly")
        return retFile
    
if __name__ == "__main__":
    pass
        
