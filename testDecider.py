#!/usr/bin/python3

# imports
import decider
from time import sleep

myDecider = decider.Decider()

print('\n\nTESTING decider.py\n\n')


#  test time stuff
print('...testing basic time functions...')
myDecider.startTimer()
myDecider.stopTimer()
print('expecting duration (0):  ' + str(myDecider.getDuration()))


myDecider.startTimer()
sleep(3) # sleep 3 seconds
myDecider.stopTimer()
print('expecting duration (3):  ' + str(myDecider.getDuration()))


#  test sanityCheckTimer()
print('...testing sanityCheckTimer()...')
myDecider.startTimer()
myDecider.stopTimer()
print('(0 sec duration) expecting False : ' + str(myDecider.sanityCheckTimer()))

myDecider.startTimer()
sleep(4) # sleep 4 seconds
myDecider.stopTimer()
print('(4 sec duration) expecting False : ' + str(myDecider.sanityCheckTimer()))

myDecider.startTimer()
sleep(5) # sleep 5 seconds
myDecider.stopTimer()
print('(5 sec duration) expecting True : ' + str(myDecider.sanityCheckTimer()))

myDecider.startTimer()
sleep(30) # sleep 30 seconds
myDecider.stopTimer()
print('(30 sec duration) expecting True : ' + str(myDecider.sanityCheckTimer()))

myDecider.startTimer()
sleep(31) # sleep 31 seconds
myDecider.stopTimer()
print('(31 sec duration) expecting False : ' + str(myDecider.sanityCheckTimer()))