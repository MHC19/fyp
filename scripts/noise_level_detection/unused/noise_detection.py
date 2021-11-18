#!/usr/bin/env python2
import numpy as np
import rospy
import sounddevice as sd # M: Used in getting mic volume
from datetime import datetime
from std_msgs.msg import String

''' M:
Requires converting to pub and sub for ROS.
Don't set duration, but instead make it run infinitely when no face is detected.
Need to collect data for how loud ambient noise is. '''

n = 30

# Adding 0.0 for shifting
array_meanA = [0.0]

# Initialize array with n values of 0.0
for h in range(n):
    array_meanA.append(0.0)

# Duration in which the caller(inputStream) is put to sleep
duration = 30
timer_on = False

def audio_callback(indata, frames, time, status):
    global array_meanA 
    global n
    global timer_on
    global start_time
    global current_time

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

    # --- TEST CODE ---

    # If the sound is loud and the timer is not on
    if meanA >= 10 and not timer_on:

        # print("Too loud. Please lower your volume...")
        # Start timer
        start_time = datetime.now()
        print("Here")
        timer_on = True
    
    # Timer is off
    # Sound is low, so can turn off timer
    elif meanA < 10:
        # print("Okay")
        timer_on = False
        print("Accepting commands")

    current_time = datetime.now()

    if timer_on == False:
        start_time = current_time
    
    timer_duration = (current_time - start_time).total_seconds()

    if timer_duration >= 5:
        print("Loud for 5 seconds...")
        start_time = datetime.now()

    # ----- UNUSED CODE -----

    # # print(meanA)
    
    # # # If the timer is not on, then enter this statement
    # # if meanA >= 1 and (not timer_on):
    # #     start_time = datetime.now()
    # #     print(start_time)

    # #     # Timer is on
    # #     timer_on = True

    # current_time = datetime.now()

    # # If meanA is low, then turn timer off
    # if meanA < 1:
    #     start_time = current_time
    #     timer_on = False
        
    # # start_time referenced here before declaration
    # timer = (current_time - start_time).total_seconds()

    # if timer >= 1:
    #     # Reset start_time
    #     start_time = datetime.now()
    #     timer = 0
    #     print("You have been noisy for 3 seconds. Please lower your volume...")
    #     timer_on = False
    
    # else:
    #     print("Still quiet.")


with sd.InputStream(callback=audio_callback) as stream:
    # https://python-sounddevice.readthedocs.io/en/0.3.14/api.html#sounddevice.sleep
    # Puts caller to sleep
    sd.sleep(duration * 1000)