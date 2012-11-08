from PIL import Image
im = Image.open("car.png")
im.rotate(45).save("car2.png")

