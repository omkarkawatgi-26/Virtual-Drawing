import cv2
import numpy as np
video = cv2.VideoCapture(0)
video.set(3,360)
video.set(4,360)
#video.set(10,)



while True:
    success, frame = video.read()
    cv2.imshow("Video",frame)
    if cv2.waitKey(1) & 0xFF == ord('x'):
        break