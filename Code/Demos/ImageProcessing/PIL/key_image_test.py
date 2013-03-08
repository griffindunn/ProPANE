import Image
import copy
import ImageEnhance as ENH
import time
import ImageFilter as IF
import ImageChops as IC

start = time.time()

# Check set number, imnum

imnum = 4

imfolder = range(imnum)

keyimg = Image.open("../../../../../ImageSets/keyimages/keyimg.jpg")

width = 0
height = 0
cell_width = 0
cell_height = 0
n=60
nsize = range(n)
width = keyimg.size[0]
height = keyimg.size[1]
cell_width = width/n
cell_height = height/n
Iw = [[0 for i in nsize] for j in nsize]
new_Iw = [[0 for i in nsize] for j in nsize]
cell = [[0 for i in nsize] for j in nsize]
out = 0
pos_step = 0.01
neg_step = 0.001
count = 1

for i in nsize:
    for j in nsize:        
          cell[i][j]= (j*cell_width, i*cell_height, (j+1)*cell_width, (i+1)*cell_height)
          cell_image = keyimg.crop(cell[i][j])
          lum = cell_image.convert("L")
          hist = lum.histogram()
          big = max(hist)
          Iw[i][j] = hist.index(big)

ref_Iw = copy.deepcopy(Iw)

imname = [0 for i in imfolder]
for k in imfolder:
    imname[k] = ("../../../../../ImageSets/keyimages/set2/keyimg%s.jpg" % (k))

for k in imfolder:    
    imseq = [Image.open(imname[k]),1]
    for i in nsize:
        for j in nsize:
              count = 1
              cell_image = imseq[0].crop(cell[i][j])
              lum = cell_image.convert("L")
              hist = lum.histogram()
              big = max(hist)
              Iw[i][j] = hist.index(big)
              if Iw[i][j] <= ref_Iw[i][j]:
                sign = 1
                step = pos_step
              elif Iw[i][j] > ref_Iw[i][j]:
                sign = -1
                step = neg_step
              temp = ENH.Brightness(cell_image)
              new_Iw[i][j] = copy.deepcopy(Iw[i][j])
              while abs(ref_Iw[i][j]-new_Iw[i][j]) != 0:
              #while Iw[i][j] != ref_Iw:
                #print "pass",count
                out = temp.enhance(1+count*step*sign)
                count = count + 1
                while_lum = out.convert("L")
                while_hist = while_lum.histogram()
                while_big = max(while_hist)
                new_Iw[i][j] = while_hist.index(while_big)
                #print Iw[i][j]
                if (sign > 0 and (new_Iw[i][j]-ref_Iw[i][j])>0):
                  #count = count - 1
                  step = pos_step
                  sign = sign*-1
                  
                elif (sign < 0 and (new_Iw[i][j]-ref_Iw[i][j])<0):
                  #count = count - 1
                  step = neg_step
                  sign = sign*-1
                if new_Iw[i][j] == 255 or new_Iw[i][j] == 0:
                  break
              imseq[0].paste(out,cell[i][j])
              #print "cell (%s,%s) done" % (i,j)
        print "row %s done" % (i)
    imname_out = ("../../../../../ImageSets/keyimages/keyimg_balanced%s.jpg" % (k))
    imseq[0].save(imname_out)
    print "image %s done" % (k)
    del imseq[0]
    
end = time.time()
print "Time elapsed %s" % (end-start)          

    
                      
            
            

