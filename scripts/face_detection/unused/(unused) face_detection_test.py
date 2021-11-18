#!/usr/bin/env python2
# From https://www.mygreatlearning.com/blog/real-time-face-detection/
import cv2
import numpy
import os
import rospy
from std_msgs.msg import String

''' M:
Change to pub and sub format.
Find way to send signal to chatbot or noise_level_detection.
Give grace timer for chatbot since face_detection might not have consistent signal or detection. Perhaps 5 seconds. After 5 seconds, change to noise_level_detection mode.
List down steps for setting up, e.g.: pip3 installs such as dlib, opencv-python, etc. '''

cascPath = os.path.dirname(cv2.__file__) + "/data/haarcascade_frontalface_alt2.xml"
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)

def talker():
    pub = rospy.Publisher('face_detected_topic', String, queue_size=5)
    rospy.init_node('face_detection_node', anonymous=True)
    rate = rospy.Rate(5.0)

    while not rospy.is_shutdown():
       

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
        ''' M:
        Consider setting up publisher here, where if face detected and timer less than 5, set timer to 0, and carry out chatbot function. '''
        # if isinstance(faces, numpy.ndarray):
        #     pub.publish("face_detected")

        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        
        # Display the resulting frame
        cv2.imshow('Video', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        if isinstance(faces, numpy.ndarray):
            # pub.publish("face_detected")
            rospy.loginfo("FACE DETECTED")
        
        rate.sleep()

    video_capture.release()
    cv2.destroyAllWindows()
    

    # # M: Publish string to topic
    # pub.publish()

    ''' M:
    Both chatbot and noise detection will subscribe to the topic.
    In chatbot, if signal = face_detected, then carry out function, and publish to speaker, reset timer to 0. If timer >= 5, then break.
    In noise detection, if signal != face_detected, then carry out function.
     '''

# M: Informs us that this is an executable script
if __name__ == '__main__':
    try:
        talker()
        
    # M: Catch exceptions, such as when user presses ctrl+c
    except Exception as e:
        print(e)