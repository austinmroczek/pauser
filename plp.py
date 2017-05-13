#!/usr/bin/python3



import log
myLog = log.Log("plp.log")
myLog.add("PLP start up checks beginning")


import plpHelper
plpHelper.startupChecks(myLog)




myLog.add("PLP start up checks passed")

# imports
import pauser
import decider

tv = pauser.Pauser()
myDecider = decider.Decider()

myLog.add("PLP ready...starting to listen")

while True: # check for a noise

    if myDecider.isNoise(): # there is noise
        
        if not tv.isPaused(): # not paused, so go ahead and pause
            tv.pause()
        
    else: #there is NOT noise now

        if tv.isPaused(): # then restart the TV
            tv.play()
