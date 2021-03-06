class Log:
   
    def __init__(self, newFile):
    
        self.fileName = "logs/" + newFile
    
        # check that "logs" folder exists and create it if necessary
        import os
        if not os.path.isdir("logs"):
            os.makedirs("logs")   

        # TODO:  error checking on file...does it exist, is it writeable?

    
    def add(self, newString): # add new line to log file
        
        try:
            file = open(self.fileName,'a') # open the file in write mode
        except PermissionError:
            return "some default data"
        else:
            with file:
                file.write(self.getCurrentTimestamp() + ': ' + newString + '\n')
                file.close() # be nice and close out the file
        
    def getCurrentTimestamp(self): # make a timestamp
        
        from datetime import datetime
        currentTime = datetime.now()
        timestamp = currentTime.strftime("%Y%m%d %H:%M:%S")
        return timestamp