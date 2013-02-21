from pImage import pImage
import pCell
from pCell import *
import glob
import numpy

class pImageSequence(object):

    def __init__(self, directory, CELLS_PER_ROW, CELLS_PER_COLUMN):
        self.directory = directory
        self.images = []
        self.cpr = CELLS_PER_ROW
        self.cpc = CELLS_PER_COLUMN

        self.histograms = [[numpy.zeros(256) for i in xrange(self.cpc)] for i in xrange(self.cpr)]

        for jpg in glob.glob("%s/*.jpg" % self.directory):
            pImg = pImage(jpg)
            pImg.cellify(self.cpr, self.cpc)
            self.images.append(pImg)

    def generateLuminance(self):
        
        count = 1
        total = len(self.images)
        for image in self.images:
            print count
            count += 1
            for x in xrange(self.cpr):
                for y in xrange(self.cpc):
                    hist = image.cells[x][y].histogram()
                    self.histograms[x][y] += hist
        image.im.free()

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
            image.im.save("./test_images/Out/out%.2d.jpg" % i)
            image.im.free()
            
            print "Finished image %s of %s" % (i, len(self.images))
            i = i + 1

