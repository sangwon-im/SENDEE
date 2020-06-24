#웹캠 읽고 감정 저장
#사람 등록 버튼(누군지)
#위치, 누구인지, 감정   

##구동부
#메인 함수는 0.1초 단위로 돈다, 따라서 움직임 트래킹은 웹캠단에서 처리해야 한다.

import time
import pickle
import cv2
import face_recognition
import os
from keras.utils import np_utils
from keras.datasets import mnist
from keras.models import Sequential
from keras.models import load_model
from keras.layers import Dense, Activation, BatchNormalization
import numpy as np

import model as md
import display

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


#img 폴더에 있는 사진을 인코딩해서 {이름:인코딩} 의 딕셔너리로 바꾸고, names_encodings.pkl 파일에 저장
def img2encoding():
    known_face_names = []
    known_face_encodings = []

    images = os.listdir("img/")
    for image in images:
        image_name = image.split('.')[0]
        print(image_name)
        known_face_names.append(image_name)
        
        name_image = face_recognition.load_image_file(f"img/{image_name}.jpg")
        image_encoding = face_recognition.face_encodings(name_image)[0]
        
        known_face_encodings.append(image_encoding)
    # names_encodings = dict(zip(known_face_names, known_face_encodings))

    with open("pkl/known_face_names.pkl", "wb") as file:
        pickle.dump(known_face_names, file)
        file.close()
    with open("pkl/known_face_encodings.pkl", "wb") as file:
        pickle.dump(known_face_encodings, file)
        file.close()


def face_reco():
    ##rgb_for_face 불러오기
    with open("pkl/rgb_for_face.pkl", "rb") as file:
        rgb_for_face = pickle.load(file)
        file.close()
    ##face_locations 불러오기
    with open("pkl/face_locations.pkl", "rb") as file:
        face_location = pickle.load(file)
        file.close()
    with open("pkl/known_face_names.pkl", "rb") as file:
        known_face_names = pickle.load(file)
        file.close()
    with open("pkl/known_face_encodings.pkl", "rb") as file:
        known_face_encodings = pickle.load(file)
        file.close()
    
    ##불러온 파일 이용해서 인코딩 구한다
    face_encoding = face_recognition.face_encodings(rgb_for_face, face_location)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding[0])
    face_distances = face_recognition.face_distance(known_face_encodings, face_encoding[0])
    best_match_index = np.argmin(face_distances)

    if matches[best_match_index]:
        name = known_face_names[best_match_index]
    else:
        name = "unknown"
    
    return name


def face_emo(model):
    with open("pkl/gray_for_emotion.pkl", "rb") as file:
        gray_for_emotion = pickle.load(file)
        file.close()
    with open("pkl/face_locations.pkl", "rb") as file:
        face_location = pickle.load(file)
        file.close()

    # model = load_model("models/20200622_2242_model.h5")
    model = model
    # emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    for (top, right, bottom, left) in face_location:
        roi_gray = gray_for_emotion[top:bottom, left:right]
        cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
        prediction = model.predict(cropped_img)
        # cv2.imwrite('cropped.png', roi_gray)
        
        if len(prediction) != 0:
            prediction = prediction[0]
            prediction = np.rint(prediction/sum(prediction)*100)# %
            return prediction
        

img2encoding()
model = md.model_basic()
model.load_weights('models/model.h5')

cycle_time = 1


while True:
    try:
        start = time.time() 
        with open("pkl/isDetected.pkl", "rb") as file:
            isDetected = pickle.load(file)
            file.close()
        if isDetected == True: #인식이 된 상태

            emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
            #5번의 감정을 평균낸다
            # count=0
            # while count==3:
            #     prediction = face_emo(model)
            #     prediction_sum = prediction_sum + prediction
            #     count+=1
            # prediction = prediction_sum
            # prediction_sum = [0,0,0,0,0,0,0]

            prediction = face_emo(model)
            emotion = emotion_dict[np.argmax(prediction)]
            print(emotion)

            name = face_reco()
            print(name)
            ###################### 행동 #####################################
            # onprocess = True
            # with open("pkl/onprocess.pkl", "wb") as file:
            #     pickle.dump(onprocess, file)

            display.emo2reaction(emotion, name)  ##unknown sangwon 

            # onprocess = False
            # with open("pkl/onprocess.pkl", "wb") as file:
            #     pickle.dump(onprocess, file)
            ################################################################
        else: #인식이 안된 상태
            #######################
            display.noface()
            #######################

        #코드 실행 시간
        print("time :", (time.time() - start), "\n") 
        
        #cycle_time 초마다 한번 실행
        if (time.time() - start) < cycle_time:
            time.sleep(cycle_time - (time.time() - start))

    except EOFError:
        pass
    except pickle.UnpicklingError as e:
        pass
