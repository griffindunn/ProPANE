from pImage import pImage
import pCell
from pCell import *
import glob
import numpy
from pImgMgr import pImgMgr

class pImageSequence(object):

    def __init__(self, directory, CELLS_PER_ROW, CELLS_PER_COLUMN):
        self.directory = directory
        self.images = []
        self.cpr = CELLS_PER_ROW
        self.cpc = CELLS_PER_COLUMN

        self.histograms = [[numpy.zeros(256) for i in xrange(self.cpc)] for i in xrange(self.cpr)]

        jpgs = glob.glob("%s/*.jpg" % self.directory)
        default = pImage(jpgs[0])
        default.makeDefault()

        
        for jpg in jpgs:
            pImg = pImage(jpg)
            pImg.cellify(self.cpr, self.cpc)
            self.images.append(pImg)

    @staticmethod
    def cert(cellForegroundPct, imageForegroundPct):
        a = 0.5
        cert = (1-a)*cellForegroundPct + a * imageForegroundPct
        return 1 - cert

    def findKeyImages(self):
        # Setup key image 
        keyImageCount = 0
        keyImage = pImage(self.images[0].filename)
        keyImage.cellify(self.cpr, self.cpc)
        keyImage.classifyCells(pCell.BOARD)

        maxDevPct = 10                   # Threshold for identifying key images
        decreasingInformation = False   # If stroke cells are becoming board cells
        debugCount = 1                  # Used to generate debugging images
        
        for image in self.images:
            
            # Check to see how many stroke cells are becoming board cells
            nFewerStrokes = 0
            for x in xrange(self.cpr):
                for y in xrange(self.cpc):
                    if keyImage.cellAt(x,y).celltype == pCell.STROKE and image.cellAt(x,y).celltype == pCell.BOARD:
                        nFewerStrokes += 1;

            # Calculate deviation of stroke cells
            deviation = nFewerStrokes * 100.0 / (keyImage.strokeCount + 1)
            print "Deviation %s decreasing %s" %(deviation, decreasingInformation)

            # If more board cells and not mid-erase then key image
            if deviation >= maxDevPct and not decreasingInformation:
                print "Saving images with %s fewer strokes (%s)" % (nFewerStrokes, deviation)
                keyImage.save("./test_images/Out/keyimg%s.jpg" % keyImageCount)
                keyImageCount += 1
                decreasingInformation = True

            elif deviation < maxDevPct:
                decreasingInformation = False



            # Cut and paste necessary cells
            for x in xrange(self.cpr):
                for y in xrange(self.cpc):
                    imCellType = image.cellAt(x,y).celltype
                    keyCellType = keyImage.cellAt(x,y).celltype

                    if imCellType != pCell.FOREGROUND:
                        cell = image.cellAt(x,y)
                        keyImage.pasteCell(cell, x, y)

            keyImage.save("./test_images/Out/debug%s.jpg" % debugCount)
            debugCount += 1
            image.free()


        keyImage.save("./test_images/Out/keyimg%s.jpg" % keyImageCount)

    def generateLuminance(self):
        
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
        print "Classifying cells"

        i = 1
        for image in self.images:
            image.classifyCells()
            image.save("./test_images/Out/out%.2d.jpg" % i)
            image.free()
            
            print "Finished image %s of %s" % (i, len(self.images))
            i = i + 1

