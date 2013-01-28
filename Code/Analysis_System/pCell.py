import Image
import ImageEnhance
import ImageOps
import ImageStat
import numpy

class pCell(object):

    """Define enumeration for defining types of cells"""
    BOARD = 0
    STROKE = 1
    FOREGROUND = 2
    UNCLASSIFIED = 3
    

    """Cell width and height are constant for processing job so make static"""
    width = 0
    height = 0

    
    """Define constructor for cell giving x and y of top left corner"""
    def __init__(self, x, y, filename):
        self.x = x
        self.y = y
        self.filename = filename
        self.celltype = pCell.UNCLASSIFIED
        self.iw = 0


    """Static method for setting height and width"""
    @staticmethod
    def setHeightWidth(h, w):
        pCell.height = h
        pCell.width = w

    
    # This is where the math goes COLIN
    """Tell cell to classify itself"""
    def classify(self, Iw):
        im = Image.open(self.filename).convert("L")
        cell_bwimage = im.crop(self.boundaries())

        Tw = 2
        Tsig = 40
        I = ImageStat.Stat(cell_bwimage).mean[0]
        sig = ImageStat.Stat(cell_bwimage).stddev[0]
        #sigw = numpy.std(Iw)   #Ideally something like this
        sigw = 0.1  #Seems to work for this value
        
        if abs(I-Iw)/(sig+sigw) < Tw and sig/sigw < Tsig:
            self.celltype = pCell.BOARD

        elif abs(I-Iw)/(sig+sigw) < Tw and sig/sigw >= Tsig:
            self.celltype = pCell.STROKE

        else:
            self.celltype = pCell.FOREGROUND
  

    """Returns the boundaries of the cell (left, upper, right, lower)"""
    def boundaries(self):
        return (self.x, self.y, self.x + pCell.width, self.y + pCell.height)


    """Show the cell on screen (probably for debugging"""
    def show(self):
        im = Image.open(self.filename)
        region = self.boundaries()
        im.crop(region).show()

    def cellData(self):
        im = Image.open(self.filename)
        return im.crop(self.boundaries())

    def histogram(self):
        lum_hist = self.cellData().convert("L").histogram()
        return numpy.array(lum_hist)
