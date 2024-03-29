#!/usr/bin/env python2
# From https://www.mygreatlearning.com/blog/real-time-face-detection/
import cv2
import numpy
import os
import rospy
from datetime import datetime
from std_msgs.msg import String

''' NOTE:
2021/11/10 1531
Add 5 seconds timer, and wait for chatbot function to be complete, and then only perform noise detection. '''

''' M:
(DONE) Change to pub and sub format. 
Find way to send signal to chatbot or noise_level_detection.
Give grace timer for chatbot since face_detection might not have consistent signal or detection. Perhaps 5 seconds. After 5 seconds, change to noise_level_detection mode.
List down steps for setting up, e.g.: pip3 installs such as dlib, opencv-python, etc. '''

''' 
M:
Both chatbot and noise detection will subscribe to the topic.
In chatbot, if signal = face_detected, then carry out function, and publish to speaker, reset timer to 0. If timer >= 5, then break.
In noise detection, if signal != face_detected, then carry out function.
'''

cascPath = os.path.dirname(
    cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)


def talker():
    pub = rospy.Publisher('face_detection_topic', String, queue_size=10)
    rospy.init_node('face_detection', anonymous=True)
    # M: This will affect webcam framerate, since we're using rate.sleep()
    rate = rospy.Rate(60.0)
    
    start_time = datetime(1990, 1, 1)

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
            start_time = datetime.now()

            pub.publish("face_detected")
            rospy.loginfo("face_detected")
        else:
            # if (isinstance(faces, numpy.ndarray) == False) and ((datetime.now() - start_time).total_seconds() >= 5):
            if isinstance(faces, numpy.ndarray) == False:
                pub.publish("no_detection")
                rospy.loginfo("no_detection")

        rate.sleep()

    video_capture.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    try:
        talker()
    # M: Catch exceptions, such as when user presses ctrl+c
    except Exception as e:
        print(e)
