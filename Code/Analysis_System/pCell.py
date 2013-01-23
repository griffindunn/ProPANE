import Image

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


    """Static method for setting height and width"""
    @staticmethod
    def setHeightWidth(h, w):
        pCell.height = h
        pCell.width = w

    
    # This is where the math goes COLIN
    """Tell cell to classify itself"""
    def classify(self): 
        pass


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

