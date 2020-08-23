import cv2
import pickle
import motordrive
import RPi.GPIO as GPIO
import time
import numpy as np

HEIGHT = 360
WIDTH =  480

capture = cv2.VideoCapture(-1)
capture.set(3, WIDTH)
capture.set(4, HEIGHT)
capture.set(10, 60) #brightness
capture.set(11, 60) #contrast
capture.set(21, 0.25) #auto exposure
#capture.set(5, 60)

hor_error_Sum = 0
hor_error_Prev = 0
ver_error_Sum = 0
ver_error_Prev = 0
past_dc = 4
##########

face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_alt2.xml')
info = ''
font = cv2.FONT_HERSHEY_SIMPLEX

count = 0
speed = 10
isDetected = False

cycle_time = 0.05 #1프레임당 시간

### 영상 캡쳐 대신에 사진 캡쳐로 하면 cycle time 증가해도 딜레이 없지 않을까?
while True:
    start = time.time()  # 시작 시간 저장
    ##감정표현이 진행중인지 읽어오기
    # with open("pkl/onprocess.pkl", "rb") as file:
    #     onprocess = pickle.load(file)
    #     file.close()
    
    ## 진행중이면 멈추기
    # if onprocess == True:
    #     # GPIO.cleanup()
    #     time.sleep(3.5)
    # else: 
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
            file.close()
        #gray 이미지 피클로 저장, 표정
        with open("pkl/gray_for_emotion.pkl", "wb") as file:
            pickle.dump(gray_for_emotion, file)
            file.close()
        # print("write!")
        count = 0
    else:
        count += 1
    ###################################################
    
    if len(faces)>1:
        face_list = []

        for face in faces:
            face_list.append(face[2])
        faces = np.array([faces[np.argmax(np.array(face_list))]])

    if len(faces)==1:
        if isDetected == False:
            isDetected = True   #
            with open("pkl/isDetected.pkl", "wb") as file:
                pickle.dump(isDetected, file)
                file.close()
        # for (x, y, w, h) in faces:
        [x, y, w, h] = faces[0]
        
        face_locations = np.array([[y, x+w, y+h, x]])
        (top, right, bottom, left) = (y, x+w, y+h, x)
        cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)

        with open("pkl/face_locations.pkl", "wb") as file:
            pickle.dump(face_locations, file)
            file.close()
        
        x_pos = x + w/2
        y_pos = y + h/2

        x_pos = 2 * (x_pos - WIDTH/2) / WIDTH + 0.1
        y_pos = -2 * (y_pos - (HEIGHT/2)) / HEIGHT

        ###########
        hor_error_Sum = hor_error_Sum + x_pos
        ver_error_Sum = ver_error_Sum + y_pos
        motordrive.MPIDCtrl(x_pos, 0.05, hor_error_Sum, hor_error_Prev)
        past_dc = motordrive.Servo(y_pos, 0.05, past_dc, ver_error_Sum, ver_error_Prev)
        hor_error_Prev = x_pos
        ver_error_Prev = y_pos
        ###########

    else:     # No face detected
        if isDetected==True:
            motordrive.headsleep()
            isDetected = False #사람없으면 True
            with open("pkl/isDetected.pkl", "wb") as file:
                pickle.dump(isDetected, file)
                file.close()
        else:
            motordrive.headsleep()
            print('')
            

    frame = cv2.flip(frame, 1)
    # cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'): break

    # print("time :", time.time() - start)
    if (time.time() - start) < cycle_time:
        time.sleep(cycle_time - (time.time() - start))
    print(isDetected)

GPIO.cleanup()



# capture.release()
# cv2.destroyAllWindows()