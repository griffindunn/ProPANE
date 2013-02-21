import ImageEnhance
import Image
from pCell import *
from pImgMgr import pImgMgr

class pImage(object):


    def __init__(self, filename):
        self.filename = filename
        self.im = pImgMgr(filename)
        self.width, self.height = self.im.getBW().size
        self.im.free()
        self.boardCount = 0
        self.strokeCount = 0
        self.foreCount = 0

    @staticmethod
    def setIwMatrix(IwMatrix):
        pImage.IwMatrix = IwMatrix

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
        self.cells = [[0 for i in xrange(cellsPerColumn)] for i in xrange(cellsPerRow)]

        for x in xrange(cellsPerRow):
            for y in xrange(cellsPerColumn):
                self.cells[x][y] = pCell(x * pCell.width, y * pCell.height, self.im)

    def classifyCells(self):

        for x in xrange(self.cellsPerRow):
            for y in xrange(self.cellsPerColumn):
                cellType = self.cells[x][y].classify(pImage.IwMatrix[x][y])

        
        print "Initial Pass complete"

        for x in xrange(self.cellsPerRow):
            for y in xrange(self.cellsPerColumn):
                cellType = self.cells[x][y].celltype
                nBoard, nStroke, nForeground = self.getNeighboringCells(x,y)

                if cellType == pCell.FOREGROUND and nForeground < 3:
                    pass #self.cells[x][y].celltype = pCell.STROKE
                elif cellType == pCell.STROKE and nForeground > 1:
                    pass #self.cells[x][y].celltype = pCell.FOREGROUND
                
                if cellType == pCell.STROKE:
                    self.strokeCount += 1
                    self.enhanceCell(x, y, 2)
                elif cellType == pCell.FOREGROUND:
                    self.foreCount += 1
                    self.enhanceCell(x,y,0)
                else:
                    self.boardCount += 1

        


    """Changes the brightness factor of the cell given by (x,y) by enhanceFactor""" 
    def enhanceCell(self, x, y, enhanceFactor):
        #print "Enhancing"
        enhanceCell = ImageEnhance.Brightness(self.cells[x][y].cellData())
        enhanceCell = enhanceCell.enhance(enhanceFactor)
        self.im.getColor().paste(enhanceCell, self.cells[x][y].boundaries)
        #print "Enhanced"

    """ Helper functions grab cell type for neighboring cells """
    def cellAboveType(self, x, y):
        above_y = y - 1
        try:
            return self.cells[x][above_y].celltype
        except IndexError:
            return pCell.UNCLASSIFIED


    def cellBelowType(self, x, y):
        below_y = y + 1
        try:
            return self.cells[x][below_y].celltype
        except IndexError:
            return pCell.UNCLASSIFIED

    def cellLeftType(self, x, y):
        left_x = x - 1
        try:
            return self.cells[left_x][y].celltype
        except IndexError:
            return pCell.UNCLASSIFIED

    def cellRightType(self, x, y):
        right_x = x + 1
        try:
            return self.cells[right_x][y].celltype
        except IndexError:
            return pCell.UNCLASSIFIED

    """ Returns count of cell types (board, stroke, foreground) """
    def getNeighboringCells(self, x, y):
        neighborTypes = []
        neighborTypes.append(self.cellAboveType(x,y))
        neighborTypes.append(self.cellAboveType(x + 1,y))
        neighborTypes.append(self.cellAboveType(x - 1,y))
        neighborTypes.append(self.cellBelowType(x,y))
        neighborTypes.append(self.cellBelowType(x + 1,y))
        neighborTypes.append(self.cellBelowType(x - 1,y))
        neighborTypes.append(self.cellLeftType(x,y))
        neighborTypes.append(self.cellRightType(x,y))
        
        nBoard = neighborTypes.count(pCell.BOARD)
        nStroke = neighborTypes.count(pCell.STROKE)
        nForeground = neighborTypes.count(pCell.FOREGROUND)

        return (nBoard, nStroke, nForeground)


    """Shows the image in the default system viewer"""
    def show(self):
        self.im.getColor().show()

