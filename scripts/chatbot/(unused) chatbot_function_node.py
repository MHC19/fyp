#!/usr/bin/env python2
import aiml  # M: Used in requesting AIML chatbot responses
import os  # M: Used to get path of files
import rospy  # M: Used in creating ROS nodes (publisher and subscriber)
import speech_recognition as sr  # M: Used for recognizing user speech
from gtts import gTTS  # M: Used in translating text response into speech
from playsound import playsound  # M: Used to play bot_response.mp3
from std_msgs.msg import String
from datetime import datetime

''' I could have another node that receives a message from the chatbot node, and then sends back a completion signal, to allow for simulataneous operation.
The problem now is that when the function is finished, the previous messages come in. So if, there are 2 face_detected messages, then first message received, carry out function, then second message received, carry out function, then finished. '''


def talker():
    global pub

    # M: 10Hz = loop 10 times per second
    # M: f = 1 / t = 1 / 10 = 0.2 s per loop
    rate = rospy.Rate(60)  # 60hz

    pub.publish("function_complete")


def callback(data):
    print("In chatbot_function_node callback")

    talker()
    
    if data.data == "do_function":
        r = sr.Recognizer()

        with sr.Microphone() as source:
            # https://www.geeksforgeeks.org/speech-recognition-in-python-using-google-speech-api/
            r.adjust_for_ambient_noise(source)
            audio_text = r.listen(source)

            # When no mic activity, close mic
            print("Time over, thanks!")

        try:
            # Converting the speech to text
            command = r.recognize_google(audio_text)

            if command == "exit":
                print("Exiting program!")
                return

            # Display user's command
            print("user > %s" % command)

            # Pass in user command to aiml file and retrieve bot response
            reply = k.respond(command)
            # Display bot response
            print("BOT >> %s" % reply)

            # Translate the bot response into speech
            tts = gTTS(reply, lang='en', tld='co.uk')
            # Save the speech into mp3 file to play
            tts.save('bot_response.mp3')
            # Play bot response
            playsound('bot_response.mp3')

        # Exception handling for mic cannot properly detect speech
        except Exception as e:
            print(e)
            print("user > ...")
            print("BOT >> Sorry, I did not get that...")
        pass

        talker()
    pass


def listener():
    rospy.Subscriber('chatbot_topic', String, callback)

    rospy.spin()


if __name__ == '__main__':
    try:
        rospy.init_node('chatbot_function_node', anonymous=True)

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
        k.respond('LEARNING AIML FILES')

        # M: Declares that node is publishing chatter topic, message type String (std_msgs.msg.String), which is a simple String container. queue_size is for when a subscriber is not receiving the messages fast enough
        pub = rospy.Publisher('face_detection_topic', String, queue_size=10)
        listener()
        
    
    except Exception as e:
        print("Exception thrown: {}".format(e))
