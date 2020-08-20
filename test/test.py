import threading, time

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
    t1=threading.Thread(target=test1)
    t2=threading.Thread(target=test2)
    t3=threading.Thread(target=test3)

    t1.start()
    t2.start()
    t3.start()
