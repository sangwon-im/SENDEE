import cv2
import face_recognition
import pickle
import motordrive
import RPi.GPIO as GPIO
import time

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

#직전 값과, 지금까지의 누적 값
# def face_tracking(x_pos, y_pos):
#     if x_pos > 0.1: #카메라 입장에서 오른쪽
#         print('move head rightward')
#         #speed 를 x_pos의 절대값에 비례하도록
#     elif x_pos < -0.1:
#         print('move head leftward')
#     if y_pos > 0.1:
#         print('move head upward')
#     elif y_pos < -0.1:
#         print('move head downward')
#     #얼마나 떨어져 있는지에 따라서 속도 다르게? PID 제어?

count = 0
speed = 10

while True:
    # start = time.time()  # 시작 시간 저장
    ret, frame = capture.read()
    if not ret: break

    rgb_for_face = frame[::]
    gray_for_emotion = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    face_locations = face_recognition.face_locations(rgb_for_face)
    # print("number of people: ", len(face_locations))

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
    
    #얼굴 위치 피클로 저장, 한명만 저장인데 먼저 인식된? 
    #추가해야할 것, 얼굴 큰 사람이 인식되게끔!!!!!!!!!!!!!!!!!!!!!!!!!!!
    if len(face_locations)>1:
        face_locations=face_locations[:1]
    if len(face_locations)==1:
        for (top, right, bottom, left) in face_locations:
            x_pos = (right+left)/2
            y_pos = (top+bottom)/2

            x_pos = (x_pos - (WIDTH/2)) / WIDTH *2 +0.1
            y_pos = -(y_pos - (HEIGHT/2)) / HEIGHT *2

            #두명이 인식되면, 먼저 인식된 사람 순으로?
            #아니면 더 큰 쪽으로 인식이 가능한가?

            ##파일로 쏘지 말고 여기서 모터 구동을 제어하자!
            face_tracking(x_pos, y_pos)

            cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
            
        with open("pkl/face_locations.pkl", "wb") as file:
            pickle.dump(face_locations, file)

    #########################################


    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'): break

    # print("time :", time.time() - start)
capture.release()
cv2.destroyAllWindows()
