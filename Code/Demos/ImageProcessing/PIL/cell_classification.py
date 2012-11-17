# Remember to "Save Copy" to Code/Demos/Image_Processing at the end of each session

#Currently only works for 1 band (L). Converts im from RGB to L.  Need it to work
#for 3 separate RGB bands

import Image
import ImageEnhance
import ImageOps
import ImageStat

im = Image.open("../../../../Images/NickelImages/wb_nickel_7_crop.jpg")
#im_new = im.copy()
im_new = im.convert("L")
width=im.size[0]
height=im.size[1]
n=61
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
Iw = [ [0 for i in range(n) ] for j in range(n) ]
sigw = [ [0 for i in range(n) ] for j in range(n) ]
I = [ [0 for i in range(n) ] for j in range(n) ]
sig = [ [0 for i in range(n) ] for j in range(n) ]
wb_color = [ [0 for i in range(n) ] for j in range(n) ]
cell_bwimage = [ [0 for i in range(n) ] for j in range(n) ]


nsize = range(0,n)

Tw = 2
Tsig = 2
cell_id = [ [ "" for i in range(n) ] for j in range(n) ]

for i in nsize:
    for j in nsize:
        cell[i][j]= ((j)*cell_width, i*cell_height, (j+1)*cell_width, (i+1)*cell_height)
        cell_image[i][j] = im.crop(cell[i][j])   


for i in nsize:
    for j in nsize:
        lum[i][j] = cell_image[i][j].convert("L")
        hist[i][j] = lum[i][j].histogram()
        big[i][j] = max(hist[i][j])
        white[i][j] = hist[i][j].index(big[i][j])
        wb[i][j] = Image.new("L",(cell_width,cell_height),white[i][j])
        #bkgd[i][j] = wb[i][j].convert("RGB")
        #im_new.paste(bkgd[i][j], cell[i][j])
        im_new.paste(wb[i][j], cell[i][j])
#im_new.show()
bwim = im.convert("L")
#sigw = ImageStat.Stat(im_new).stddev[0]
sigw = 8
for  i in nsize:
        for j in nsize:
           
            #wb_color[i][j] = im_new.crop(cell[i][j])
            cell_bwimage[i][j] = bwim.crop(cell[i][j])
            Iw[i][j] = white[i][j]
           # sigw[i][j] = ImageStat.Stat(wb[i][j]).stddev
            
            I[i][j] = ImageStat.Stat(cell_bwimage[i][j]).mean
            sig[i][j] = ImageStat.Stat(cell_bwimage[i][j]).stddev
          
            if abs(I[i][j][0]-Iw[i][j])/(sig[i][j][0]+sigw) < Tw and sig[i][j][0]/sigw < Tsig:
               cell_id[i][j] = "whiteboard cell"

            elif abs(I[i][j][0]-Iw[i][j])/(sig[i][j][0]+sigw) < Tw and sig[i][j][0]/sigw >= Tsig:
               cell_id[i][j] = "stroke cell"
               temp = ImageEnhance.Brightness(cell_image[i][j])
               temp = temp.enhance(2.0)
               im.paste(temp, cell[i][j])

            else:
               cell_id[i][j] = "foreground object"
               temp = ImageEnhance.Brightness(cell_image[i][j])
               temp = temp.enhance(0)
               im.paste(temp, cell[i][j])
im.show()
                                            

#for i in range(n):
	#print cell_id[i][15]
