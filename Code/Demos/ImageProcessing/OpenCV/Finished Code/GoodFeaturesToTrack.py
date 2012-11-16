import cv
img = cv.LoadImageM("car.png", cv.CV_LOAD_IMAGE_GRAYSCALE)
eig_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
temp_image = cv.CreateMat(img.rows, img.cols, cv.CV_32FC1)
for (x,y) in cv.GoodFeaturesToTrack(img, eig_image, temp_image, 10, 0.04, 1.0, useHarris = True):
   print "good feature at", x,y
