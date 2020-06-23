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
# import motordrive
import display

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'


#img 폴더에 있는 사진을 인코딩해서 {이름:인코딩} 의 딕셔너리로 바꾸고, names_encodings.pkl 파일에 저장
def img2encoding():
    known_face_names = []
    known_face_encodings = []

    images = os.listdir("img/")
    for image in images:
        image_name = image.split('.')[0]
        known_face_names.append(image_name)
        
        image_encoding = face_recognition.face_encodings(face_recognition.load_image_file(f"img/{image_name}.jpg"))[0]
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
    
    ##불러온 파일 이용해서 인코딩 구한다
    face_encoding = face_recognition.face_encodings(rgb_for_face, face_location, num_jitters=1)

    with open("pkl/known_face_names.pkl", "rb") as file:
        known_face_names = pickle.load(file)
        file.close()
    with open("pkl/known_face_encodings.pkl", "rb") as file:
        known_face_encodings = pickle.load(file)
        file.close()

    matches = face_recognition.compare_faces(known_face_encodings, face_encoding[0])

    if True in matches:
        name = known_face_names[matches.index(True)]
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
        cv2.imwrite('cropped.png', roi_gray)
        
        if len(prediction) != 0:
            prediction = prediction[0]
            prediction = np.rint(prediction/sum(prediction)*100)# %
            return prediction
        


model = md.model_basic()
model.load_weights('models/model.h5')

cycle_time = 5

while True:
    # try:
    start = time.time() 
    emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}
    
    emotion = face_emo(model)
    print(emotion_dict[np.argmax(emotion)])
    
    name = face_reco()
    print(name)
    ###################### 행동 #####################################
    



    ################################################################
    
    #코드 실행 시간
    print("time :", (time.time() - start), "\n") 
    
    #cycle_time 초마다 한번 실행
    if (time.time() - start) < cycle_time:
        time.sleep(cycle_time - (time.time() - start))

    # except EOFError:
    #     pass






    # count = 0
    # emo_count = 5
    # #5번 읽은 감정을 평균냄
    # emo_sum = [0,0,0,0,0,0,0]
    # emotion = [0,0,0,0,0,0,0]


        # print("time :", time.time() - start) #코드 실행 시간
        
        
        # emotion_dict[np.argmax(emotion)]

        # print(emotion_dict[np.argmax[face_emo]])
        # print(name)
        # print(emotion)
        #angry -> (화냄, 시선 회피, 울음)
        #disgust -> (궁금, 회피, 화냄)
        #fear -> (위로)
        #happy -> (웃음, 장난, 춤)
        #sad -> (위로, 울음)
        #surprise -> (궁금, 놀람)
        #neutral -> (장난, 심심, 졸음)
        #혼자 장난치는 패턴 여러개
        # webcam.webcam()
        # face_position()
        # face_emo()
        # time.sleep(0.5)

        # emo_sum = emo_sum + emo
        # count += 1
        # #얼굴 인식은 5번마다 한번씩 , 표정 인식은 5번을 평균내서
        # if count == emo_count:
        #     emo_sum = emo_sum/emo_count
        #     emotion = emo_sum
        #     name = face_reco()
        #     # print(name, dict(zip(list(emotion_dict.values()), list(emo_sum))))
    
        #     ########### 여기에 행동 넣기 ################
        #     print(name)
        #     print(emotion_dict[np.argmax(emotion)])
            

        #     ############################################

        #     emo_sum = [0,0,0,0,0,0,0]
        #     count = 0