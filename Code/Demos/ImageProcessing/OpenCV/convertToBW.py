import cv2
import cv
import numpy as np


#img = cv.LoadImageM("originalb.jpg")
#cv.Erode(img, img, iterations=2)
#cv.SaveImage("originalc.jpg", img)

im_gray = cv2.imread("originalb.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)



(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
#(thresh, im_bw) = cv2.threshold(im_gray, 110, 255, cv2.THRESH_BINARY | cv2.THRESH_BINARY_INV)
#(thresh, im_bw) = cv2.threshold(im_gray, 128, 255, cv2.THRESH_BINARY_INV)

#thresh = 100
im_bw = cv2.threshold(im_gray, thresh, 255, cv2.THRESH_BINARY)[1]

cv2.imwrite('bwimage.jpg', im_bw)

#img = cv.LoadImageM("bwimage.jpg")
#cv.Dilate(img, img, iterations=2)
#cv.SaveImage("bwimage2.jpg", img)

#img = cv.LoadImageM("bwimage.jpg")
#cv.Erode(img, img, iterations=1)
#cv.SaveImage("bwimage.jpg", img)
