import cv

img = cv.LoadImageM("p2.jpg")

grey = cv.CreateImage(cv.GetSize(img),8,1)

cv.CvtColor(img, grey, cv.CV_BGR2GRAY)

cv.Threshold(grey, grey, 100, 200, cv.CV_THRESH_BINARY)

cv.Threshold(grey, grey, 128, 255, cv.CV_THRESH_BINARY)

cv.Erode(grey, grey)

cv.SaveImage("equalCanny.jpg", grey)

