import ImageEnhance
import Image
from pCell import *

class pImage(object):

    def __init__(self, filename):
        self.filename = filename
        self.im = Image.open(self.filename)
        self.width, self.height = self.im.size


    """Generate pCells for image given number of cells for row and column"""    
    def cellify(self, cellsPerRow, cellsPerColumn):
        # These might be needed later
        self.cellsPerRow = cellsPerRow
        self.cellsPerColumn = cellsPerColumn

        cellWidth = self.width/cellsPerRow
        cellHeight = self.height/cellsPerColumn
        
        # Set the width and height of cells 
        pCell.setHeightWidth(cellHeight, cellWidth)

        # Initialize matrix of cells
        self.cells = [[0 for i in range(cellsPerColumn)] for i in range(cellsPerRow)]

        for x in range(cellsPerRow):
            for y in range(cellsPerColumn):
                self.cells[x][y] = pCell(x * pCell.width, y * pCell.height, self.im)

    """Changes the brightness factor of the cell given by (x,y) by enhanceFactor""" 
    def enhanceCell(self, x, y, enhanceFactor):
        #print "Enhancing"
        enhanceCell = ImageEnhance.Brightness(self.cells[x][y].cellData())
        enhanceCell = enhanceCell.enhance(enhanceFactor)
        self.im.paste(enhanceCell, self.cells[x][y].boundaries())
        #print "Enhanced"


    """Shows the image in the default system viewer"""
    def show(self):
        self.im.show()

