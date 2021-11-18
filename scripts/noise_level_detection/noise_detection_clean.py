#!/usr/bin/env python2
import gtts
import numpy as np
import rospy
import sounddevice as sd # M: Used in getting mic volume
from datetime import datetime
from std_msgs.msg import String
from playsound import playsound
from gtts import gTTS

# SMA: https://hackaday.com/2019/09/06/sensor-filters-for-coders/
# realtime microphone audio volume: https://stackoverflow.com/questions/40138031/how-to-read-realtime-microphone-audio-volume-in-python-and-ffmpeg-or-similar

def stream_callback(indata, frames, time, status):
    global array_meanA
    global n
    global stream
    global start_time
    global lock_boolean

    # print("in stream callback")

    volume_norm = np.linalg.norm(indata) * 10

    # M: Replace end of array with volume_norm
    array_meanA[n] = int(volume_norm)

    # M: Shift elements left by 1
    for h in range(n):
        array_meanA[h] = array_meanA[(h + 1)]

    meanA = 0

    # M: Sum values in array_meanA
    for h in range(n):
        meanA = array_meanA[h] + meanA
    
    meanA = meanA / n

    print(meanA)
    """ 
    If meanA > 10 and lock_boolean, set start_time = datetime.now(). Else, set start_time = large number. lock_boolean = False.

    If (datetime.now()).total_seconds() - start_time >= 5 seconds, then warn student and lock_boolean = True
     """
    
    if meanA > 55 and lock_boolean:
        start_time = datetime.now()
        lock_boolean = False
    elif meanA <= 55:
        lock_boolean = True
        start_time = datetime(2022, 1, 1)
    
    if (datetime.now() - start_time).total_seconds() >= 5:
        warning = "Please lower your volume. Thank you!"
        tts = gTTS(warning, lang='en', tld='co.uk')
        tts.save("bot_warning.mp3")
        playsound('bot_warning.mp3')
        print(warning)

        lock_boolean = True
        start_time = datetime(2022, 1, 1)

''' NOTE:
Instead of subscribing to the same face_detection_topic, could have face_detection_clean publish a different topic called noise_detection_topic. '''
def listener_callback(data):
    global stream

    if data.data == 'no_detection':
        # print("Starting stream!")
        stream.start()
    else:
        print("Stopping stream!")
        stream.stop()
    
    # print("End of listener_callback")

def listener():
    # TOPIC TO BE CHANGED TO SOMETHING ELSE
    rospy.Subscriber('face_detection_topic', String, listener_callback)

    print("This statement is only called once!")

    # M: Keeps node from exiting until it is shutdown
    rospy.spin()

if __name__ == '__main__':
    try:
        start_time = datetime(2022, 1, 1)

        # M: Length of data to store in array
        n = 50
        # M: Added 0.0 for shifting values
        array_meanA = [0.0]

        # M: Initialize array with n values of 0.0
        for h in range(n):
            array_meanA.append(0.0)

        # Output: array_meanA = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0] --> 31 elements

        # M: Create node
        rospy.init_node('noise_detection', anonymous=True)


        stream = sd.InputStream(callback=stream_callback)

        lock_boolean = True

        listener()
    
    except Exception as e:
        print("Exception thrown: {}".format(e))