class Report:
   
    
    def __init__(self):
        
        import log
    
        self.startTime = 0
        self.stopTime = 0
        self.duration = 0
               
        # sync time with NTP so we have accurate time?  Or assume parent is sending good time?
        
        # load local ruleset?   
        self.curfewStart = 23400 # daily start time in seconds
        
  
        self.planeLog = log.Log("plane.log")
        self.violationLog = log.Log("violation.log")
        self.errorLog = log.Log("error.log")
  
    def report(self, duration):

        # assume this function called immediately after the plane left
        
        # first get the time right now
        from datetime import datetime
        from datetime import timedelta
        self.stopTime = datetime.now()
        d = timedelta(seconds=duration)
        self.startTime = self.stopTime - d


        # so it must be a plane...log it
        timestamp = self.startTime.strftime("%Y%m%d %H:%M:%S")
        self.planeLog.add(timestamp + ': Plane with duration ' + str(duration) + ' seconds')

        # check against local ruleset if this is a violation
        if self.violationCheck(): # yes it's a violation so do something
            self.sendReport() # go ahead and send report
        
        return 1
        
    def violationCheck(self):
        # check that the current time is a violation

#        if 
        
        pass

    def sendReport(self):
        pass
        
        