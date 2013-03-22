# Takes key images and makes them pure white and black

import Image
import ImageEnhance
import ImageOps
import ImageStat
import numpy
import time
from operator import xor
import gc
import copy

from movingaverage import movingaverage
start = time.time()
print "opening images"
imnum = 1

imfolder = range(imnum)
#imseq = [0 for i in imfolder]
imname = [0 for i in imfolder]
for i in range(0,imnum):
    imname[i] = ("../../../../../ImageSets/keyimages/keyimg%s.jpg" % (i))

red = Image.open("red.jpg")    
print "images open"

imseq = [Image.open(imname[0]),1]
    
Iw_image = imseq[0].convert("L")    

width = [0 for i in imfolder]
height = [0 for i in imfolder]
cell_width = [0 for i in imfolder]
cell_height = [0 for i in imfolder]

n=60


width=imseq[0].size[0]
height=imseq[0].size[1]
cell_width=width/n
cell_height=height/n

del imseq
    
cell = [[ 0 for i in range(n) ] for j in range(n)]
lum = []
hist = []
numpyhist = []
tothist = [[ 0 for i in range(n) ] for j in range(n)]
big = []
wb = [[ 0 for i in range(n) ] for j in range(n)]
Iw = [[ 0 for i in range(n) ] for j in range(n)]   #whiteboard color
#sigw = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
I = []
sig = []
cell_bwimage = []
temp_big = []
temp_Iw = [[ 0 for i in range(n) ] for j in range(n)]
big_cell = [[ [0 for k in imfolder ] for i in range(n+2) ] for j in range(n+2)]
Tw_1 = []
Tsig_1 = []
relevant_cell = []
logic = []
temp = []
stroke_count = [0 for k in imfolder]
foreground_count = [0 for k in imfolder]
temprary = []
surrounding_cells = []
local_strokes = []
local_foreground = []
loc_stroke_num = []
loc_foreground_num = []
filter_num = [1, 2]
Iout = []

mycount = 0


nsize = range(0,n)

print "calculating image parameters"
print "defining cells"

for k in imfolder:
    for i in nsize:
        for j in nsize:        
            cell[i][j]= (j*cell_width, i*cell_height, (j+1)*cell_width, (i+1)*cell_height)
            #cell_image[i][j][k] = [imseq[k].crop(cell[i][j]),1]

print "finding Iw"

# IDEAL ######
mycount = 0

print "creating histograms"
enough_memory = True
#for k in imfolder:
for k in [0]:
    mycount += 1
    print mycount
    imseq = [Image.open(imname[k]),1]
    for i in nsize:       
        for j in nsize:
            enough_memory = True
            while enough_memory:
                try:
                    cell_image = imseq[0].crop(cell[i][j])
                    #temprary = ImageEnhance.Brightness(cell_image)
                    #cell_image = temprary.enhance(0.5)
                    enough_memory = False
                    lum = cell_image.convert("L")
                except MemoryError:
                    print "Memory Error caught"
                    gc.collect()
                    enough_memory = True
                    
            hist = lum.histogram()
            #numpyhist = numpy.array(hist)
            #tothist[i][j] += numpyhist
            ##TEMP##

            big = max(hist)
            Iw[i][j] = hist.index(big)
            wb[i][j] = Image.new("L",(cell_width,cell_height),Iw[i][j])
            Iw_image.paste(wb[i][j], cell[i][j])
            ##TEMP##
    del imseq[0]
    
##for i in nsize:
##    for j in nsize:
##        big = max(tothist[i][j])
##        Iw[i][j] = numpy.where(tothist[i][j] == big)
##        wb[i][j] = Image.new("L",(cell_width,cell_height),Iw[i][j][0][0])
##        Iw_image.paste(wb[i][j], cell[i][j])
        
imname_new = ("../../../../../ImageSets/Norm_out/test_image_Iw.jpg")
Iw_image.save(imname_new)

imname_out = [0 for i in imfolder]
for k in range(0,imnum):
    imname_out[k] = ("../../../../../ImageSets/Norm_out/norm_out_%s.jpg" % (k))
print "Normalizing Images"
mycount = 0

def normalization (x):
    if x < 5:
        x = 255
    if Iw[i][j] == 0:
        Iw[i][j] = 255
    return min([255,x*255/Iw[i][j]])

for k in imfolder:
    mycount += 1
    print mycount
    imseq = [Image.open(imname[k]),1]
    imseq = [imseq[0].convert("L"),1]
    for i in nsize:
        for j in nsize:
            cell_image = imseq[0].crop(cell[i][j])
            #temprary = ImageEnhance.Brightness(cell_image)
            #cell_image = temprary.enhance(0.9)
            #norm_image = cell_image.point(lambda x: min([255,x*255/Iw[i][j]]))
            norm_image = cell_image.point(lambda x: normalization(x))
            imseq[0].paste(norm_image, cell[i][j])
    imseq[0].save(imname_out[k])
    del imseq[0]
    
