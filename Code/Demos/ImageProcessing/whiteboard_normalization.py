# Remember to "Save Copy" to Code/Demos/Image_Processing at the end of each session

import Image
import ImageEnhance
import ImageOps

im = Image.open("whiteboard_cropped.jpg")
im_new = im.copy()
width=im.size[0]
height=im.size[1]
n=41
cell_width=width/n
cell_height=height/n
cell = [ [0 for i in range(n) ] for j in range(n) ]
cell_image = [ [0 for i in range(n) ] for j in range(n) ]
lum = [ [0 for i in range(n) ] for j in range(n) ]
hist = [ [0 for i in range(n) ] for j in range(n) ]
big = [ [0 for i in range(n) ] for j in range(n) ]
white = [ [0 for i in range(n) ] for j in range(n) ]
wb = [ [0 for i in range(n) ] for j in range(n) ]
bkgd = [ [0 for i in range(n) ] for j in range(n) ]
nsize = range(0,n)

for i in nsize:
    for j in nsize:
        cell[i][j]= ((j)*cell_width, i*cell_height, (j+1)*cell_width, (i+1)*cell_height)
        cell_image[i][j] = im.crop(cell[i][j])   

"""lum = im.convert("L")
#lum.show()
hist = lum.histogram()
#print hist
big = max(hist)
#print big
white = hist.index(big)
#print white

#wb = Image.new("L",(400,400),white)
#wb.show()"""

for i in nsize:
    for j in nsize:
        lum[i][j] = cell_image[i][j].convert("L")
        hist[i][j] = lum[i][j].histogram()
        big[i][j] = max(hist[i][j])
        white[i][j] = hist[i][j].index(big[i][j])
        wb[i][j] = Image.new("L",(cell_width,cell_height),white[i][j])
        bkgd[i][j] = wb[i][j].convert("RGB")
        im_new.paste(bkgd[i][j], cell[i][j])
        
#print white
im_new.show()



