import cv

img = cv.LoadImageM("original.jpg")
size = cv.GetSize(img)
#cv.Dilate(img, img, iterations=1)
cv.Erode(img, img, iterations=1)
cv.SaveImage("dilateNew.jpg", img)

