import picamera
import cv2 
import numpy as np
import pickle
import face_recognition

HEIGHT = 240
WIDTH = 320 

camera = picamera.PiCamera()
camera.resolution = (WIDTH, HEIGHT)
frame = np.empty((HEIGHT, WIDTH, 3), dtype=np.uint8)

#직전 값과, 지금까지의 누적 값
def face_tracking(x_pos, y_pos):
    if x_pos > 0.1: #카메라 입장에서 오른쪽
        print('move head rightward')
        #speed 를 x_pos의 절대값에 비례하도록
    elif x_pos < -0.1:
        print('move head leftward')
    if y_pos > 0.1:
        print('move head upward')
    elif y_pos < -0.1:
        print('move head downward')
    #얼마나 떨어져 있는지에 따라서 속도 다르게? PID 제어?

while True:    
    # ret, frame = capture.read()
    # if not ret: break

    camera.capture(frame, format="rgb")

    rgb_for_face = frame[:,:,::-1]
    gray_for_emotion = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    file = open("pkl/rgb_for_face.pkl", "wb")
    pickle.dump(rgb_for_face, file) #dic을 file에 쓴다
    file.close()

    file = open("pkl/gray_for_emotion.pkl", "wb")
    pickle.dump(gray_for_emotion, file) #dic을 file에 쓴다
    file.close()

    face_locations = face_recognition.face_locations(rgb_for_face)

    for (top, right, bottom, left) in face_locations:
        x_pos = (right+left)/2
        y_pos = (top+bottom)/2

        x_pos = (x_pos - (WIDTH/2)) / WIDTH *2 +0.1
        y_pos = -(y_pos - (HEIGHT/2)) / HEIGHT *2


        #두명이 인식되면, 먼저 인식된 사람 순으로?
        #아니면 더 큰 쪽으로 인식이 가능한가?

        #그러면 사람이 두명일 때 각각의 left right 값이 어떻게 변하는지
        if len(face_locations) > 1:
            face_locations = face_locations[:1]
            #일단 이건 인식된 사람 순

        print("number of people: ", len(face_locations))
        print("x", x_pos," y:", y_pos)

        #읽어낸 좌표를 피클 파일로 계속 저장
        dic = {"face_location": (x_pos, y_pos)}
        file = open("pkl/face_location.pkl", "wb")
        pickle.dump(dic, file) #dic을 file에 쓴다
        file.close()

        ##파일로 쏘지 말고 여기서 모터 구동을 제어하자!
        face_tracking(x_pos, y_pos)

        #읽어낸 사진을 사진파일로 저장?

        cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)

    cv2.imshow('frame', frame)
    
    
    
    if cv2.waitKey(1) == ord('q'): break

capture.release()
cv2.destroyAllWindows()
