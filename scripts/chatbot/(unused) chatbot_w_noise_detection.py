#!/usr/bin/env python2
import aiml
import numpy as np
import os
import rospy
import sounddevice as sd
import speech_recognition as sr
from datetime import datetime
from gtts import gTTS
from playsound import playsound
from std_msgs.msg import String

def callback(data):
    rospy.loginfo("Messaged received: %s" % data.data)

    