import cv2
import face_recognition

HEIGHT = 240
WIDTH = 360 

capture = cv2.VideoCapture(0)
capture.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
capture.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)


while True:
    ret, frame = capture.read()
    if not ret: break

    rgb_for_face = frame[:,:,::-1]
    face_locations = face_recognition.face_locations(rgb_for_face)

    for (top, right, bottom, left) in face_locations:
        x_pos = (right+left)/2
        y_pos = (top+bottom)/2

        x_pos = (x_pos - (WIDTH/2)) / WIDTH *2 +0.1
        y_pos = -(y_pos - (HEIGHT/2)) / HEIGHT *2


        print(x_pos, y_pos)

        cv2.rectangle(frame, (left, top), (right, bottom), (0,0,255), 2)

    cv2.imshow('frame', frame)
 
    if cv2.waitKey(1) == ord('q'): break

capture.release()
cv2.destroyAllWindows()
