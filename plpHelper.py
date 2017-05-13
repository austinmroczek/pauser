
def startupChecks(myLog):
    
    # check we're using the right Python version
    if not hasRequiredPython(3,2,0): # python 3.2.0 --> hasRequiredPython(3,2,0)
        myLog.add("ERROR: Python version " + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + " is less than required")
        exit()
    myLog.add("pass:  Python version high enough")
    
    # check that scipy exists
    try:
        import scipy
        myLog.add("pass:  scipy exists")
    except ImportError:
        myLog.add("ERROR: scipy does not exist")
        exit()
    
    # TODO other setup sanity checks
    

##### hasRequiredPython() #####
def hasRequiredPython(vMajor,vMinor,vMicro):

    import sys

    if sys.version_info[0] < vMajor:
        return False
    elif sys.version_info[0] > vMajor:
        return True
    else:
        if sys.version_info[1] < vMinor:
            return False
        elif sys.version_info[1] > vMinor:
            return True
        else:
            if sys.version_info[2] < vMicro:
                return False
            else:
                return True


##### getFileName() #####
def getFileName():
        # get the filename from command line
        import sys
        file_in = sys.argv[1]

        # TODO: error checking on the filename...does it exist...etc

        return file_in
##### getFileName() #####

def test():
	print('it works')
