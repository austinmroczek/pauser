#!/usr/bin/python3

import log
myLog = log.Log("plp.log")
myLog.add("PLP start up checks beginning")

import plpHelper
# check we're using the right Python version
if not plpHelper.hasRequiredPython(3,2,0): # python 3.2.0 --> hasRequiredPython(3,2,0)
    myLog.add("ERROR: Python version " + str(sys.version_info[0]) + "." + str(sys.version_info[1]) + "." + str(sys.version_info[2]) + " is less than required")
    exit()

# TODO other setup sanity checks

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
