import face_recognition
import cv2
import numpy as np
from model import *
import pickle

model.load_weights('models/model.h5')

emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

HEIGHT = 480
WIDTH = 720 

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)


##############face encoding
obama_face_encoding = face_recognition.face_encodings(face_recognition.load_image_file("img/obama.jpg"))[0]
biden_face_encoding = face_recognition.face_encodings(face_recognition.load_image_file("img/biden.jpg"))[0]

known_face_encodings = [
    obama_face_encoding,
    biden_face_encoding
]
known_face_names = [
    "obama",
    "biden"
]

name = "Unknown"

count = 1
speedconst = 30

while True:
    ret, frame = capture.read()
    #ret 은 카메라의 상태, 정상작동되면 true 아니면 false
    if not ret:
        break
    #frame 이 정보를 가져옴 
    rgb_for_face = frame[:,:,::-1]
    gray_for_emotion = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    #facereco 가 읽을 수 있는 상태로 변환, emotion도 읽을 수 있게

    face_locations = face_recognition.face_locations(rgb_for_face)
    # face_encodings = []

    
    # facecasc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    # faces = facecasc.detectMultiScale(gray_for_emotion,scaleFactor=1.3, minNeighbors=5)
    for (top, right, bottom, left) in face_locations:
        x_pos = (right + left)/2
        y_pos = (top+bottom)/2  

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
        
        roi_gray = gray_for_emotion[top:bottom, left:right]
        # roi_rgb = rgb_for_face[top:bottom, left:right]

        cropped_gray = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        # cropped_rgb = cv2.resize(roi_rgb, dsize=(144, 144))

        # cv2.imwrite('img/crop.png', cropped_gray)
        
        #얼굴인식이 속도를 저하시키는 원인이므로, 5번 얼굴 윤곽을 인식했을 때, 한번 얼굴인식을 하도록 한다.
        if count%speedconst == 0:
            face_encodings = face_recognition.face_encodings(rgb_for_face)
            count = 1 

            for face_encoding in face_encodings:
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
                best_match_index = np.argmin(face_distances)
                
                name = "Unknown"

                if matches[best_match_index]:
                    name = known_face_names[best_match_index]
                
                    # name_input = input('name:')
                    # known_face_names.append(name_input)
                    # known_face_encodings.append(face_encodings[0])

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)
        
        count +=1


    # for (x, y, w, h) in faces:
        # cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)
    #     roi_gray = gray_for_emotion[y:y + h, x:x + w]
    #     cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        prediction = model.predict(cropped_gray)
        maxindex = int(np.argmax(prediction))
        
        # print(prediction)
        cv2.putText(frame, emotion_dict[maxindex], (left+20, bottom-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)
        # cv2.putText(frame, (left+20, bottom-60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.imshow('Video', frame)

    
    # x_pos = (right + left)/2
    # y_pos = (top+bottom)/2
    x_pos = (x_pos-(WIDTH/2))/WIDTH
    y_pos = -(y_pos-(HEIGHT/2))/HEIGHT

    print(name, emotion_dict[maxindex], (x_pos, y_pos))
    dic = {"name":name ,"emotion":emotion_dict[maxindex], "face_location": (x_pos, y_pos)}
    file = open("WebcamOutput", "wb")
    pickle.dump(dic, file)
    file.close()

    if cv2.waitKey(1) == ord('q'): break

capture.release()
cv2.destroyAllWindows()


