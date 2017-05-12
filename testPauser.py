#!/usr/bin/python3

# imports
import pauser

myPauser = pauser.Pauser()

print('\n\nTESTING pauser.py\n\n')

if myPauser.isPlaybackMode():
    print('\nisPlaybackMode() = TRUE\n')
else:
    print('\nisPlaybackMode() = FALSE\n')