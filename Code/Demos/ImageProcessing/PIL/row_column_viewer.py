import Image
import ImageEnhance

pic = Image.open("../../../../../ImageSets/Test_out/test_out_5.jpg")
#pic = Image.open("P1010053crop.jpg")

width = pic.size[0]
height = pic.size[1]
n=60
cell_width=width/n
cell_height = height/n

cell = [ [0 for i in range(n) ] for j in range(n) ]
cell_image = [ [0 for i in range(n) ] for j in range(n) ]




nsize = range(0,n)

for i in nsize:
    for j in nsize:
        cell[i][j]= ((j)*cell_width, i*cell_height, (j+1)*cell_width, (i+1)*cell_height)
        cell_image[i][j] = pic.crop(cell[i][j])

choice = raw_input("row or column?")
number = raw_input("Which %s?" % (choice))

index = int(float(number))  

if choice == "row":

    Row_disp = Image.new("RGB",(width,cell_height),None)
    single_row = [ 0 for j in range(n) ]

    for i in nsize:
        single_row[i]= (i*cell_width, 0, (i+1)*cell_width, cell_height)
    for i in nsize:
        Row_disp.paste(cell_image[index][i], single_row[i])

    for i in range(0,n,2): 
        temp = ImageEnhance.Brightness(cell_image[index][i])
        temp = temp.enhance(2.0)
        Row_disp.paste(temp, single_row[i])

    Row_disp.show()

elif choice == "column":

    Column_disp = Image.new("RGB",(cell_width,height),None)
    single_column = [ [0] for j in range(n)] 

    for i in nsize:
        single_column[i]= (0, i*cell_height, cell_width, (i+1)*cell_height)
    for i in nsize:
        Column_disp.paste(cell_image[i][index], single_column[i])

    for i in range(0,n,2): 
        temp = ImageEnhance.Brightness(cell_image[i][index])
        temp = temp.enhance(2.0)
        Column_disp.paste(temp, single_column[i])       

    Column_disp.show()

else:
    print "error"
