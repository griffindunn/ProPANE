import ImageEnhance
import Image
from pCell import *
from pImgMgr import pImgMgr
import sys
import os
import pickle

class pImage(object):
    
    width = 0
    height = 0
    y_start = None
    y_end = None
    
    def __init__(self, filename):
        self.boardCount = 0
        self.strokeCount = 0
        self.foreCount = 0
        self.filename = filename
        self.cellFile = "%sout" % filename
        self.im = pImgMgr(filename)
        self.cells = None

    def load(self):
        pklFl = open(self.cellFile, 'r')
        self.cells = pickle.load(pklFl)
        pklFl.close()
        os.remove(self.cellFile)

    def makeDefault(self):
        pImage.width, pImage.height = self.im.getColor().size

    def setBoardArea(self):
        y1 = 0
        y2 = 0
        for x in xrange(self.cellsPerRow):
            y_start, y_end = self.getBoardInColumn(x)
            y1 += y_start * 1.0 /self.cellsPerRow
            y2 += y_end   * 1.0 /self.cellsPerRow

        pImage.y_start = int(round(y1))
        pImage.y_end   = int(round(y2))
        print "start %s end %s" % (y1, y2)

    def getBoardInColumn(self, column):
        y_start = 0
        while self.cellAt(column, y_start).celltype != pCell.BOARD or self.cellAt(column, y_start + 1).celltype != pCell.BOARD or self.cellAt(column, y_start + 2).celltype != pCell.BOARD :
            y_start += 1


        y_end = self.cellsPerColumn - 1
        while self.cellAt(column, y_end).celltype != pCell.BOARD or self.cellAt(column, y_end - 1).celltype != pCell.BOARD or self.cellAt(column, y_end - 2).celltype != pCell.BOARD:
            y_end -= 1

        return (y_start, y_end)


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

        if pImage.y_start == None:
            pImage.y_start = 0
            pImage.y_end = self.cellsPerColumn - 1

        cellWidth = pImage.width/cellsPerRow
        cellHeight = pImage.height/cellsPerColumn
        
        # Set the width and height of cells 
        pCell.setHeightWidth(cellHeight, cellWidth)

        # Initialize matrix of cells
        self.cells = [[0 for i in xrange(cellsPerColumn)] for i in xrange(cellsPerRow)]

        for x in xrange(cellsPerRow):
            for y in xrange(cellsPerColumn):
                self.cells[x][y] = pCell(x * pCell.width, y * pCell.height, self.im)

    """ Copies non-foreground cells from arg image to called image """
    def updateCleanWith(self, image):
        for x in xrange(self.cellsPerRow):
            for y in xrange(self.cellsPerColumn):
                newCellType = image.cellAt(x,y).celltype
                if newCellType != pCell.FOREGROUND:
                    cell = image.cellAt(x,y)
                    self.pasteCell(cell, x, y)


    def nFewerStrokesThan(self, image):
        nFewerStrokes = 0
        for x in xrange(self.cellsPerRow):
            for y in xrange(self.cellsPerColumn):
                if image.cellAt(x,y).celltype == pCell.STROKE and self.cellAt(x,y).celltype == pCell.BOARD:
                    nFewerStrokes += 1
                elif self.cellAt(x,y).celltype == pCell.STROKE and image.cellAt(x,y).celltype == pCell.BOARD:
                    nFewerStrokes -= 1

        return nFewerStrokes


    def classifyCells(self, noForeground = False):

        for x in xrange(self.cellsPerRow):
            for y in range(pImage.y_start, pImage.y_end + 1):
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

        if noForeground:
            for x in xrange(self.cellsPerRow):
                for y in range(pImage.y_start, pImage.y_end + 1):
                    cell = self.cellAt(x, y)
                    if cell.celltype == pCell.FOREGROUND:
                        self.foreCount -= 1
                        self.strokeCount += 1
                        cell.celltype = pCell.STROKE
                

    def secondPass(self):
        for x in xrange(self.cellsPerRow):
            for y in range(pImage.y_start, pImage.y_end + 1):
                cellType = self.cells[x][y].celltype
                nBoard, nStroke, nForeground = self.getNeighboringCells(x,y)


                if cellType == pCell.FOREGROUND and nForeground < 3:
                    self.cells[x][y].celltype = pCell.STROKE

    def thirdPass(self):
        for x in xrange(self.cellsPerRow):
            for y in range(pImage.y_start, pImage.y_end + 1)[::-1]:
                cellType = self.cells[x][y].celltype
                nBoard, nStroke, nForeground = self.getNeighboringCells(x,y)

                if cellType == pCell.STROKE and nForeground >= 3:
                    self.cells[x][y].celltype = pCell.FOREGROUND

    def fourthPass(self):
        for y in range(pImage.y_start, pImage.y_end + 1)[::-1]:
            for x in xrange(self.cellsPerRow):
                cellType = self.cells[x][y].celltype
                nBoard, nStroke, nForeground = self.getNeighboringCells(x,y)

                if cellType == pCell.STROKE and nForeground >= 4:
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
                elif cellType == pCell.UNCLASSIFIED:
                    self.enhanceCell(x,y,0.2)
                else:
                    self.boardCount += 1
        
    def cleanPass(self):
        print "running clean pass"
        for x in xrange(self.cellsPerRow):
            for y in xrange(self.cellsPerColumn):
                cellType = self.cells[x][y].celltype
                if cellType == pCell.STROKE:
                    self.strokeCount += 1
                    self.make2D(x, y)

                elif cellType == pCell.FOREGROUND:
                    self.foreCount += 1
                    self.makeWhite(x, y)
                    
                elif cellType == pCell.UNCLASSIFIED:
                    #self.enhanceCell(x,y,0.2)
                    self.makeWhite(x, y)
                else:
                    self.boardCount += 1
                    self.makeWhite(x, y)


    def makeWhite(self, x, y):
        #makeWhiteCell = ImageEnhance.Brightness(self.cells[x][y].cellData())
        #makeWhiteCell = makeWhiteCell.enhance(100)
        makeWhiteCell = self.cells[x][y].cellData().convert('L')
        lut = [255 if v < 254 else 0 for v in range(256)]
        makeWhiteCell = makeWhiteCell.point(lut, '1')
        self.im.getColor().paste(makeWhiteCell, self.cells[x][y].boundaries)

    def make2D(self, x, y):
        make2D = self.cells[x][y].cellData().convert('L')
        color = self.cells[x][y].cellData()
        stat = ImageStat.Stat(make2D)
		#average = stat.mean[0]
		#im = self.cells[x][y].cellData()
		#image = self.cells[x][y].cellData()
        pixels = make2D.load()
        colPix = color.load()
        width = self.cells[x][y].width
        height = self.cells[x][y].height
		#all_pixels = []
        for xx in range(width):
            for yy in range(height):
                cpixel = colPix[xx, yy]
                if round(sum(cpixel)/float(len(cpixel))) > stat.mean[0]:
                    color.putpixel((xx, yy), (255, 255, 255))
        #else:
        #all_pixels.append(0)
        #pixels[x,y] = (0, 0, 0)
        #pixels[x, y] = cpixel

		#hope = Image.fromarray(all_pixels, 'RGB')
		#stat = ImageStat.Stat(make2D)
		#lut = [255 if v > stat.mean[0] else 0 for v in range(256)]
		#make2D = make2D.point(lut, '1')
        make2D = make2D.point(lambda i: i > (stat.mean[0]-stat.stddev[0]/5) and 255)
		#invert = PIL.ImageOps.invert(make2D)
		#im.putdata(all_pixels)

        self.im.getColor().paste(color, self.cells[x][y].boundaries)

    

        

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

    def save(self, filename, keyimage = False):
        image = self.im.getColor()
        for x in xrange(self.cellsPerRow):
            for y in xrange(self.cellsPerColumn):
                cellType = self.cells[x][y].celltype
                if cellType == pCell.STROKE:
                    self.strokeCount += 1
                    if keyimage:
                        self.make2D(x, y)

                elif cellType == pCell.FOREGROUND:
                    self.foreCount += 1
                    if keyimage:
                        self.makeWhite(x, y)
                    
                elif cellType == pCell.UNCLASSIFIED:
                    if keyimage:
                        self.makeWhite(x, y)
                else:
                    self.boardCount += 1
                    if keyimage:
                        self.makeWhite(x, y)

        image.save(filename)

    def cellAt(self, x, y):
        return self.cells[x][y]

    def free(self):
        self.im.free()
        pklFl = open(self.cellFile, 'w')
        pickle.dump(self.cells, pklFl)
        pklFl.close()
        self.cells = None

