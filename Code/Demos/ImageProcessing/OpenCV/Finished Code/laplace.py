import cv

original = cv.LoadImageM("original.jpg", 1)
dst = cv.CreateImage(cv.GetSize(original), cv.IPL_DEPTH_16S, 3)
laplace = cv.Laplace(original, dst)
cv.SaveImage("laplace.jpg", dst)
