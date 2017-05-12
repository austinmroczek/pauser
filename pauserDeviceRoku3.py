from subprocess import call
from pauserDevice import PauserDevice

class PauserDeviceRoku3(PauserDevice):
    
    """PauserDeviceRoku3 class"""

    # for a Roku3 device (other Roku versions may work...haven't checked)

#    def __init__(self):

    def checkReady(self):
        # check if the device is ready to accept commands (it's been set up properly)
        # set the ready flag when done    

        checksFailed = 0

        # TODO:  serious error checking, check on address, etc
        
        if not self.isPlaybackMode():
            checksFailed += 1
            
        if checksFailed > 0:
            self.ready = False
        else:
            self.ready = True 
    
    def tryPause(self):
        # for Roku via https://sdkdocs.roku.com/display/sdkdoc/External+Control+Guide
        # call("curl -d '' http://192.168.2.11:8060/keypress/Play", shell=True)

        if not self.isReady():
            return False
        
        if not self.isPlaybackMode():
            return False
              
        curlCommand = "curl -d '' http://" + self.address + ":8060/keypress/Play"
        self.myLog.add('pauserDeviceRoku3 tryPause() curl command: ' + curlCommand)
        call(curlCommand, shell=True)

        # TODO:  how to error check curl command?
        
        return True

    def tryPlay(self):

        if not self.isReady():
            return False
        
        if not self.isPlaybackMode():
            return False

        curlCommand = "curl -d '' http://" + self.address + ":8060/keypress/Play"
        self.myLog.add('pauserDeviceRoku3 tryPlay() curl command: ' + curlCommand)
        call(curlCommand, shell=True)

        # TODO:  how to error check curl command?

        return True

    def tryBackup(self):

        if not self.isReady():
            return False
        
        if not self.isPlaybackMode():
            return False

            
        curlCommand = "curl -d '' http://" + self.address + ":8060/keypress/InstantReplay"
        self.myLog.add('pauserDeviceRoku3 tryBackup() curl command: ' + curlCommand)
        call(curlCommand, shell=True)

        # TODO:  how to error check curl command?

        return True

    def isPlaybackMode(self):
        # return true if the roku is not at the homescreen right now

        # TODO:  serious error checking.  
              
        # https://sdkdocs.roku.com/display/sdkdoc/External+Control+Guide    query/active-app Examples

        curlCommand = "curl -m 2 -s http://" + self.address + ":8060/query/active-app > isPlaybackMode.txt"
        #self.myLog.add('pauserDeviceRoku3 isPlaybackMode() curl command: ' + curlCommand)
        call(curlCommand, shell=True)

        # TODO: figure out if netflix screen
        # TODO:  figure out if system is paused already

        
        if '<app>Roku</app>' in open('isPlaybackMode.txt').read():
            self.myLog.add('pauserDeviceRoku3 isPlaybackMode() == False')
            return False
        else:
            self.myLog.add('pauserDeviceRoku3 isPlaybackMode() == True')
            return True
         