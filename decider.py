
class Decider:
   
    def __init__(self):
        
        import log
        import listener
        
        self.myListener = listener.Listener()
        
        self.myLog = log.Log('decider.log')
        self.myLog.add('Decider initialized')

        self.deciders = []  # array to hold various deciders
        self.setupDeciders()
        
    def __del__(self):
        self.myLog.add('Decider closing down [destructor called]')

    def setupDeciders(self):
        # append as many deciders as you want to the 'deciders' list
        
        # austin's airplane finder
        import deciderTypeAirplane
        tempDecider = deciderTypeAirplane.deciderTypeAirplane()
        self.deciders.append(tempDecider)

        # TODO: add improved/alternate airplane finder

        # TODO: add train finder

        # TODO: add fog horn finder

        # TODO: add general noise monitor
                        
        # TODO: add other finder

    def isNoise(self): # returns true if there is a noise

        """
        We do the audio capture here so it only happens one time.
        
        If we let the deciderType do it, we could capture audio multiple times
        for each cycle.
        
        """
        # capture audio
        self.myListener.audioCapture()

        # load the data from file
        self.myListener.getAudioData()

        # do the FFT
        self.myListener.doFFT()

        # calculate stats on raw wave data
        self.myListener.calculateStats()
        self.myListener.printStats()

        # TODO:  should we also calculate basic audio statistics that all deciders want?


        # TODO:  right now it stops as soon as the first noise it hears
        # ...should it look through all deciders for some reason?

        for x in self.deciders:
            if x.isNoise(self.myListener):
                return True

        return False
