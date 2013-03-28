from pImage import pImage
import pCell
from pCell import *
import glob
import numpy
import time
from pImgMgr import *
import sys

class pImageSequence(object):
    
    def __init__(self, directory, CELLS_PER_ROW, CELLS_PER_COLUMN): 
        self.directory = directory
        self.images = []
        self.cpr = CELLS_PER_ROW
        self.cpc = CELLS_PER_COLUMN

        self.histograms = [[numpy.zeros(256) for i in xrange(self.cpc)] for i in xrange(self.cpr)]

        jpgs = glob.glob("%s/*.jpg" % self.directory)
        print "Found %s images" % len(jpgs)
        default = pImage(jpgs[0])
        default.makeDefault()
        default.cellify(self.cpr, self.cpc)
        self.generateLuminance(default)
        default.classifyCells(True)
        default.setBoardArea()
        default.free()

        self.images = [0 for x in xrange(len(jpgs))]        
        for index in xrange(len(jpgs)):
            pImg = pImage(jpgs[index])
            pImg.cellify(self.cpr, self.cpc)
            self.images[index] = pImg
            pImg.free()

    def getStartingKeyImage(self):
        keyImage = pImage(self.images[0].filename)
        keyImage.cellify(self.cpr, self.cpc)
        keyImage.classifyCells(True)
        return keyImage

    def findKeyImages(self):
        # Setup key image 
        keyImage = self.getStartingKeyImage()

        # Initialize values
        keyImageCount = 0                   # Num key images found
        strokeThresh = 1.2 * keyImage.strokeCount # Baseline misclassified stroke cells
        decreasingInformation = False       # If currently erasing
        debugCount = 1                      # Used to generate debugging images
        devThreshSing = 3                  # Threshold for detecting key image looking at one image
        devThreshDoub1 = 2                  # Threshold for detecting key image looking at two images
        devThreshDoub2 = 3
        
        sThresh1 = 5
        sThresh2 = 5
        
        for index in range(len(self.images) - 1):
            imLookAhead1 = self.images[index]
            imLookAhead2 = self.images[index + 1]

            imLookAhead1.load()
            imLookAhead2.load()

            # Check to see how many stroke cells are becoming board cells
            nFewerStrokesLA1 = imLookAhead1.nFewerStrokesThan(keyImage)
            nFewerStrokesLA2 = imLookAhead2.nFewerStrokesThan(keyImage)

            # Calculate deviation of stroke cells
            deviationLA1 = nFewerStrokesLA1 * 100.0 / (keyImage.strokeCount + 1)
            deviationLA2 = nFewerStrokesLA2 * 100.0 / (keyImage.strokeCount + 1)
            print "(%s) fewer 1: %s fewer 2: %s" % (debugCount, nFewerStrokesLA1, nFewerStrokesLA2)

            isPossibleKey = keyImage.strokeCount > strokeThresh and not decreasingInformation
            isKey1 = nFewerStrokesLA1 > sThresh1 and nFewerStrokesLA2 > sThresh2 and isPossibleKey

            # If more board cells and not mid-erase then key image
            if isKey1:
                print "Saving Key 1"
                keyImage.save("%s/Out/keyimg%s.jpg" % (self.directory, keyImageCount))
                keyImageCount += 1
                decreasingInformation = True

            elif deviationLA1 < devThreshSing:
                decreasingInformation = False

            # Cut and paste necessary cells
            keyImage.updateCleanWith(imLookAhead1)

            keyImage.save("%s/Out/debug%s.jpg" % (self.directory, debugCount))
            debugCount += 1
            imLookAhead1.free()
            imLookAhead2.free()


        keyImage.save("%s/Out/keyimg%s.jpg" % (self.directory, keyImageCount))
        print "Saved %s key images" % keyImageCount

    def generateLuminance(self, image):
        #image = self.images[0]
        for x in xrange(self.cpr):
            for y in xrange(self.cpc):
                hist = image.cellAt(x, y).histogram()
                self.histograms[x][y] += hist

        for x in xrange(self.cpr):
            for y in xrange(self.cpc):
                largest = max(self.histograms[x][y])
                lum = numpy.where(self.histograms[x][y] == largest)[0][0]
                self.histograms[x][y] = lum
        pImage.setIwMatrix(self.histograms)

    def generateLuminance2(self):
        
        count = 1
        total = len(self.images)
        for image in self.images:
            print count
            count += 1
            for x in xrange(self.cpr):
                for y in xrange(self.cpc):
                    hist = image.cellAt(x, y).histogram()
                    self.histograms[x][y] += hist
            image.free()

        for x in xrange(self.cpr):
            for y in xrange(self.cpc):
                largest = max(self.histograms[x][y])
                lum = numpy.where(self.histograms[x][y] == largest)[0][0]
                self.histograms[x][y] = lum

        pImage.setIwMatrix(self.histograms)

    def classifyCells(self):
        
        i = 1
        for image in self.images:
            image.load()
            image.classifyCells()
            #image.save("%s/Out/out%.2d.jpg" % (self.directory, i))
            image.free()
            
            print "Finished image %s of %s" % (i, len(self.images))
            i = i + 1

