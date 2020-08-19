import numpy as np
import cv2

# create cascads classifier
face_cascad1 = cv2.CascadeClassifier("cascades/data/haarcascade_frontalface_alt2.xml")
face_cascad2 = cv2.CascadeClassifier("cascades/data/haarcascade_frontalface_alt.xml")
face_cascad3 = cv2.CascadeClassifier("cascades/data/haarcascade_profileface.xml")
hand_cascad = cv2.CascadeClassifier("cascades/haarcascade/aGest.xml")
# define the computer's default wb camera as our capture device.
cap = cv2.VideoCapture(0)


def save_face_image_recognized(face, frame):
    """
    save only the face on the given frame.
    :param face: Tuple of four values x,y,w,h. where (x,y) are the location of the face "start" on the frame and w , h
    are the width and height respectively
    :param frame: frame where the face was detected.
    :return:
    """
    x, y, w, h = face
    # cut the face form the entire frame.
    only_face = frame[y:y + h, x: x + w]
    cv2.imwrite("original.png", frame)
    cv2.imwrite("detected_face_.png", only_face)


def draw_rectangle_around_face(face, frame, text):
    x, y, w, h = face
    color = (255, 0, 0)
    stroke = 2
    end_x = x + w
    end_y = x + h
    cv2.rectangle(frame, (x, y), (end_x, end_y), color, stroke)
    put_text_in_frame(face, frame, text)


def put_text_in_frame(face, frame, text):
    x, y, w, h = face
    font = cv2.FONT_HERSHEY_SIMPLEX
    color = (255, 255, 255)
    stroke = 2
    cv2.putText(frame, text, (x, y), font, 1, color, stroke, cv2.LINE_AA)


def detect_face(faces, classifier_name):
    for face in faces:
        print(face)
        save_face_image_recognized(face, frame)
        draw_rectangle_around_face(face, frame, classifier_name)


while True:
    # just read single frame from our capture device.
    ret, frame = cap.read()
    # The classifier works only with gray images thus we first convert our frame to gray.
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # ask to detect all in the current frame. #todo check those scale factors and see if there is any thing better.
    faces1 = face_cascad1.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=6)
    # faces2 = face_cascad2.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5)
    # faces3 = face_cascad3.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=5)

    hand = hand_cascad.detectMultiScale(gray, scaleFactor=1.05, minNeighbors=6)

    to_finish = False
    detect_face(faces1, "frontalface_alt2")
    detect_face(hand, "hand")
    # detect_face(faces2, "frontalface_alt")
    # detect_face(faces3, "profileface")
    if to_finish:
        break

    # display the frame
    cv2.imshow('frame', frame)
    # wait for 5 mili seconds between iterations and stop the loop if "q" is pressed.
    if cv2.waitKey(5) & 0xFF == ord('q'):
        break

# When we done, release the capture
cap.release()
cv2.destroyAllWindows()
