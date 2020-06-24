import motordrive
import pickle
import time

while True:
    with open("pkl/emotion.pkl", "rb") as file:
        emotion = pickle.load(file)
            
    motordrive.emoreact(emotion)

