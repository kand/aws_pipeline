import urllib,os

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
        
    def upload(self,url,bucketName,s3FileName,accessGrants=None):
        '''Download a file from url, upload it to an s3 bucket.
            
            Inputs:
                url = url of file to download, or absolute path to local flie
                bucketName = name of bucket to create/put file on, will be made
                    lower case and prefixed with '<access_key>_'
                s3FileName = name of file, will be made lower case
                accessGrant = a list of AccessGrant instances that will give the 
                    specified level of access to specified user emails. Setting
                    this to None will not make the file public. Setting this to
                    an empty list will make the file completely public.
                
            Returns: returns the url of the file on s3'''
            
        bucketName = bucketName.lower()
        s3FileName = s3FileName.lower()
        path = ""
        
        if url[0:7] == "http://":
            path = s3FileName
            try:
                urllib.urlretrieve(url,path)
            except IOError:
                print("[ERROR] file not found at url: '" + url + "'")
                return None
        else:
            path = url
            try:
                open(path,"r").close()
            except IOError:
                print("[ERROR] file not found at path: '" + url + "'")
                return None
        
        bucket_name = str(self.__access_key).lower() + "_" + bucketName
        bucket = self.__conn.create_bucket(bucket_name)
        
        k = Key(bucket)
        k.key = s3FileName
        k.set_contents_from_filename(path)
        
        if isinstance(accessGrants,list):
            if len(accessGrants) == 0:
                k.set_acl('public-read')
                print("File set to be publicly read")
            else:
                for g in accessGrants:
                    k.add_email_grant(g.access,g.email)
                    print("user '" + g.email + "' granted permission '" + g.access + "'")
        else:
            print("File set to private")
        
        if url[0:7] == "http://":
            os.remove(path)
        
        return "https://s3.amazonaws.com/" + bucket_name + "/" + s3FileName
        
    def __splitUrl(self,url):
        return url.replace("http://","").split("/")
    
if __name__ == "__main__":
    pass
        