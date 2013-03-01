import ImageEnhance
import Image
from pCell import *
from pImgMgr import pImgMgr

class pImage(object):
    
    width = 0
    height = 0

    def __init__(self, filename):
        self.filename = filename
        self.im = pImgMgr(filename)
        self.boardCount = 0
        self.strokeCount = 0
        self.foreCount = 0

    def makeDefault(self):
        pImage.width, pImage.height = self.im.getColor().size


    @staticmethod
    def setIwMatrix(IwMatrix):
        pImage.IwMatrix = IwMatrix

    def pasteCell(self, cell, x, y):
        replacedType = self.cellAt(x,y).celltype
        if replacedType == pCell.BOARD:
            self.boardCount -= 1
        elif replacedType == pCell.STROKE:
            self.strokeCount -= 1
        else:
            self.foreCount -= 1

        replacingType = cell.celltype
        if replacingType == pCell.BOARD:
            self.boardCount += 1
        elif replacingType == pCell.STROKE:
            self.strokeCount += 1
        else:
            self.foreCount += 1
        
        self.cells[x][y] = cell


    """Generate pCells for image given number of cells for row and column"""    
    def cellify(self, cellsPerRow, cellsPerColumn):
        # These might be needed later
        self.cellsPerRow = cellsPerRow
        self.cellsPerColumn = cellsPerColumn

        cellWidth = pImage.width/cellsPerRow
        cellHeight = pImage.height/cellsPerColumn
        
        # Set the width and height of cells 
        pCell.setHeightWidth(cellHeight, cellWidth)

        # Initialize matrix of cells
        self.cells = [[0 for i in xrange(cellsPerColumn)] for i in xrange(cellsPerRow)]

        for x in xrange(cellsPerRow):
            for y in xrange(cellsPerColumn):
                self.cells[x][y] = pCell(x * pCell.width, y * pCell.height, self.im)

    def classifyCells(self, cell_type = None):

        if cell_type != None:
            for x in xrange(self.cellsPerRow):
                for y in xrange(self.cellsPerColumn):
                    self.cellAt(x, y).celltype = cell_type
            return 


        for x in xrange(self.cellsPerRow):
            for y in xrange(self.cellsPerColumn):
                cellType = self.cells[x][y].classify(pImage.IwMatrix[x][y])

        
        print "    Initial Pass complete"
        self.secondPass()
        print "    Second pass complete"
        self.thirdPass()
        print "    Third pass complete"
        self.fourthPass()
        print "    Fourth pass complete"
        self.enhancePass(False)
        print "    Enhance pass complete"

                

    def secondPass(self):
        for x in xrange(self.cellsPerRow):
            for y in xrange(self.cellsPerColumn):
                cellType = self.cells[x][y].celltype
                nBoard, nStroke, nForeground = self.getNeighboringCells(x,y)


                if cellType == pCell.FOREGROUND and nForeground < 3:
                    self.cells[x][y].celltype = pCell.STROKE

    def thirdPass(self):
        for x in xrange(self.cellsPerRow):
            for y in xrange(self.cellsPerColumn):
                cellType = self.cells[x][y].celltype
                nBoard, nStroke, nForeground = self.getNeighboringCells(x,y)

                if cellType == pCell.STROKE and nForeground >= 2:
                    self.cells[x][y].celltype = pCell.FOREGROUND

    def fourthPass(self):
        for y in xrange(self.cellsPerColumn):
            for x in xrange(self.cellsPerRow):
                nBoard, nStroke, nForeground = self.getNeighboringCells(x,y)

                if nForeground >= 3:
                    self.cells[x][y].celltype = pCell.FOREGROUND

    def enhancePass(self, shouldEnhance):
        for x in xrange(self.cellsPerRow):
            for y in xrange(self.cellsPerColumn):
                cellType = self.cells[x][y].celltype
                if cellType == pCell.STROKE:
                    self.strokeCount += 1

                    if shouldEnhance:
                        self.enhanceCell(x, y, 2)
                elif cellType == pCell.FOREGROUND:
                    self.foreCount += 1

                    if shouldEnhance:
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
        if above_y < 0 or x < 0 or x >= self.cellsPerRow:
            return pCell.UNCLASSIFIED
        return self.cells[x][above_y].celltype


    def cellBelowType(self, x, y):
        below_y = y + 1
        if below_y >= self.cellsPerColumn or x < 0 or x >= self.cellsPerRow:
            return pCell.UNCLASSIFIED
        return self.cells[x][below_y].celltype

    def cellLeftType(self, x, y):
        left_x = x - 1
        if left_x < 0 or y < 0 or y >= self.cellsPerColumn:
            return pCell.UNCLASSIFIED
        return self.cells[left_x][y].celltype

    def cellRightType(self, x, y):
        right_x = x + 1
        if right_x >= self.cellsPerRow or y < 0 or y >= self.cellsPerColumn:
            return pCell.UNCLASSIFIED
        return self.cells[right_x][y].celltype

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

    def save(self, filename):
        image = self.im.getColor()
        for x in xrange(self.cellsPerRow):
            for y in xrange(self.cellsPerColumn):
                cell = self.cells[x][y]
                image.paste(cell.cellData(), cell.boundaries)

        self.im.save(filename)

    def cellAt(self, x, y):
        return self.cells[x][y]

    def free(self):
        self.im.free()

