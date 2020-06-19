import cv2


HEIGHT = 480
WIDTH = 720 

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)


face_cascade = cv2.CascadeClassifier('haar/haarcascade_frontalface_default.xml')

while True:
    ret, frame = capture.read()
    if not ret: break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x,y),(x+w, y+h), (255,0,0), 1)
    

    cv2.imshow('frame',frame)

    if cv2.waitKey(1) == ord('q'): break

capture.release()
cv2.destroyAllWindows()
