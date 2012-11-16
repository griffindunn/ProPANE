import cv
import cv2
import numpy as np



img = cv.LoadImageM("P1010058.jpg")
grey = cv.CreateImage(cv.GetSize(img),8,1)
cv.CvtColor(img, grey, cv.CV_BGR2GRAY)
cv.Smooth(grey, grey, cv.CV_MEDIAN)
cv.EqualizeHist(grey, grey)
cv.SaveImage("originalz.jpg", grey)


img = cv2.imread('originalz.jpg')
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
ret,thresh = cv2.threshold(gray,128,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

fg = cv2.erode(thresh,None,iterations = 1)

#bgt = cv2.dilate(thresh,None,iterations = 2)
ret,bg = cv2.threshold(fg,1,128,1)

marker = cv2.add(fg,bg)

marker32 = np.int32(marker)

cv2.watershed(img,marker32)
m = cv2.convertScaleAbs(marker32)

ret,thresh = cv2.threshold(m,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
res = cv2.bitwise_and(img,img,mask = (128-thresh))

cv2.imwrite("waterfalld.jpg", fg)
cv2.imwrite("waterfallb.jpg", res)
