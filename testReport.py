#!/usr/bin/python3

# imports
import report
from time import sleep

# TODO setup sanity checks

#fileName = plp_helper.getFileName()


myReport = report.Report()
isPlane = False 
testPlane = 1

print('\n\nTESTING report.py\n\n')

while True:

    # check for a plane
    if testPlane > 1 and testPlane < 5:
        #there is a plane now...check if we're already paused
        
        if not isPlane: # not paused, so go ahead and pause
            isPlane = True
            print('Plane...pausing TV')
            # tv.pause()
            myReport.start()
        else:
            print('Plane...already paused')    
        
    else:
        #there is NOT a plane now
        if isPlane:
            #restart the TV
            print('No plane...restarting the TV')
            # tv.backup()
            myReport.stop()
            isPlane = False
        else:
            print('No plane')    

    testPlane += 1
    sleep(3) # sleep so it goes about as fast as the real hardware
    if testPlane > 6:
        testPlane = 1