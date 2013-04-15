import Image

imnum = 1

imfolder = range(imnum)
imname_out = [0 for i in imfolder]
imname = [0 for i in imfolder]
for i in range(1,imnum+1):
    #imname[i-1] = ("../../../../../ImageSets/keystone_correction/wide_board/test_image_(%s).jpg" % (i))
    imname[i-1] = ("../../../../../ImageSets/keystone_correction/3boards/lowres.jpg")

imseq = [Image.open(imname[0]),1]
width=imseq[0].size[0]
height=imseq[0].size[1]
del imseq

# X and Y (i,j) Coordinates of top and bottom left and right corners of whiteboard
#low res
##tli = 26
##tlj = 309
##bli = 34
##blj = 589
##bri = 1869
##brj = 713
##tri = 1870
##trj = 130

#lowres
width_new = 932
height_new = 584
#highres
##width_new = 2230
##height_new = 1400

for k in imfolder:
    imseq = [Image.open(imname[k]),1]

    # LOW RESOLUTION
    #left
    tli = 27
    tlj = 310
    bli = 33
    blj = 588
    bri = 389
    brj = 612
    tri = 379
    trj = 276

    fixedimg_left = imseq[0].transform((width_new,height_new),Image.QUAD,(tli,tlj,bli,blj,bri,brj,tri,trj))

    #middle 
    tli = 379
    tlj = 276
    bli = 389
    blj = 612
    bri = 940
    brj = 650
    tri = 936
    trj = 219

    fixedimg_mid = imseq[0].transform((width_new,height_new),Image.QUAD,(tli,tlj,bli,blj,bri,brj,tri,trj))

    #right
    tli = 936
    tlj = 219
    bli = 940
    blj = 650
    bri = 1867
    brj = 713
    tri = 1868
    trj = 129

    fixedimg_right = imseq[0].transform((width_new,height_new),Image.QUAD,(tli,tlj,bli,blj,bri,brj,tri,trj))
    
    # HIGH RESOLUTION
##    #left
##    tli = 67
##    tlj = 747
##    bli = 81
##    blj = 1412
##    bri = 935
##    brj = 1471
##    tri = 906
##    trj = 661
##
##    fixedimg_left = imseq[0].transform((width_new,height_new),Image.QUAD,(tli,tlj,bli,blj,bri,brj,tri,trj))
##
##
##    #middle 
##    tli = 906
##    tlj = 661
##    bli = 935
##    blj = 1471
##    bri = 2261
##    brj = 1553
##    tri = 2249
##    trj = 537
##
##    fixedimg_mid = imseq[0].transform((width_new,height_new),Image.QUAD,(tli,tlj,bli,blj,bri,brj,tri,trj))
##
##    #right
##    tli = 2253
##    tlj = 533
##    bli = 2261
##    blj = 1557
##    bri = 4481
##    brj = 1714
##    tri = 4483
##    trj = 314
##
##    fixedimg_right = imseq[0].transform((width_new,height_new),Image.QUAD,(tli,tlj,bli,blj,bri,brj,tri,trj))


##    width_new = max(tri,bri)-min(tli,bli)
##    height_new = max(blj,brj)-min(tlj,trj)
    
##    print width_new
##    print height_new

    fixedimg = Image.new('RGB',(width_new*3,height_new))
    fixedimg.paste(fixedimg_left,(0,0))
    fixedimg.paste(fixedimg_mid,(width_new,0))
    fixedimg.paste(fixedimg_right,(2*width_new,0))
    
##    fixedimg = imseq[0].transform((width_new,height_new),Image.QUAD,(tli,tlj,bli,blj,bri,brj,tri,trj))

    imname_out[k] = ("../../../../../ImageSets/keystone_correction/3boards/lowres_out_test.jpg")
    fixedimg.save(imname_out[k])
    del imseq
