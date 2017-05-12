#!/usr/bin/python3


# get the filename from command line
import sys
file_in = sys.argv[1]

# imports
import listener

myListener = listener.Listener()
myListener.getAudioData(file_in)
myListener.calculateStats()
myListener.printStats()

#print('comparing against "zero" file that is as low noise as possible')
#myListener.getAudioData('zero.wav')
#myListener.calculateStats()
#myListener.printStats()
