import cv2
import numpy as np
video = cv2.VideoCapture(0)
video.set(3,640)#Frame width
video.set(4,480)#Frame Height
video.set(10,150)#Frame Brightness



while True:
    success, frame = video.read()
    cv2.imshow("Video",frame)
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break
