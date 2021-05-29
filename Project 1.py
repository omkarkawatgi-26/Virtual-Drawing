import cv2
import numpy as np



def empty(a):
    pass
#Stack Function for stacking images
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

def getContours(img):
    contours , hierarchy = cv2.findContours(img,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
    x,y,w,h = 0,0,0,0

    for cnt in contours:
        #cv2.drawContours(imgCon,cnt,-1,(0,0,255),3)
        peri = cv2.arcLength(cnt,True)
        approx = cv2.approxPolyDP(cnt,0.02*peri,True)
        x,y,w,h =  cv2.boundingRect(approx)
    return x+w//2 , y+h//2

# Create TrackBars
cv2.namedWindow("TraceBars")
cv2.resizeWindow("TraceBars",640,260)
cv2.createTrackbar("Hue min","TraceBars",91,179,empty)
cv2.createTrackbar("Hue max","TraceBars",157,179,empty)
cv2.createTrackbar("Sat min","TraceBars",82,255,empty)
cv2.createTrackbar("Sat max","TraceBars",223,255,empty)
cv2.createTrackbar("Val min","TraceBars",43,255,empty)
cv2.createTrackbar("Val max","TraceBars",255,255,empty)

#Get your mask value from here
while True:
    h_min = cv2.getTrackbarPos("Hue min", "TraceBars")
    h_max = cv2.getTrackbarPos("Hue max", "TraceBars")
    s_min = cv2.getTrackbarPos("Sat min", "TraceBars")
    s_max = cv2.getTrackbarPos("Sat max", "TraceBars")
    v_min = cv2.getTrackbarPos("Val min", "TraceBars")
    v_max = cv2.getTrackbarPos("Val max", "TraceBars")
    #print(h_min,h_max,s_min,s_max,v_min,v_max)
def drawonCanvas(mypoints):
    for point in mypoints:
        cv2.circle(imgCon, (point[0],point[1]), 10, (128,0,0), cv2.FILLED)



Webcam = cv2.VideoCapture(0)
Webcam.set(10,100)
Webcam.set(3,1000)
Webcam.set(4,1000)
newpoints =[]
mypoints = []
while True:
    success,frame = Webcam.read()
    imgHSV = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    imgCon = frame.copy()
    lower = np.array([h_min,s_min,v_min])
    upper = np.array([h_max,s_max,v_max])
    mask = cv2.inRange(imgHSV,lower,upper)
    imgResult = cv2.bitwise_and(frame,frame,mask = mask)
    #imgstack = stackImages(0.5, [[frame, imgHSV],[mask,imgResult]])
    #cv2.imshow("stacked images", imgstack)
    X,Y = getContours(mask)

    if X != 0 and Y != 0:
        newpoints.append([X,Y])

    if len(newpoints) != 0:
         for newp in newpoints:
             mypoints.append(newp)
    if len(mypoints) != 0:
        drawonCanvas(mypoints)

    #cv2.circle(imgCon,(X,Y),5,(0,165,255),cv2.FILLED)
    cv2.imshow("Contour",imgCon)

    cv2.waitKey(1)
