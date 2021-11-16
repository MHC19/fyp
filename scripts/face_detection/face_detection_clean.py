#!/usr/bin/env python2
# From https://www.mygreatlearning.com/blog/real-time-face-detection/
import cv2
import numpy
import os
import rospy
from datetime import datetime
from std_msgs.msg import String

def talker():
    face_success = 0.0
    total_messages = 0.0
    
    pub = rospy.Publisher('face_detection_topic', String, queue_size=10)
    rospy.init_node('face_detection', anonymous=True)
    # M: This will affect webcam framerate, since we're using rate.sleep()
    rate = rospy.Rate(30.0)
    
    # start_time = datetime(1990, 1, 1)

    while not rospy.is_shutdown():
        # Capture frame-by-frame
        ret, frame = video_capture.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = faceCascade.detectMultiScale(gray,
                                             scaleFactor=1.1,
                                             minNeighbors=5,
                                             minSize=(60, 60),
                                             flags=cv2.CASCADE_SCALE_IMAGE)

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # Display the resulting frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # https://stackoverflow.com/questions/14113187/how-do-you-set-a-conditional-in-python-based-on-datatypes/49067320
        # https://stackoverflow.com/questions/36783921/valueerror-when-checking-if-variable-is-none-or-numpy-array
        # M: Check if face detected. Used in mode switching
        ''' 
        M: Considerations
        Have two modes: chatbot_mode and noise_detection mode.
        When face detected, enter chatbot_mode and start 5s timer.
        While face remains detected, reset 5s timer to 0.
        If face not detected, let timer run to 5s.
        If timer = 5s, enter noise_detection mode.
        When face detected again, enter chatbot_mode... '''
        if isinstance(faces, numpy.ndarray):
            # M: Set and reset start time
            # start_time = datetime.now()

            face_success += 1

            pub.publish("face_detected")
            # rospy.loginfo("face_detected")
        else:
            # if (isinstance(faces, numpy.ndarray) == False) and ((datetime.now() - start_time).total_seconds() >= 5):
            # if isinstance(faces, numpy.ndarray) == False:
            pub.publish("no_detection")
            # rospy.loginfo("no_detection")
        
        total_messages += 1

        average_success_detection = face_success / total_messages * 100

        print("face_success = {}\ntotal_messages = {}\naverage_success_detection = {}\n\n".format(face_success, total_messages, average_success_detection))

        rate.sleep()
    
    print("Closing face_detection_clean.py...")

    video_capture.release()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    try:
        # https://www.bogotobogo.com/python/OpenCV_Python/python_opencv3_Image_Object_Detection_Face_Detection_Haar_Cascade_Classifiers.php
        ''' OpenCV already contains many pre-trained classifiers for face, eyes, smile etc. Those XML files are stored in opencv/data/haarcascades/ folder: '''
        cascPath = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
        faceCascade = cv2.CascadeClassifier(cascPath)
        video_capture = cv2.VideoCapture(0)

        

        talker()
    # M: Catch exceptions, such as when user presses ctrl+c
    except Exception as e:
        print(e)

