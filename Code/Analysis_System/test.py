from pCell import *
import pImage
import time

CELLS_PER_ROW = 32
CELLS_PER_COLUMN = 32


image = pImage.pImage("test_images/test_image1.jpg")
image.cellify(CELLS_PER_ROW, CELLS_PER_COLUMN)

print "Starting for loop"
start = time.time()

print image.cells[10][10].histogram()

end = time.time()

print "Time elapsed %s" % (end -start)



