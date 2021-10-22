# From https://www.mygreatlearning.com/blog/real-time-face-detection/
import cv2
import os
import numpy

''' M:
Change to pub and sub format.
Find way to send signal to chatbot or noise_level_detection.
Give grace timer for chatbot since face_detection might not have consistent signal or detection. Perhaps 5 seconds. After 5 seconds, change to noise_level_detection mode.
List down steps for setting up, e.g.: pip3 installs such as dlib, opencv-python, etc. '''

# M: FIND OUT WHERE THIS DATA COMES FROM
cascPath = os.path.dirname(
    cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"

print(cascPath)
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)

while True:
    # Capture frame-by-frame
    ret, frame = video_capture.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray,
                                        scaleFactor=1.1,
                                        minNeighbors=5,
                                        minSize=(60, 60),
                                        flags=cv2.CASCADE_SCALE_IMAGE)

    # https://stackoverflow.com/questions/14113187/how-do-you-set-a-conditional-in-python-based-on-datatypes/49067320
    # https://stackoverflow.com/questions/36783921/valueerror-when-checking-if-variable-is-none-or-numpy-array
    # M: Added code for checking if face detected. So can be used in mode switching, by returning true or false
    if isinstance(faces, numpy.ndarray):
        print("Face detected!\n")

    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    
    # Display the resulting frame
    cv2.imshow('Video', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()