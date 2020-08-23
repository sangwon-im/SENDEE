import cv2
import time
import random
import pickle


def display(filename, name, emotion):
    cap = cv2.VideoCapture(f"displays/{filename}.gif")
    

    with open("pkl/emotion.pkl", "wb") as file:
        pickle.dump(filename, file)

    while True:
        ret, frame = cap.read()
        if ret==False: break

        #뉴트럴만 좀 빨리 재생하도록
        #프레임당 33ms 기다리고 다음 프레임 재생
        if filename == "neutral1":
            cv2.waitKey(11)
        else:
            cv2.waitKey(33)
    
        ##인식 되고, 알때
        ##인식 되고, 모를때
        ##인식 안될때
        font = cv2.FONT_HERSHEY_DUPLEX

        if name =="noone":
            if emotion == "fun":
                cv2.putText(frame, f"Anybody there..?", (30, 450), font, 1.0, (0, 0, 0), 1)
            else:
                cv2.putText(frame, f"Anybody there..?", (30, 450), font, 1.0, (0, 0, 0), 1)
        
        elif name == "unknown": 
            cv2.putText(frame, f"Who are you?? You look {emotion}", (30, 450), font, 1.0, (0, 0, 0), 1)
        
        else:
            name_ = name.capitalize()
            cv2.putText(frame, f"{name_}, you look {emotion}", (30, 450), font, 1.0, (0, 0, 0), 1)
        
        #재생 되는 순간
        cv2.namedWindow("window", cv2.WND_PROP_FULLSCREEN)
        cv2.setWindowProperty("window",cv2.WND_PROP_FULLSCREEN,cv2.WINDOW_FULLSCREEN)
        cv2.imshow("window", frame)


def emo2reaction(emotion, name):

    if emotion == 'Neutral':
        if name != "unknown": #아는 사람
            if random.randrange(100) < 50:
                display("neutral1", name, emotion) #무표정
            else:
                display("neutral2", name, emotion) #눈깜박
                display("neutral1", name, emotion)

        else:  #모르는 사람
            if random.randrange(100) < 50:
                display("neutral1", name, emotion)
            else:
                display("neutral3", name, emotion) #물음표
                display("neutral1", name, emotion)
    

    elif emotion == 'Angry':
        if name != "unknown": #아는 사람
            if random.randrange(100) < 50:
                display("fear2", name, emotion) #인상쓰기
            else:
                display("angry2", name, emotion) #극대노

        else:  #모르는 사람
            if random.randrange(100) < 80:
                display("angry1", name, emotion) #쫄음
            else:
                display("neutral1", name, emotion)


    elif emotion == 'Sad':
        if random.randrange(100) < 50:
            display("sad1", name, emotion)  #한숨
        else:
            display("sad2", name, emotion)  #울음


    ## 멋쩍은 웃음 만들어줘라!!!
    elif emotion == 'Happy':
        #아는 사람
        if name != "unknown": 
            display("happy1", name, emotion)  #많이 행복

        #모르는 사람
        else: 
            if random.randrange(100) < 80:
                display("neutral3", name, emotion) #happy3 어색한 웃음으로 대체
            else:
                display("neutral3", name, emotion)  #물음표

    elif emotion == 'Surprised':
        if name != "unknown": #아는 사람
            display("surprised2", name, emotion)

        else:  #모르는 사람
            display("surprised1", name, emotion)

    elif emotion == 'Fearful':
        display("fear1", name, emotion)

def noface():
    name = "noone"
    emotion = "noone"
    rand = random.randrange(100)
    if rand < 50:     
        display("neutral1", name, emotion) #무표정
    elif 50<=rand<60:
        emotion = "fun"
        display("happy2", name, emotion)  #비웃음
    else:
        display("neutral2", name, emotion) #눈깜박
        display("neutral1", name, emotion) #무표정




# print(random.randrange(2))


#사람 인식 못하면 재밌는 gif 아무거나 랜덤 재생

# neutral1 #기본
# neutral2 #기본
# neutral3 #unknown
# angry1 #쫄았다
# angry2 #같이 화낸다
# happy1 #해피
# happy2 #비웃음
# sad1 #한숨
# sad2 #눈물
# fear1 #무서워서 소리침
# fear2 #지켜줄게? 화나보인다
# surprise1 #깜짝아;;
# surprise2 #무슨일이지????