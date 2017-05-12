#!/usr/bin/python3


# imports
import listener

# TODO setup sanity checks

myListener = listener.Listener()

# get user input then capture audio

print('\n\n\tTeach the pauser about new recordings!\n\n')

choice = ''

while choice != 'x':

  choice = input('\np = plane, n = not plane, x = exit\n')
  if choice == 'p': # Plane
    myListener.teach(True)
  elif choice == 'n': # NOT a plane
    myListener.teach(False)
  elif choice == 'x': # exit
    exit()
  else:
    print('\nBad entry....try again\n')



