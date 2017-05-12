
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
