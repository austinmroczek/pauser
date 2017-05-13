from deciderType import deciderType

class deciderTypeAirplane(deciderType):
   
    """Austin's Airplane Finder"""

    def startup(self):
        self.setDeciderName("DeciderTypeAirplane")

        self.planeThreshold = 4 # number of tests that must pass to count as a plane
        # load correlation data from file

        self.correlationThreshold = 22900
        self.correlationFile = 'correlationData.txt'
        self.getCorrelationData()

    def isNoise(self, theListener): # returns true if there is a noise 
        
        return self.isPlane(theListener)
        
    def isPlane(self, theListener): # returns true if there is a noise (after sanity checks)
        # 'hearPlaneNow' is true if the Listener hears a plane right now

        hearPlaneNow = self.hearPlaneNow(theListener)

        if not self.clockRunning and hearPlaneNow: 
            self.startTimer()

        if self.clockRunning and not hearPlaneNow:
            self.stopTimer()
            
        self.addListenerHistory(hearPlaneNow)
        
        if not self.sanityCheckConsequtive():
            self.addDecisionHistory(False)
            return False

        if not self.sanityCheckTimer():
            self.addDecisionHistory(False)
            return False

        self.addDecisionHistory(True)
        return True
    
    def hearPlaneNow(self, theListener):     # return True if it sounds like a plane right now

        # run tests
        if self.runPlaneTests(theListener) >= self.planeThreshold: # sounds like a plane right now
            return True
        else:
            return False
        
    def runPlaneTests(self, theListener):
        plane = 0

        # TODO:  theListener.fftData --> theListener.fftData
        if sum(theListener.fftData[1:101])/100 > 400:
            plane += 1

        if sum(theListener.fftData[1:201])/200 > 300:
            plane += 1

        if sum(theListener.fftData[1:301])/300 > 250:
            plane += 1

        # check if avg(100:200) > 200
        if sum(theListener.fftData[101:200])/100 > 200:
            plane += 1
            
        if sum(theListener.fftData[201:250])/50 > 125:
            plane += 1

        plane += self.testCorrelation(theListener)    
            
        return plane

    def testCorrelation(self, theListener, length=0):
        # return 1 if correlated to plane, 0 if not    

        if length == 0:
            testLength = theListener.fftNumUsefulBins
        else:
            if length <= theListener.fftNumUsefulBins:
                testLength = length
            else:
                self.myLog.add("ERROR in testCorrelation(): length is longer than fftNumUsefulBins")
                testLength = theListener.fftNumUsefulBins
                

        if theListener.fftNumUsefulBins!=len(self.correlationData):
            print('ERROR: fftNumUsefulBins different size than correlationData ' + str(theListener.fftNumUsefulBins) + ' vs ' + str(len(self.correlationData)))

        correlSum = 0.0
        for n in range(testLength):
            #print(str(n) + '\tdata: ' + str(theListener.fftData[n]) + '\tcorrel: ' + str(self.correlationData[n]) + '\tsum: ' + str(float(theListener.fftData[n])*float(self.correlationData[n])) + '\tcumm: ' + str(correlSum))
            correlSum += float(theListener.fftDataABS[n])*float(self.correlationData[n])

        self.statsCorrelation = round(correlSum,1)
        
        if correlSum > self.correlationThreshold:
            return 1
        else:
            return 0    

    def calculateCorrelationData(self, newTeachPath):
        # calculates the Pearson correlation for each frequency bin

        import os
        from scipy.stats import pearsonr 
        
        import listener
        tempListener = listener.Listener()
        

        groundTruth = []
        numSamples = 0
        correlData = [] # correlation data matrix
        finalData = []

        # get list of files in recordings directory
        filelist = os.listdir(newTeachPath)

        # take a filename and see if it is a .fft file
        for file in filelist:
            fftfile = newTeachPath + file
            # check if 'file' is a file (it could be a directory)
            if os.path.isfile(fftfile) and file[-4:]=='.fft':

                # set the groundTruth if the file is for a plane or not
                if file[0]=='p': # it's a plane
                    groundTruth.append(float(1))
                else:
                    groundTruth.append(float(0))

                # get the FFT data from file and add it to the list
                correlData.append(tempListener.getFFTData(fftfile))        
                numSamples += 1
                if len(correlData[numSamples-1]) != tempListener.fftNumUsefulBins:
                    print('Error: FFT in file (' + fftfile + ') not equal to expected value')
                    print('Expected: ' + str(tempListener.fftNumUsefulBins) + '\tActual: ' + str(len(correlData[numSamples-1])))
 
#        print(groundTruth)
  
        file = open('rawCorrelData.csv','w') # open the file in write mode
    
        for b in range(len(groundTruth)):
            file.write(str(groundTruth[b]) + ', ')

        file.write('\n')
    
        for freq in range(int(tempListener.fftNumUsefulBins)):
            freqSet = []
            for sample in range(numSamples):
                freqSet.append(correlData[sample][freq])
                file.write(str(correlData[sample][freq]) + ', ')

            file.write('\n')

            # find the correlation co-efficient for this frequency
            # use scipy's pearsonr(x,y) to calculate the correlation
            result = pearsonr(freqSet,groundTruth)
            finalData.append(result[0])

        # TODO:  sanity check the correlation data against existing FFT files?

        file.close() # be nice and close out the file

        # save the correlation data to a file for future use 
        self.saveCorrelationData(self.correlationFile, finalData)    
            
    def teach(self, plane, theListener):
        # plane = True if there is a plane

        theListener.audioCapture() # grab an audio sample

        from datetime import datetime
        now = datetime.now()
        timestamp = now.strftime("%Y%m%d_%H%M_%S")

        if plane == True:
            newFileName = theListener.teachPath + 'plane_' + str(timestamp) + '.wav'
        else:
            newFileName = theListener.teachPath + 'not_' + str(timestamp) + '.wav'

        import os
        if not os.path.isfile(theListener.fileName):
            self.myLog.add("ERROR:  teach() the Listener filename doesn't exist")
            print("ERROR:  teach() the Listerer filename doesn't exist")
            exit()

        # move the file and change the name
        os.rename(theListener.fileName, newFileName)

    def learn(self, theListener):  # learn from collected wave files

        import os

        learnCount = 0
    
        # get list of files in recordings directory
        filelist = os.listdir(theListener.teachPath)

        # take a filename and see if it has an associated .fft file
        for file in filelist:
            wavefile = theListener.teachPath + file
            fftfile = wavefile + '.fft'
            # check if 'file' is a file (it could be a directory)
            if os.path.isfile(wavefile) and wavefile[-4:]=='.wav':
                # got a valid file name, so check if the FFT file exists
                if not os.path.isfile(fftfile): # fft doesn't exist so make it
                    print(wavefile + ' FFT does not exist.  Creating...')
                    theListener.getAudioData(wavefile)
                    theListener.doFFT()
                    theListener.saveFFT(fftfile, theListener.fftData)
                    learnCount += 1

        if learnCount > 0:
            print('\n\nLearned from ' + str(learnCount) + ' new WAVE files.\n\n')
        else:
            print('\n\nThere was nothing to learn.  You need to teach the pauser some WAVE files.\n\n') 

        print('Calculating correlation...could take a while...')
        self.calculateCorrelationData(theListener.teachPath)
