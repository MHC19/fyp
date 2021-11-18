#!/usr/bin/env python2
import numpy as np
from numpy.core.fromnumeric import mean
import sounddevice as sd  # M: Used in getting mic volume
import rospy
from datetime import datetime
from std_msgs.msg import String

# def callback(indata, frames, time, status):
#     global array_meanA
#     global n

#     volume_norm = np.linalg.norm(indata) * 10

#     # Replace end of array with volume_norm
#     array_meanA[n] = int(volume_norm)

#     # Shift elements left by 1
#     # Note: Final element will be the same as previous element
#     for h in range(n):
#         array_meanA[h] = array_meanA[(h + 1)]

#     meanA = 0

#     # Sum values in array_meanA
#     for h in range(n):
#         meanA = array_meanA[h] + meanA

#     meanA = meanA / n


# ''' Convert into function '''
# stream = sd.InputStream(callback=callback)
# print("Starting stream!\n\n")
# stream.start()
# stream_start = True
# while stream_start:
#     current_time = datetime.now()
#     timer = (current_time - start_time).total_seconds()

#     if timer >= 3:
#         stream_start = False

# print("Stopping stream!")
# stream.abort()


def stream_callback(indata, frames, time, status):
    print("IN STREAM")
    # print("Starting stream_callback!!!\n\n")
    global array_meanA 
    global n
    global timer_on
    global start_time
    # global current_time
    global data

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

    meanA = meanA / n
    

    if meanA >= 10 and timer_on == False:
        # M: Start timer when volume is loud and timer is off
        start_time = datetime.now()
        timer_on = True
    elif meanA < 10:
        # M: Turn timer off when volume goes below threshold
        timer_on = False

        start_time = datetime.now()
    
    current_time = datetime.now()
    timer = (current_time - start_time).total_seconds()

    if timer >= 5:
        timer_on = False
        # Use TTS to play warning
        print("Please lower your volume, loud for 5 seconds!")
        timer = 0
    

def listener_callback(data):
    if data.data == "no_detection":
        stream = sd.InputStream(callback=stream_callback)

        rospy.loginfo("Message received: %s" % data.data)
        stream_start = True
    

    while stream_start:
        stream.start()

        if data.data == "face_detected":
            print("NO FACE")
            raise sd.CallbackStop()
            stream_start = False
            
    
    print("Aborting stream")
    stream.abort()



def listener():
    rospy.init_node("noise_detection", anonymous=True)
    rospy.Subscriber('face_detection_topic', String, listener_callback)

    rospy.spin()


if __name__ == '__main__':
    try:
        # M: Length of data to collect in array
        n = 30

        # M: Added 0.0 for shifting
        array_meanA = [0.0]

        # M: Initialize array with n values of 0.0
        for h in range(n):
            array_meanA.append(0.0)

        timer_on = False

        listener()
    # M: Catch exceptions, such as when user presses ctrl+c
    except Exception as e:
        print(e)
