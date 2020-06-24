import motordrive
import pickle
import time

cycle_time = 0.05
temp = True
while True:
    try:
        start = time.time()

        with open("pkl/emotion.pkl", "rb") as file:
            emotion = pickle.load(file)[0]
            count = pickle.load(file)[1]

        if temp == count:
            motordrive.emoreact(emotion)
            temp = not temp
        
        if (time.time() - start) < cycle_time:
            time.sleep(cycle_time - (time.time() - start))


    except EOFError:
        pass
