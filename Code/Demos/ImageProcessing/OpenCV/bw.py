import cv

img = cv.LoadImageM("car.png")

grey = cv.CreateImage(cv.GetSize(img),8,1)
cv.CvtColor(img, grey, cv.CV_BGR2GRAY)

cv.EqualizeHist(grey, grey)

#cv.Smooth(grey, grey, cv.CV_MEDIAN)

cv.SaveImage("bwCar.png", grey)


