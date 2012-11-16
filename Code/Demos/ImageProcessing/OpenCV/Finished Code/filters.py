import cv
import cv2

img = cv.LoadImageM("original.jpg")

#cv.Dilate(img, img, iterations=1)
#cv.Erode(img, img, iterations=1)

cv.SaveImage("medianBlur.jpg", img)

