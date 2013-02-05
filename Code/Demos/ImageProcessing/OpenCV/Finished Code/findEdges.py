import cv
import cv2
import numpy as np

img = cv2.imread('test.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

lowThreshold = 14
max_lowThreshold = 100
ratio = 3
kernel_size = 3

detected_edges = cv2.GaussianBlur(gray,(3,3),0)
detected_edges = cv2.Canny(detected_edges,lowThreshold,lowThreshold*ratio,apertureSize = kernel_size)
dst = cv2.bitwise_and(img,img,mask = detected_edges)  # just add some colours to edges from original image.


cv2.imwrite('cannydemo.jpg',dst)

inv = cv.LoadImageM('cannydemo.jpg')
cv.Threshold(inv, inv, 100, 255, cv.CV_THRESH_BINARY_INV)
#cv.Erode(inv, inv, iterations=1)

cv.SaveImage('cannydemo2.jpg', inv)


inv = cv.LoadImageM('cannydemo2.jpg')

cv.Erode(inv, inv)

cv.SaveImage('cannydemo3.jpg', inv)
