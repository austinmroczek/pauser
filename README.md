# README #

### What is this repository for? ###

* Summary:  the Point Loma Pauser is python code running on a Raspberry Pi to listen for airplanes and then pause the television.  While the original purpose was specific to airplanes, it can be used for many other purposes.

### Supported playback devices to be controlled ###
* Roku3 

If you want to add one, see the Contribution section below

### How do I get set up? ###

Required hardware:

* Raspberry Pi 2
* Sound card
* Supported TV/other playback device(s) 

Check software dependencies:
* curl
* arecord
* python 3.?
* more???

Teach the system what is a plane:
* ./teach.py 
* Press P for plane, N for not, and X for exit
* Teaching pointers
**Teach the system many cases for both planes and not planes cases.  
**Make sure to have at least as many cases where there is NOT a plane as that is usually the case
**Teach in a number of scenarios in which you listen to TV.  Windows open/closed.
**Teach with your TV on and playing show(s) you watch often

Learn from what was taught
* ./learn.py  (this will take a long time...probably minutes)

### Contribution guidelines ###

Adding support for new playback devices
* create a new class that inherits the 'PauserDevice' class and implements the noted functions 
* add code to pauser.findDevices() so your device is found

Adding a new "decider" to decide if the noise heard is a train, foghorn or something else.  You could also create a better/alternative airplane decider.
* create a new class that inherits the 'deciderType' class and implements the noted functions
* add code to import your new class in the decider.setupDeciders() function in decider.py 

Other help needed
* audiophile know-how to review and/or improve everything

### Who do I talk to? ###

* austin@mroczek.org