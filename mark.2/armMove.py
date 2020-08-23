import motordrive
import pickle
import time

cycle_time = 0

while True:
    try:
        start = time.time()

        with open("pkl/emotion.pkl", "rb") as file:
            emotion = pickle.load(file)
        
        if emotion == 'neutral1':
            cycle_time= 11*90/1000
        else:
            cycle_time = 33*90/1000
        
        motordrive.emoreact(emotion)
        
        if (time.time() - start) < cycle_time:
            time.sleep(cycle_time - (time.time() - start))

    except EOFError:
        pass
