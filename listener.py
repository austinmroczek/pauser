#import unicodedata

class Listener:

    def __init__(self):
        import log
        self.myLog = log.Log('listener.log')

        # files and paths
        self.fileName = 'rectest.wav' # default file name
        self.teachPath = 'recordings/'

        # audio data        
        self.max_freq = 11025 
        self.fs = 0
        self.numSamples = 0
        self.bitsPerSample = 16 # number of bits per sample in the file...assumed to be 16
        self.rawData = [] # raw data from wave file
        self.normalizedData = [] # wave file data normalized on -1 to 1
        self.normalizedDataDB = [] # normalized data coverted to decibels

        # FFT data
        self.fftData = []
        self.fftDataABS = []
        self.fftNumUsefulBins = 11026 # set when FFT performed or when FFT data read from file
        self.fftBinSize = 0.0

        # A-weight data
        self.fftDataAweight = []
        self.normalized_aWeight = []
        self.statsRMSdB_A = 0.0



        #stats
        self.statsMaxAmplitudeDB = 0.0
        self.statsRMSdB = 0.0
        self.statsCorrelation = 0.0

    def audioCapture(self):
        # captures audio into a file
        # from http://www.g7smy.co.uk/?p=283

        #SAVEFILE='rectest.wav'
        #DURATION='1'
        #RATE='22050'
        #FORMAT='S16_LE' # see manual for arecord
        #CHANNELS='1'

        from subprocess import call
        # this function won't work in python 3.5
        call('/usr/bin/arecord -D plughw:1 -f S16_LE -c1 -r22050 --duration=1 ' + self.fileName + ' > /dev/null 2>&1', shell=True)

    def saveFFT(self, newFile, myFFT):
        # save FFT data to a file
        file = open(newFile,'w') # open the file in write mode
        
        # only save useful data
        for x in range(self.fftNumUsefulBins):
            file.write(str(abs(myFFT[x])) + '\n')
        
        file.close() # be nice and close out the file

    def getAudioData(self, audioFile=""):
        # get audio data out of the file
        if audioFile=="":
            audioFile = self.fileName
            
        from scipy.io import wavfile 

        # TODO: error checking on file operations...does it exist...can I access it...etc
            
        # https://docs.scipy.org/doc/scipy-0.15.1/reference/generated/scipy.io.wavfile.read.html
        self.fs, self.rawData = wavfile.read(audioFile) # load the data

        # from http://samcarcagno.altervista.org/blog/basic-sound-processing-python/
        if self.rawData.dtype == "int16":
            self.bitsPerSample = 16
        elif self.rawData.dtype == "int32":
            self.bitsPerSample = 32
        else: # unknown....we asked for 16 so assume it...but log an error
            self.bitsPerSample = 16
            self.myLog.add("WARNING in getAudioData(): unknown number of bits per sample: " + self.rawData.dtype + " continuing with 16 bits")

        self.numSamples=len(self.rawData)
                        
        self.normalizeData()
        
    def normalizeData(self): # normalize audio data 
        # normalize wave data between -1 and 1
        
        normalizeFactor = 2**(self.bitsPerSample-1)

        self.normalizedData = []
        self.normalizedDataDB = []
        
        #self.normalizedData=[x/normalizeFactor for x in self.rawData]             
        for x in self.rawData:
            self.normalizedData.append(x/normalizeFactor)
            self.normalizedDataDB.append(self.calculateDecibels(abs(x/normalizeFactor)))

    def getFFTData(self, filename):
      
        # read data from a file
        data = []
        file = open(filename,'r')
        # TODO:  file error checks


        for line in file:
            data.append(float(line))
        file.close()
        return data

    def printStats(self): #print stats about data
        #print('Sample freq: ' + str(self.fs) + ' Hz')
        #print('FFT # useful bins: ' + str(self.fftNumUsefulBins))
        #print('FFT bin size: ' + str(self.fftBinSize) + ' Hz/bin')
        #print('Correlation data points: ' + str(len(self.correlationData)))
        #print('Max Amplitude: ' + str(round(self.statsMaxAmplitudeDB,1)) + ' dB\tRMS: ' + str(round(self.statsRMSdB,1)) + ' dB\tRMS: ' + str(round(self.statsRMSdB_A,1)) + ' dB(A)')
        print('Max Amplitude: ' + str(round(self.statsMaxAmplitudeDB,1)) + ' dB\tRMS: ' + str(round(self.statsRMSdB,1)) + ' dB')
    def doFFT(self):
        # from https://stackoverflow.com/questions/23377665/python-scipy-fft-wav-files
        from scipy.fftpack import rfft
        self.fftData = rfft(self.normalizedData) # calculate real FFT

        self.setFFTnumUsefulBins()
        self.setFFTbinSize()
        
        self.calculateFFTABS()

    def calculateFFTABS(self):
        # use absolute value of data because only care about amplitude
        self.fftDataABS = [abs(x) for x in self.fftData]       

    def setFFTnumUsefulBins(self):
        if self.numSamples == 0:
            self.myLog.add("ERROR in setFFTnumUsefulBins():  numSamples == 0 --> about to divide by zero")
            exit()
            
        # from https://docs.scipy.org/doc/scipy/reference/tutorial/fftpack.html#one-dimensional-discrete-fourier-transforms
        if self.numSamples % 2 == 0: # even number of samples
            # n/2 + 1 
            # item [0] is the zero-frequency term
            # item [1]....[n/2] are the positive frequency terms
            self.fftNumUsefulBins = int((self.numSamples / 2)) + 1

        else: # odd number of samples
            #...which is odd because we should have an even number
            #...because the audio sample rates are even
            #...and the number of seconds to record using 'arecord' is an integer
            # TODO: can probaby do error checking...but not expecting to get here
            self.myLog.add("ERROR in doFFT():  odd number of audio samples")
            exit()
        
    def setFFTbinSize(self):
        if self.fftNumUsefulBins == 0: # don't divide by zero
            self.fftBinSize = 0
        else:
            self.fftBinSize = float(self.fs/2)/self.fftNumUsefulBins # max frequency found is Fs/2 divided by number of real bins

    def learn(self):  # learn from collected wave files

        import os

        learnCount = 0
    
        # get list of files in recordings directory
        filelist = os.listdir(self.teachPath)

        # take a filename and see if it has an associated .fft file
        for file in filelist:
            wavefile = self.teachPath + file
            fftfile = wavefile + '.fft'
            # check if 'file' is a file (it could be a directory)
            if os.path.isfile(wavefile) and wavefile[-4:]=='.wav':
                # got a valid file name, so check if the FFT file exists
                if os.path.isfile(fftfile):
                    # fft exists...do anything?
                    #print(wavefile + ' FFT exists')
                    pass
                else:
                    # fft doesn't exist so make it
                    print(wavefile + ' FFT does not exist.  Creating...')
                    self.getAudioData(wavefile)
                    self.doFFT()
                    self.saveFFT(fftfile, self.fftData)
                    learnCount += 1

        if learnCount > 0:
            print('\n\nLearned from ' + str(learnCount) + ' new WAVE files.\n\n')
        else:
            print('\n\nThere was nothing to learn.  You need to teach the pauser some WAVE files.\n\n') 

        print('Calculating correlation...could take a while...')
        self.calculateCorrelationData()
        
    def calculateAweight(self): # calculate A-weight of current FFT
    
        # TODO:  make sure this is even correct...probably NOT
    
    
    
        # lookup aWeight for each frequency bin from FFT data
        # https://stackoverflow.com/questions/4364823/how-do-i-obtain-the-frequencies-of-each-value-in-an-fft
        data = []

                
        for binNum in range(0,int(self.fftNumUsefulBins/2)):
            data.append(self.aWeightLookup(binNum*self.fftBinSize) * self.fftData[binNum])
        
        self.fftDataAweight = data
        
        
        # do inverse transform to get aWeight wave data
        from scipy.fftpack import irfft
        self.normalized_aWeight = irfft(self.fftDataAweight)
        # do RMS on data to get dB(A)
        
        self.statsRMSdB_A = self.calculateRMS(self.normalized_aWeight)       
        
        pass

    def aWeightLookup(self,frequency): # look up A-weight for a frequency and return the coefficient to multiply by
        
        # http://www.diracdelta.co.uk/science/source/a/w/aweighting/source.html
        coefficient = 1.0  # placeholder  until we know the forumula

        if frequency > 0:
            
            f2 = frequency ** 2
            f4 = frequency ** 4
            
            from math import log10
            
#            a = 10*log10(1.562339*f4/((f2 + 11589.0930520225)*(f2 + 544440.6704605728)))
#            b = 10*log10(2.242881e+16*f4/((f2 + 424.31867740600904)*(f2 + 148699001.40839997)))

            # skip the log10() because we're not in dB yet
#            a = (1.562339*f4/((f2 + 11589.0930520225)*(f2 + 544440.6704605728)))
#            b = (2.242881e+16*f4/((f2 + 424.31867740600904)*(f2 + 148699001.40839997)))

            a = (1.562339*f4)/(((f2 + 11589.0930520225)*(f2 + 544440.6704605728)))
            b = (2.242881e+16*f4/((f2 + 424.31867740600904)*(f2 + 148699001.40839997)))



#            print("Freq: " + str(frequency) + '\tA-factor: ' + str(a+b))
#            print("Freq: " + str(frequency) + '\tA-factor db: ' + str(self.calculateDecibels(a)+self.calculateDecibels(b)))
            
            return (a + b) 
            
        else:
            return -1E+32
    
    def calculateStats(self): # calculate stats about the wave file

        maxDB=-100.0
        for x in self.normalizedDataDB:
            if x>maxDB:
                maxDB = x
        self.statsMaxAmplitudeDB = maxDB
        
        self.statsRMSdB = self.calculateDecibels(self.calculateRMS(self.normalizedData))
        
#        self.calculateAweight()

    def calculateRMS(self,data):
        # https://stackoverflow.com/questions/5613244/root-mean-square-in-numpy
        from numpy import mean, sqrt, square
        return sqrt(mean(square(data)))

    def calculateDecibels(self,ratio):
        from math import log10    
        if ratio==0:
            self.myLog.add("MATH ERROR: log10(zero) in calculateDecibels() ")
            return -100.0
        else:
            # TODO: age old question ....10 or 20 x log10(ratio)
            # think it's 20 times
            return 20 * log10(ratio)      
            
9