
class deciderType:
   
    """DeciderType class"""

    # class template for all future specific "deciders" to implement
   
    def __init__(self): # class constructor
        
        import log

        self.myLog = log.Log('decider.log')
        self.myLog.add('DeciderType initialized')
        
        self.deciderName = "DeciderType"

        ##### sanity check variables #####
        from datetime import datetime
        self.startTime = datetime.now()
        self.stopTime = datetime.now()
        self.duration = 0
        self.clockRunning = False
        self.consequtive = 3        # minimum number of hits in a row before we think it's a real noise

        self.minimumTime = 5      # minimum time in seconds for reporting a noise
        self.maximumTime = 30     # maximum time in seconds for reporting a noise
        
        """
        The 'listenerHistory' is based on a single moment of audio capture data.  
        It could 'hear' a noise based on dB level, frequency correlation or other values
        
        The 'decisionHistory' is based on other factors or sanity checks.
        For example, while the listener could think there is a noise, 
        a sanity check could be the fact that we wear that noise three consequtive times.
        Until we 'hear' it three times in a row, we do not 'decide' there is a noise.
        
        """
        self.listenerHistory = []   # history of the Listener hearing a noise in the moment
        self.decisionHistory = []      # history of this Decider determining there is a noise after sanity checks

        # these should both be the same value
        self.listenerHistoryMax = 20
        self.decisionHistoryMax = 20
        
        self.correlationData = []
        
        
        self.startup()
        
    def startup(self):
        # this will run immediately after the constructor
        # it is here so deciderTypeXYZ can have "startup" code without overriding the entire contstructor
        pass

#    def __del__(self):
#        self.myLog.add('DeciderType ' + self.deciderName + ' closing down [destructor called]')

    def setDeciderName(self,newName):
        self.deciderName = newName

    def isNoise(self, theListener): # returns true if there is a noise 
        # return False by default
        self.myLog.add("ERROR - Decider (" + self.deviceName + ") did not implement isNoise()")
        return False
           
    def sanityCheckTimer(self):  # return True if passes all sanity checks, False if not

        self.calculateDuration()
        
        # check if time is greater than X seconds
        if self.getDuration() < self.minimumTime:
            print('Decider.sanityCheckTimer() failed minimum time check (' + str(self.getDuration()) + ' seconds)')
            self.myLog.add('Decider.sanityCheckTimer() failed minimum time check (' + str(self.getDuration()) + ' seconds)')
            return False
        
        # check if time is less than Y seconds      
        if self.duration > self.maximumTime:
            print('Decider.sanityCheckTimer() failed maximum time check (' + str(self.duration) + ' seconds)')
            self.myLog.add('Decider.sanityCheckTimer() failed maximum time check (' + str(self.duration) + ' seconds)')
            return False
        
        return True # passed all tests so return True
    
    def startTimer(self): # start the reporting clock
        from datetime import datetime    
        self.startTime = datetime.now() 
        self.clockRunning = True
    
    def stopTimer(self):
        from datetime import datetime
        self.stopTime = datetime.now()
        self.clockRunning = False
        
    def calculateDuration(self):
        from datetime import timedelta
        d = self.stopTime - self.startTime
        self.duration = int(d.total_seconds())

    def calculateCurrentDuration(self):
        # returns the current time duration from startTime until this moment 
        from datetime import datetime
        from datetime import timedelta
        currentTime = datetime.now()
        d = currentTime - self.startTime
        return int(d.total_seconds())
    def getDuration(self):
        # if the clock is running return the difference between startTime and now
        # if the clock is not running return the difference between startTime and stopTime
        
        if self.clockRunning:
            return self.calculateCurrentDuration()
        else:                  
            self.calculateDuration()
            return self.duration

    def addListenerHistory(self, newEntry): # adds 
        if newEntry:
            self.listenerHistory.append(1)
        else:
            self.listenerHistory.append(0)
        
        if len(self.listenerHistory) > self.listenerHistoryMax:
            self.listenerHistory = self.listenerHistory[-self.listenerHistoryMax:]

    def addDecisionHistory(self, newEntry): # adds 
        if newEntry:
            self.decisionHistory.append(1)
        else:
            self.decisionHistory.append(0)
        
        if len(self.decisionHistory) > self.decisionHistoryMax:
            self.decisionHistory = self.decisionHistory[-self.decisionHistoryMax:]

    def sanityCheckConsequtive(self): # return true if we heard noise last X times
        
        a = 0
        
        if self.consequtive > len(self.listenerHistory):
            return False
        
        for x in self.listenerHistory[-self.consequtive:]:
            if x:
                a += 1
        
        if a == self.consequtive:
            return True
        else:
            return False

    def wasNoise(self): # return True if there was a noise last time around

        if len(self.decisionHistory) > 0: # return last item in the list
            if self.decisionHistory[-1] == 1:
                return True
        
        return False

    def heardNoise(self): # return True if the listener heard a noise last time around

        if len(self.listenerHistory) > 0: # return last item in the list
            if self.listenerHistory[-1] == 1:
                return True
        
        return False

    def getCorrelationData(self): # read correlation data from a file

        self.correlationData = [] # first clear out the data 

        if self.correlationFile == '':
            self.myLog.add("ERROR: correlationFile was not defined")
            exit()

        import os
        if os.path.isfile(self.correlationFile):

            file = open(self.correlationFile,'r')
            for line in file:
                self.correlationData.append(float(line))
            file.close()

        else: # doesn't exist so create it
            file = open(self.correlationFile,'w')
            file.write("")
            file.close()

        # TODO check that there was actually data in the file
        if not len(self.correlationData) > 0:
            self.myLog.add("ERROR: there is no data in the correlationFile...use teach.py")
                    
    def saveCorrelationData(self, newfile, myData):
        # save correlation data to a File
        file = open(newfile,'w') # open the file in write mode
        for x in range(len(myData)):
            file.write(str(myData[x]) + '\n')
        file.close() # be nice and close out the file


