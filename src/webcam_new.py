import face_recognition
import cv2
import numpy as np
from model import *

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, 320)



while True:
    ret, frame = capture.read()
    #ret 은 카메라의 상태, 정상작동되면 true 아니면 false
    if not ret:
        break
    #frame 이 정보를 가져옴 
    rgb_frame = frame[:,:,::-1]
    #facereco 가 읽을 수 있는 상태로 변환

    face_locations = face_recognition.face_locations(rgb_frame)
    face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)


    cv2.imshow('Video', frame)

    if cv2.waitKey(1) == ord('q'): break

capture.release()
cv2.destroyAllWindows()

