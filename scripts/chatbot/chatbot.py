#!/usr/bin/env python
import aiml #M: Used in requesting AIML chatbot responses
import os # M: Used to get path of files
import rospy # M: Used in creating ROS nodes (publisher and subscriber)
import speech_recognition as sr # M: Used for recognizing user speech
from gtts import gTTS # M: Used in translating text response into speech
from playsound import playsound # M: Used to play bot_response.mp3
from std_msgs.msg import String

# QM: Insert regex maybe?

# M: Get directory path of current file
# NM: os.path.realpath(__file__) shows the path including the filename, so we wish to extract only the directory path
path = os.path.dirname(os.path.realpath(__file__))
# M: Concat to get path for setup.aiml file
path = path + '/aiml_files/setup.aiml'

print("setup_aiml file found at: %s" % path)

# M: Public interface to AIML interpreter
k = aiml.Kernel()
# M: Load the contents of setup AIML file into Kernel
k.learn(path)
# M: Get response from learned AIML file
# M: This will load the other AIML files
k.respond('LEARN AIML FILES')

# --- Setting up pub and sub stuff
# M: Used to publish topic for USB speaker
''' M:
Process flow: face_detection face detected -> chatbot.py listens to user commands -> retrieves bot response based on matching patterns in aiml files -> saves to mp3 file -> publishes to bot USB speaker '''
def talker():
    # M: Topic - Name: Speech, Type: String (requires import from std_msgs), queue_size: 10
    # M: Might have to do some remapping for the topic that the USB speaker will be subscribed to in launch files
    pub = rospy.Publisher('speech', String, queue_size=5)
    # M: Tells rospy name of node
    rospy.init_node('speech_recognition', anonymous=True)
    # M: Rate at which messages are published. In this case, 5Hz
    rate = rospy.Rate(5.0)
    # M: Initialize recognizer class (for recognizing speech)
    r = sr.Recognizer()



# M: Used to listen for topic from face_detection. When face_detection signals that it defects a face, then carry out chatbot function
# M: Consider having Boolean signal from face_detection, so if true, then chatbot.py, else noise detection
def listener():
    pass

# M: Informs us that this is an executable script
if __name__ == '__main__':
    try:
        talker()
    # M: Catch exceptions, such as when user presses ctrl+c
    except Exception as e:
        print(e)