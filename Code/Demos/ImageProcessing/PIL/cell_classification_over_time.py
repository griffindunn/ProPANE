# Remember to "Save Copy" to Code/Demos/Image_Processing at the end of each session

#Currently only works for 1 band (L). Converts im from RGB to L.  Need it to work
#for 3 separate RGB bands

import os, sys
#image_path = os.path.abspath('../../../../Images/StandardImages')
#os.path.join(image_path)

import Image
import ImageEnhance
import ImageOps
import ImageStat
import numpy

imnum = 6
imfolder = range(imnum)
imseq = [0 for i in imfolder]
for i in range(3,9):
    imname = ("P101005%scrop.jpg" % (i))
    imseq[i-3] = Image.open(imname)

#im = Image.open("P1010054.jpg")
#im_new = im.copy()         #ideal
imseq_new = [0 for i in imfolder]
imseq_out = [0 for i in imfolder]
for i in imfolder:
    imseq_new[i] = imseq[i].convert("L")    #temporary
    imseq_out[i] = imseq[i].copy()

width = [0 for i in imfolder]
height = [0 for i in imfolder]
cell_width = [0 for i in imfolder]
cell_height = [0 for i in imfolder]

n=61

for i in imfolder:
    width[i]=imseq[i].size[0]
    height[i]=imseq[i].size[1]
    cell_width[i]=width[i]/n
    cell_height[i]=height[i]/n
    
cell = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
cell_image = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
lum = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
hist = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
numpyhist = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
tothist = [[ 0 for i in range(n) ] for j in range(n)]
big = [[ 0 for i in range(n) ] for j in range(n)]
#white = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
wb = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
bkgd = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
Iw = [[ 0 for i in range(n) ] for j in range(n)]   #whiteboard color
sigw = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
I = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
sig = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
wb_color = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
cell_bwimage = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]
temp_big = [[ 0 for i in range(n) ] for j in range(n)]
temp_Iw = [[ 0 for i in range(n) ] for j in range(n)]



nsize = range(0,n)

Tw = 2
Tsig = 40
cell_id = [[ [0 for k in imfolder ] for i in range(n) ] for j in range(n)]

for k in imfolder:
    for i in nsize:
        for j in nsize:        
            cell[i][j][k]= (j*cell_width[k], i*cell_height[k], (j+1)*cell_width[k], (i+1)*cell_height[k])
            cell_image[i][j][k] = imseq[k].crop(cell[i][j][k])

for k in imfolder:
    for i in nsize:
        for j in nsize:             
            lum[i][j][k] = cell_image[i][j][k].convert("L")
            hist[i][j][k] = lum[i][j][k].histogram()
            numpyhist[i][j][k] = numpy.array(hist[i][j][k])

for i in nsize:
    for j in nsize:
        for k in imfolder:
            tothist[i][j] += numpyhist[i][j][k]

for k in imfolder:
    for i in nsize:
        for j in nsize:
            big[i][j] = max(tothist[i][j])
            temp_big[i][j] = max(hist[i][j][5])  #temporary Iw calculation
            Iw[i][j] = numpy.where(tothist[i][j] == big[i][j])
            temp_Iw[i][j] = hist[i][j][5].index(temp_big[i][j]) #temporary Iw calculation
            wb[i][j][k] = Image.new("L",(cell_width[k],cell_height[k]),Iw[i][j][0][0])
            #bkgd[i][j] = wb[i][j].convert("RGB")       #ideal for RGB
            #im_new.paste(bkgd[i][j], cell[i][j])       #ideal for RGB
            imseq_new[k].paste(wb[i][j][k], cell[i][j][k])


for k in range(3,9):
    imname_new = ("test_images/P101005%s_new.jpg" % (k))
    imseq_new[k-3].save(imname_new)

bwim = [0 for k in imfolder]    
for k in imfolder:
    bwim[k] = imseq[k].convert("L")      #temporary
    
    
#sigw = ImageStat.Stat(im_new).stddev[0]
#sigw = 8


###WHY DOESN'T IT DETECT WHITEBOARD CELLS ANYMORE???####

for k in imfolder:
    for  i in nsize:
        for j in nsize:
            #sigw[i][j] = numpy.std(Iw[i][j])   #Ideally this
            #wb_color[i][j] = im_new.crop(cell[i][j])   #ideal for RGB
            cell_bwimage[i][j][k] = bwim[k].crop(cell[i][j][k])  #temporary
            sigw = 0.1

            #correct Iw is Iw[i][j][0][0]... temp_Iw is Iw[i][j] 

            
            I[i][j][k] = ImageStat.Stat(cell_bwimage[i][j][k]).mean
            sig[i][j][k] = ImageStat.Stat(cell_bwimage[i][j][k]).stddev
        
            if abs(I[i][j][k][0]-Iw[i][j][0][0])/(sig[i][j][k][0]+sigw) < Tw and sig[i][j][k][0]/sigw < Tsig:
                cell_id[i][j][k] = "whiteboard cell"

            elif abs(I[i][j][k][0]-Iw[i][j][0][0])/(sig[i][j][k][0]+sigw) < Tw and sig[i][j][k][0]/sigw >= Tsig:
                cell_id[i][j][k] = "stroke cell"
                temp = ImageEnhance.Brightness(cell_image[i][j][k])
                temp = temp.enhance(2.0)
                imseq_out[k].paste(temp, cell[i][j][k])

            else:
                cell_id[i][j][k] = "foreground object"
                temp = ImageEnhance.Brightness(cell_image[i][j][k])
                temp = temp.enhance(0)
                imseq_out[k].paste(temp, cell[i][j][k])

for k in range(3,9):
    imname_out = ("test_images/out_P101005%s.jpg" % (k))
    imseq_out[k-3].save(imname_out)
                                            

#for i in range(n):
	#print cell_id[i][15]
