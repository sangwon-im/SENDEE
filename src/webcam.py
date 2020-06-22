import cv2
import pickle
# import motordrive
# import RPi.GPIO as GPIO
import time
import numpy as np

HEIGHT = 360
WIDTH =  480

capture = cv2.VideoCapture(-1)
capture.set(3, WIDTH)
capture.set(4, HEIGHT)
capture.set(10, 80) #brightness
capture.set(11, 60) #contrast
capture.set(21, 0.25) #auto exposure
#capture.set(5, 60)

hor_error_Sum = 0
hor_error_Prev = 0
ver_error_Sum = 0
ver_error_Prev = 0
past_dc = 0
##########

face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_alt2.xml')
info = ''
font = cv2.FONT_HERSHEY_SIMPLEX

count = 0
speed = 10

while True:
    start = time.time()  # 시작 시간 저장
    ret, frame = capture.read()
    if not ret: break

    rgb_for_face = frame[::]
    gray_for_emotion = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    faces = face_cascade.detectMultiScale(gray_for_emotion, 1.3, 5)

    cv2.putText(frame, info, (5, 15), font, 0.5, (255, 0, 255), 1)

    #############10프레임에 한번 시행되는 부분###############
    if count==speed:
        #rgb 이미지 피클로 저장, 얼굴인식
        with open("pkl/rgb_for_face.pkl", "wb") as file:
            pickle.dump(rgb_for_face, file) 
        #gray 이미지 피클로 저장, 표정
        with open("pkl/gray_for_emotion.pkl", "wb") as file:
            pickle.dump(gray_for_emotion, file)
        count = 0

    else:
        count += 1
    ###################################################
    
    if len(faces)>1:
        faces=faces[:1]

    if len(faces)==1:
        for (x, y, w, h) in faces:
            face_locations = np.array([[y, x+w, y+h, x]])
            (top, right, bottom, left) = (y, x+w, y+h, x)
            cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
            
            # print(face_locations)
            # print(faces)

            with open("pkl/face_locations.pkl", "wb") as file:
                pickle.dump(face_locations, file)
            
            # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
            # cv2.putText(frame, 'Detected Face', (x-5, y-5), font, 0.5, (255, 255, 0), 2)
            
            x_pos = x + w/2
            y_pos = y + h/2

            x_pos = 2 * (x_pos - WIDTH/2) / WIDTH
            y_pos = -2 * (y_pos - (HEIGHT/2)) / HEIGHT

            # print("x", x_pos," y:", y_pos)

            ###########
            hor_error_Sum = hor_error_Sum + x_pos
            ver_error_Sum = ver_error_Sum + y_pos
            # motordrive.MPIDCtrl(x_pos, 0.03, hor_error_Sum, hor_error_Prev)
            # past_dc = motordrive.Servo(y_pos, 0.05, past_dc, ver_error_Sum, ver_error_Prev)
            # 0.1 sec movememt
            hor_error_Prev = x_pos
            ver_error_Prev = y_pos
            ###########
    frame = cv2.flip(frame, 1)
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'): break

    # print("time :", time.time() - start)
capture.release()
cv2.destroyAllWindows()
