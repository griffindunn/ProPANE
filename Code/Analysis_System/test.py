from pCell import *
import pImage

CELLS_PER_ROW = 16
CELLS_PER_COLUMN = 16


image = pImage.pImage("test_images/test_image1.jpg")
image.cellify(CELLS_PER_ROW, CELLS_PER_COLUMN)

for x in range(CELLS_PER_ROW):
    for y in range(CELLS_PER_COLUMN):
        if x == 5 or y == 10:
            image.enhanceCell(x, y, 2.0)

image.show()

