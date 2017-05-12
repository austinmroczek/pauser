#!/usr/bin/python3

print('\n\nlearn.py starting\n\n')

# imports
import listener
import log

myLog = log.Log("plp.log")
myLog.add("learn.py starting")

# TODO setup sanity checks

myListener = listener.Listener()

print('\n\n\tLearn what we have been taught by the user (using teach.py).')
print('This could take a long time....\n\n')

myListener.learn()

myLog.add("learn.py done")
print('\n\nlearn.py done\n\n')
