import sys

from util.uploader import AccessGrant,Uploader

def printUsage():
    print("")
    print("VERTEX PIPELINE UTILITY")
    print("    Commands to use and manipulate pipelines.")
    print("USAGE")
    print("    pipeline <pipeline_name> <data_file_location>")
    print("        <pipeline_name> = name of pipeline to execute")
    print("        <data_file_location> = url or absolute path of data file")
    print("")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        printUsage()
    else:
        pass
        