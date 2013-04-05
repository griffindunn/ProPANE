import Image

imnum = 1

imfolder = range(imnum)
imname_out = [0 for i in imfolder]
imname = [0 for i in imfolder]
for i in range(1,imnum+1):
    #imname[i-1] = ("../../../../../ImageSets/keystone_correction/wide_board/test_image_(%s).jpg" % (i))
    imname[i-1] = ("../../../../../ImageSets/keystone_correction/classroom.jpg")

imseq = [Image.open(imname[0]),1]
width=imseq[0].size[0]
height=imseq[0].size[1]
del imseq

# X and Y (i,j) Coordinates of top and bottom left and right corners of whiteboard
tli = 547
tlj = 228
bli = 546
blj = 441
bri = 1279
brj = 508
tri = 1279
trj = 174

width_new = max(tri,bri)-min(tli,bli)
height_new = max(blj,brj)-min(tlj,trj)

for k in imfolder:
    imseq = [Image.open(imname[k]),1]
    fixedimg = imseq[0].transform((width_new,height_new),Image.QUAD,(tli,tlj,bli,blj,bri,brj,tri,trj))
    imname_out[k] = ("../../../../../ImageSets/keystone_correction/classroom_out.jpg")
    fixedimg.save(imname_out[k])
    del imseq
