import Image
import ImageEnhance

im = Image.open("wb_nickel_7_crop.jpg")
width=im.size[0]
height=im.size[1]
n=41
cell_width=width/n
cell_height=height/n
#cell = (n**2)*[0]
#cell_image = (n**2)*[0]
cell = [ [0 for i in range(n) ] for j in range(n) ]
cell_image = [ [0 for i in range(n) ] for j in range(n) ]

"""for i in range(0,n):
    for j in range(1,n+1):
        cell[x]= ((j-1)*cell_width, i*cell_height, j*cell_width, (i+1)*cell_height)
        cell_image[x] = im.crop(cell[x])
        x = x+1"""

for i in range(0,n):
    for j in range(0,n):
        cell[i][j]= ((j)*cell_width, i*cell_height, (j+1)*cell_width, (i+1)*cell_height)
        cell_image[i][j] = im.crop(cell[i][j])   

#for i,j below produces a checkerboard pattern

#Rotates every other image cell and displays result

"""for i in range(0,n):
    for j in range(i%2,n-(i%2),2): 
        temp = cell_image[i][j].transpose(Image.ROTATE_180)
        im.paste(temp, cell[i][j])
im.show()"""

#Changes contrast for cells in checkerboard pattern

"""for i in range(0,n):
    for j in range(i%2,n-(i%2),2): 
        enh = ImageEnhance.Contrast(cell_image[i][j])
        enh = enh.enhance(3.0)
        im.paste(enh, cell[i][j])
im.show()"""

#Changes brightness for cells in checkerboard pattern

for i in range(0,n):
    for j in range(i%2,n-(i%2),2): 
        temp = ImageEnhance.Brightness(cell_image[i][j])
        temp = temp.enhance(2.0)
        im.paste(temp, cell[i][j])
im.show()

