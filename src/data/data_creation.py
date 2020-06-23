import cv2

HEIGHT = 360
WIDTH =  480

capture = cv2.VideoCapture(-1)
# capture.set(3, WIDTH)
# capture.set(4, HEIGHT)
# capture.set(10, 50) #brightness
# capture.set(11, 50) #contrast
# capture.set(21, 0.25) #auto exposure

while True:
    ret, frame = capture.read()
    if not ret: break
    
    cv2.imshow('frame', frame)
    if cv2.waitKey(1) == ord('q'): break

    # print("time :", time.time() - start)
capture.release()
cv2.destroyAllWindows()