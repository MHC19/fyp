#!/usr/bin/env python2
import numpy as np
import sounddevice as sd  # M: Used in getting mic volume
import rospy
from datetime import datetime
from std_msgs.msg import String


def stream_callback(indata, frames, time, status):
    print("In stream_callback\n---------\n")
    # nd_mode_on = False
    # print("Face detected\n-----\n\n")

    # https://stackoverflow.com/questions/36988920/how-to-gracefully-stop-python-sounddevice-from-within-callback
    # raise sd.CallbackStop()
    pass
    

def do_nothing(indata, frames, time, status):
    print("Within do_nothing")
    pass

def listener_callback(data):
    # # Need flag to avoid queuing up multiple times from no_detection
    # if data.data == "no_detection":
    #     nd_mode_on = True
    #     # print("Setting nd_mode_on to True")
    # if data.data == "face_detected":
    #     nd_mode_on = False
    

    if data.data == "face_detected":
        stream = sd.InputStream(callback=stream_callback, blocksize=0)

        start_stream = True
    else:
        start_stream = False
        print("Face not detected")
        stream = sd.InputStream(callback=do_nothing)

    if data.data == "face_detected":
        stream.start()

        # start_stream = False
        # stream.stop()

    else:
        stream.stop()
        print("Stream stopped\n\n")

    # if nd_mode_on:
    #     stream.start()
    #     print("In if statement")
    #     # stream.abort()
    #     # nd_mode_on = False
    # else:
    #     stream.abort()
    #     print("Aborting stream")

    # print("Outside while loop of listener_callback")
    # stream.abort()


def listener():
    rospy.init_node("noise_detection", anonymous=True)
    rospy.Subscriber('face_detection_topic', String, listener_callback)
    rospy.spin()


if __name__ == '__main__':
    try:
        # Need flag to avoid queuing up multiple times from no_detection
        nd_mode_on = True
        listener()
    # M: Catch exceptions, such as when user presses ctrl+c
    except Exception as e:
        print(e)
