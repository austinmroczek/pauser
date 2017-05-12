class PauserDevice:
    
    """PauserDevice class"""

    # class template for all future specific devices to inherit

    # TODO:  checks for "ready" in the various functions


    def __init__(self, deviceName):
        self.paused = False
        self.ready = False    # flag for if device is ready to take commands (it's been set up properly)
        self.address = ''
        
        self.setDeviceName(deviceName)
        
        import log
        self.myLog = log.Log('device.log')

    def __del__(self):
        self.myLog.add('Device (' + self.deviceName + ') closing down [destructor called]')

    def setDeviceName(self,newName):
        # TODO:  check that it's a string or convert it
        self.deviceName = newName

    def setDeviceAddress(self, newAddress):
        
        #TODO: error checking on address
        
        self.address = newAddress     

    def pause(self):
        # try to pause the device
        if (self.tryPause()):
            self.paused = True
        else:
            # the attempt failed...do we know if it's paused now?
            self.myLog.add("Device (" + self.deviceName + ") tryPause() failed")

    def tryPause(self):
        # try to pause the device and return True if successful
        
        # individual devices types (e.g. PauserDeviceRoku3) must implement this function
        
        # return False by default
        self.myLog.add("Device (" + self.deviceName + ") did not implement tryPause()")
        return False

    def play(self):

        # TODO:  check if already playing and if in playback mode
        
        # try to play the device
        if (self.tryPlay()):
            self.paused = False
        else:
            # the attempt failed...do we know if it's paused now?
            self.myLog.add("Device (" + self.deviceName + ") tryPlay() failed")

    def tryPlay(self):
        # try to play the device and return True if successful
        
        # individual devices types (e.g. PauserDeviceRoku3) must implement this function
        
        # return False by default
        self.myLog.add("Device (" + self.deviceName + ") did not implement tryPlay()")
        return False

    def backup(self):

        # try to backup the device
        if (self.tryBackup()):
            # success...
            # TODO:  check on mpact on self.paused status (device dependent?)
            pass
        else:
            # the attempt failed...do we know if it's paused now?
            self.myLog.add("Device (" + self.deviceName + ") tryBackup() failed")

    def tryBackup(self):
        # try to backup the device and return True if successful
        
        # individual devices types (e.g. PauserDeviceRoku3) must implement this function
        
        # return False by default
        self.myLog.add("Device (" + self.deviceName + ") did not implement tryBackup()")
        return False

    def isPaused(self):
        # return if we are paused or not
        
        # TODO:  what if not in playback mode?
        
        return self.paused

    def checkReady(self):
        # check if the device is ready to accept commands (it's been set up properly)
        # set the ready flag when done
        
        # individual devices types (e.g. PauserDeviceRoku3) must implement this function
        
        # set False by default
        self.myLog.add("Device (" + self.deviceName + ") did not implement checkReady()")
        self.ready = False

    def isReady(self):
        # return True if the device is ready for commands
        # if not already ready, check if it is ready
        
        # TODO:  think about errors over time...what if we lose the network after initial setup?
        # but don't want to checkReady() too much as it takes time/resources
        
        if self.ready==True:
            return True
        else:
            self.checkReady()
            return self.ready

    def isPlaybackMode(self):
        # return True if the device is in playback mode (not at a menu screen) 

        # this function is required so we don't try to restart playback when not appropriate
        # for example, don't send Roku the "play" command while in a menu screen


        # TODO:  determine if this belongs here...or in sub classes

        # individual devices types (e.g. PauserDeviceRoku3) must implement this function
        return True
         