from pCell import *
import pImage
from pImageSequence import pImageSequence
import time

CELLS_PER_ROW = 64
CELLS_PER_COLUMN = 64

print "Starting for loop"
start = time.time()

imageSeq = pImageSequence("test_images/", CELLS_PER_ROW, CELLS_PER_COLUMN)

imageSeq.generateLuminance()
imageSeq.classifyCells()

for image in imageSeq.images:
    image.show()

end = time.time()

print "Time elapsed %s" % (end -start)



