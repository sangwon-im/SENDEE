#웹캠 읽고 감정 저장
#사람 등록 버튼(누군지)
#위치, 누구인지, 감정   

##구동부
#메인 함수는 0.1초 단위로 돈다, 따라서 움직임 트래킹은 웹캠단에서 처리해야 한다.

import time
# import tkinter
import pickle
import cv2
import face_recognition
import os

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
    with open("pkl/known_face_encodings.pkl", "wb") as file:
        pickle.dump(known_face_encodings, file)


def face_reco():
    ##rgb_for_face 불러오기
    with open("pkl/rgb_for_face.pkl", "rb") as file:
        rgb_for_face = pickle.load(file)
    ##face_locations 불러오기
    with open("pkl/face_locations.pkl", "rb") as file:
        face_location = pickle.load(file)
    
    ##위에서 불러온 두개 이용해서 
    face_encoding = face_recognition.face_encodings(rgb_for_face, face_location, num_jitters=1)

    with open("pkl/known_face_names.pkl", "rb") as file:
        known_face_names = pickle.load(file)
    with open("pkl/known_face_encodings.pkl", "rb") as file:
        known_face_encodings = pickle.load(file)
    
    print("known", known_face_encodings)
    print("face", face_encoding)
    matches = face_recognition.compare_faces(known_face_encodings, face_encoding[0])
    print(matches)
    print(known_face_names)
    if True in matches:
        matches.index('True')
    else:
        name="unknown"



def face_emo():
    with open("pkl/gray_for_emotion.pkl", "rb") as file:
        gray_for_emotion = pickle.load(file)
    # cv2.imwrite('gray.png',gray_for_emotion)
    #감정표현이 들어오면 딜레이를 피클파일에 저장, webcam 파일에서 읽어서 if문, 딜레이동안 webcam py 정지
    #일시정지 여부를 피클로 보냄

def main():
    while True:
        #랜덤 난수 생성
        #행동 패턴 리스트로 저장
        pattern = ('angry', 'disgust', 'fear', 'happy', 'sad', 'surprise', 'neutral')
        
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
        face_reco()
        face_emo()
        time.sleep(1)

        
# main()
face_reco()
