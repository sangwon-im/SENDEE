from multiprocessing import Process
import time

def test1():
    time.sleep(5)
    print('5초지났다.')
    
def test2():
    for i in range(10):
        time.sleep(1)
        print("{0}second".format(i+1))
        
def test3():
    while True:
        time.sleep(1)
        print("병렬")


if __name__ == '__main__':
    Process(target=test1).start()
    Process(target=test2).start()
    Process(target=test3).start()
