import cv
from time import sleep

cv.NamedWindow("camera", 1)
capture = cv.CaptureFromCAM(0)

DELAY_TIME = 1500

i = 0
while i < 10:
    img = cv.QueryFrame(capture)
    cv.SaveImage("test1.jpg", img)
    cv.ShowImage("camera", img)
    i += 1
    if cv.WaitKey(10) == 27:
        break
cv.DestroyWindow("camera")
sleep(5)
img2 = cv.QueryFrame(capture)
cv.SaveImage("testb.jpg", img2)

