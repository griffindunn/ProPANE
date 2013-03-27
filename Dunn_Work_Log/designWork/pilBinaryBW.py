from PIL import Image
from PIL import ImageStat

image_file = Image.open("keyimg1.jpg")
image_file = image_file.convert('L') #make it greyscale
lut = [255 if v > 128 else 0 for v in range(256)]
out = image_file.point(lut, '1')
out.save('result.jpg')
stat = ImageStat.Stat(image_file)
print stat.mean[0]
print int(stat.mean[0])
