#!/usr/bin/python3


# imports
import listener
import deciderTypeAirplane

# TODO setup sanity checks

myListener = listener.Listener()

myDecider = deciderTypeAirplane.deciderTypeAirplane()

# get user input then capture audio

print('\n\n\tTeach the pauser about new recordings!\n\n')

choice = ''

while choice != 'x':

  choice = input('\np = plane, n = not plane, x = exit\n')
  if choice == 'p': # Plane
    myDecider.teach(True,myListener)
  elif choice == 'n': # NOT a plane
    myDecider.teach(False,myListener)
  elif choice == 'x': # exit
    pass
  else:
    print('\nBad entry....try again\n')

print('\nLearning what was taught...')
myDecider.learn(myListener)