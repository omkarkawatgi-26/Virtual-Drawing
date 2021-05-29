import cv2
import numpy as np


def empty(a):
    pass

cv2.namedWindow("TraceBars")
cv2.resizeWindow("TraceBars",640,240)
cv2.createTrackbar("Hue min","TraceBars",0,179,empty)
cv2.createTrackbar("Hue max","TraceBars",179,179,empty)
cv2.createTrackbar("Sat min","TraceBars",0,255,empty)
cv2.createTrackbar("Sat max","TraceBars",255,255,empty)
cv2.createTrackbar("Val min","TraceBars",0,255,empty)
cv2.createTrackbar("Val max","TraceBars",255,255,empty)

def stackImages(scale,imgArray):
    rows = len(imgArray)
    cols = len(imgArray[0])
    rowsAvailable = isinstance(imgArray[0], list)
    width = imgArray[0][0].shape[1]
    height = imgArray[0][0].shape[0]
    if rowsAvailable:
        for x in range ( 0, rows):
            for y in range(0, cols):
                if imgArray[x][y].shape[:2] == imgArray[0][0].shape [:2]:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (0, 0), None, scale, scale)
                else:
                    imgArray[x][y] = cv2.resize(imgArray[x][y], (imgArray[0][0].shape[1], imgArray[0][0].shape[0]), None, scale, scale)
                if len(imgArray[x][y].shape) == 2: imgArray[x][y]= cv2.cvtColor( imgArray[x][y], cv2.COLOR_GRAY2BGR)
        imageBlank = np.zeros((height, width, 3), np.uint8)
        hor = [imageBlank]*rows
        hor_con = [imageBlank]*rows
        for x in range(0, rows):
            hor[x] = np.hstack(imgArray[x])
        ver = np.vstack(hor)
    else:
        for x in range(0, rows):
            if imgArray[x].shape[:2] == imgArray[0].shape[:2]:
                imgArray[x] = cv2.resize(imgArray[x], (0, 0), None, scale, scale)
            else:
                imgArray[x] = cv2.resize(imgArray[x], (imgArray[0].shape[1], imgArray[0].shape[0]), None,scale, scale)
            if len(imgArray[x].shape) == 2: imgArray[x] = cv2.cvtColor(imgArray[x], cv2.COLOR_GRAY2BGR)
        hor= np.hstack(imgArray)
        ver = hor
    return ver

WebCam = cv2.VideoCapture(0)
while True:
    rec,Frame = WebCam.read()
    imgHSV = cv2.cvtColor(Frame, cv2.COLOR_BGR2HSV)

    h_min = cv2.getTrackbarPos("Hue min","TraceBars")
    h_max = cv2.getTrackbarPos("Hue max","TraceBars")
    s_min = cv2.getTrackbarPos("Sat min","TraceBars")
    s_max = cv2.getTrackbarPos("Sat max","TraceBars")
    v_min = cv2.getTrackbarPos("Val min","TraceBars")
    v_max = cv2.getTrackbarPos("Val max","TraceBars")
    print(h_min,h_max,s_min,s_max,v_min,v_max)
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)

    imgResult = cv2.bitwise_and(Frame,Frame,mask = mask)
    imgstack = stackImages(1, [[Frame, imgHSV],[mask,imgResult]])
    cv2.imshow("stacked images", imgstack)

    cv2.waitKey(1)















