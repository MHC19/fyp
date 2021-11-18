#!/usr/bin/env python2
import numpy as np
import sounddevice as sd  # M: Used in getting mic volume
import rospy
from numpy.core.fromnumeric import mean
from numpy.core.records import array
from datetime import datetime
from std_msgs.msg import String


def stream_callback(indata, frames, time, status):
    global array_meanA
    global n

    volume_norm = np.linalg.norm(indata) * 10

    # Replace end of array with volume_norm
    array_meanA[n] = int(volume_norm)

    # Shift elements left by 1
    # Note: Final element will be the same as previous element
    for h in range(n):
        array_meanA[h] = array_meanA[(h + 1)]

    meanA = 0

    # Sum values in array_meanA
    for h in range(n):
        meanA = array_meanA[h] + meanA

    print(meanA)
    # raise sd.CallbackStop()


def listener_callback(data):
    stream = sd.InputStream(callback=stream_callback)

    """ Note:
    data is a class of the message, while data.data is the actual String data type. """
    # print("data: {}\ndata.data: {}\n".format(type(data), type(data.data)))

    """ Process flow note:
    If message == no_detection, then start checking noise level.
    If noise_level >= threshold, start timer.
    If noise_level < threshold, reset timer to 0. """
    if data.data == 'no_detection':
        # M: Get from noise detection website explanation
        # stream.start()
        pass
    # When face_detected, then stop stream
    else:
        print("Stopping stream!!!")
        stream.stop()

    print("END")
    pass


def listener():
    # M: Creates node named noise_detection with unique numbers at the end (anonymous=True)
    rospy.init_node("noise_detection", anonymous=True)

    # M: Tells node to subscribe to face_detection_topic, that has messages of type String and will carry out listener_callback() every time a new message is received
    rospy.Subscriber('face_detection_topic', String, listener_callback)

    print("This is only called once!")

    # M: Keeps node from exiting until it is shutdown
    """ Note:
    It will keep looping within listener_callback with the new data. """
    rospy.spin()


# Note: Refer to ROS wiki for explanation or Python __name__ check
if __name__ == '__main__':
    try:
        # M: Length of data to collect in array
        n = 30
        # M: Added 0.0 for shifting
        array_meanA = [0.0]

        # M: Initialize array with n values of 0.0
        for h in range(n):
            array_meanA.append(0.0)

        # Output: array_meanA = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] --> 31 elements

        listener()
    except Exception as e:
        print("Exception thrown: {}".format(e))
