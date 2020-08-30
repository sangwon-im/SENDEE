from multiprocessing import Process
import time, cv2
import numpy as np
####RPi####
# import motordrive
# import RPi.GPIO as GPIO

# 웹캠에서는 얼굴 인식하고 변수에 저장하는 것만
def webcam():
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

    isDetected = False
    cycle_time = 0.05 #1프레임당 시간

    while True:
        start = time.time()
        ret, frame = capture.read()
        if not ret: break

        rgb_for_face = frame[::]
        gray_for_emotion = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = face_cascade.detectMultiScale(gray_for_emotion, 1.3, 5) #문제는 이부분이 수평만 인지한다, 기울어진 얼굴도 인식하도록

        cv2.putText(frame, info, (5, 15), font, 0.5, (255, 0, 255), 1)
        #피클 파일에 쓰는 부분을 없애고, 프로세스간에 변수를 공유하도록 한다.
        if len(faces)>1:
            face_list = []

            for face in faces:
                face_list.append(face[2])
            faces = np.array([faces[np.argmax(np.array(face_list))]])

        if len(faces)==1:
            if isDetected == False:
                isDetected = True   #
            # for (x, y, w, h) in faces:
            [x, y, w, h] = faces[0]
            
            face_locations = np.array([[y, x+w, y+h, x]])
            (top, right, bottom, left) = (y, x+w, y+h, x)
            cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)
        else:     # No face detected
            if isDetected==True:
                motordrive.headsleep()
                isDetected = False #사람없으면 True

        frame = cv2.flip(frame, 1)
        # cv2.imshow('frame', frame)
        if cv2.waitKey(1) == ord('q'): break

        # print("time :", time.time() - start)
        if (time.time() - start) < cycle_time:
            time.sleep(cycle_time - (time.time() - start))

def face_tracking():
    pass
def armMove():
    pass 
def test2():
    pass     
def test3():
    pass

if __name__ == '__main__':
    Process(target=webcam).start()
    # Process(target=test2).start()
    # Process(target=test3).start()
