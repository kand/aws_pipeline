import sys

from util.uploader import AccessGrant,Uploader

def printUsage():
    print("")
    print("VERTEX PIPELINE UTILITY")
    print("    Commands to use/manipulate vertex pipelines.")
    print("")
    print("Usage")
    print("    python pipeline.py upload <access_key> <secret_key> <url> <bucket_name> <file_name> [<access_list>]")
    print("        Upload a file to an aws bucket.")
    print("         access_key = aws access key")
    print("         secret_key = aws secret key")
    print("                url = url (must start with 'http://') or absoulte path where file to upload is located")
    print("        bucket_name = name of bucket to use/create, name will be prefixed with <access_key>")
    print("          file_name = name to give file once uploaded to s3")
    print("        access_list = (optional) a list of aws user e-mails and access level to provide to them. This") 
    print("                should be formatted the following way:")
    print("                    [] will make the file completely public, even to non aws users.")
    print("                                             OR")
    print("                    [<user_email_1>:<access_level>,<user_email_2>:<access_level>,...]")
    print("")

if __name__ == "__main__":
    if len(sys.argv) < 7:
        printUsage()
    else:
        if sys.argv[1] == "upload":
            u = Uploader(str(sys.argv[2]),str(sys.argv[3]))
            
            accessGrants = None
            if len(sys.argv) == 8:
                accessGrants = []
                if sys.argv[7] != "[]":
                    temp = sys.argv[7].strip("[").strip("]")
                    temp = temp.split(",")
                    for a in temp:
                        s = a.split(":")
                        g = AccessGrant(s[0],s[1])
                        accessGrants.append(g)
            
            print(u.upload(str(sys.argv[4]),str(sys.argv[5]),str(sys.argv[6]),accessGrants))
        else:
            printUsage()