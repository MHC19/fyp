#!/usr/bin/env python2
import numpy as np
from numpy.core.fromnumeric import mean
from numpy.core.records import array
import sounddevice as sd  # M: Used in getting mic volume
import rospy
from datetime import datetime
from std_msgs.msg import String

def stream_callback(indata, frames, time, status):
    global array_meanA
    global n
    global start_time
    # print('array_meanA: {}; n: {}'.format(array_meanA, n))
    
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

    meanA = (meanA / n) + 10

    print(meanA)

    if ((datetime.now() - start_time).total_seconds() >= 5 and meanA > 10):
        pass

    ''' Complete thing, wait for 5 seconds, then continue. '''
    # Raise exception to exit callback
    raise sd.CallbackStop()

def listener_callback(data):
    global lock_boolean
    message = data.data
    # rospy.loginfo("Message received: %s" % data.data)

    if message == 'no_detection' and lock_boolean:
        lock_boolean = False
        print("LOCKED")

        stream = sd.InputStream(callback=stream_callback)
        stream.start()
    
    lock_boolean = True



def listener():
    # M: Creates node named noise_detection with unique numbers at the end (anonymous=True)
    rospy.init_node("noise_detection", anonymous=True)
    # M: Tells node to subscribe to face_detection_topic, that has messages of type String and will carry out listener_callback() every time a new message is received
    rospy.Subscriber('face_detection_topic', String, listener_callback)

    # M: Keeps node from exiting until it is shutdown
    rospy.spin()

if __name__ == '__main__':
    try:
        # M: Length of data to collect in array
        n = 30
        # M: Added 0.0 for shifting
        array_meanA = [0.0]
        # M: Global boolean to prevent noise_detection from running continuously due to queued messages
        lock_boolean = True

        # M: Initialize array with n values of 0.0
        for h in range(n):
            array_meanA.append(0.0)

        global start_time
        start_time = None
        print(start_time)

        listener()
    # M: Catch exceptions, such as when user presses ctrl+c
    except Exception as e:
        print(e)