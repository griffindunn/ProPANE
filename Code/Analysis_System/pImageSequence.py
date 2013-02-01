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

        for jpg in glob.glob("%s/*.jpg" % self.directory):
            pImg = pImage(jpg)
            pImg.cellify(self.cpr, self.cpc)
            self.images.append(pImg)

    def generateLuminance(self):
        print "Generating luminance values"

        for x in range(self.cpr):
            for y in range(self.cpc):
                self.generateLuminanceForCell(x,y)


    def generateLuminanceForCell(self, x, y):

        lum_hist = numpy.zeros(256)
        for image in self.images:
            lum_hist += image.cells[x][y].histogram()

        largest = max(lum_hist)
        luminance = numpy.where(lum_hist == largest)[0][0]

        #print "Luminance for (%s, %s): %s" %(x,y,luminance)

        for image in self.images:
            image.cells[x][y].iw = luminance 

    def classifyCells(self):
        print "Classifying cells"

        for image in self.images:
            for x in range(self.cpr):
                for y in range(self.cpc):
                    image.cells[x][y].classify()

                    if image.cells[x][y].celltype == pCell.STROKE:
                        image.enhanceCell(x,y,2.0)


