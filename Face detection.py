import cv2
import numpy as np

## FACE DETECTION IN IMAGE
import cv2
img = cv2.imread(r"C:\Users\Omkar Kawatgi\Downloads\face.jpg")
imgGray = cv2.cvtColor(img,cv2.COLOR_BGR2BGRA)
facecascade = cv2.CascadeClassifier(r"C:\Users\Omkar Kawatgi\PycharmProjects\opencv\venv\haarcascade_frontalface_default.xml")
faces = facecascade.detectMultiScale(imgGray,1.1,4)
for (x,y,w,h) in faces:
    cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)


cv2.imshow("Dected Face",img)
cv2.waitKey(0)


## Face Detection in Video
Webcam = cv2.VideoCapture(0)
FaceCascade = cv2.CascadeClassifier(r"C:\Users\Omkar Kawatgi\PycharmProjects\opencv\venv\haarcascade_frontalface_default.xml")
Webcam.set(3,1000)#Frame width
Webcam.set(4,1000)#Frame Height

while True:
    sucesses,frame = Webcam.read()
    face = FaceCascade.detectMultiScale(frame,1.1,4)
    for (x,y,w,h) in face:
        cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
    cv2.imshow("Live", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
