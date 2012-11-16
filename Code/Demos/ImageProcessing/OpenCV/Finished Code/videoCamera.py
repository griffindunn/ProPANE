import cv

cv.NamedWindow("camera", 1)
capture = cv.CaptureFromCAM(0)
i = 0
while True:
    img = cv.QueryFrame(capture)
    cv.ShowImage("camera", img)
    i += 1
    if cv.WaitKey(10) == 27:
        break
cv.DestroyWindow("camera")
