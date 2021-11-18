#!/usr/bin/env python2
import aiml  # M: Used in requesting AIML chatbot responses
import os  # M: Used to get path of files
import rospy  # M: Used in creating ROS nodes (publisher and subscriber)
import speech_recognition as sr  # M: Used for recognizing user speech
from gtts import gTTS  # M: Used in translating text response into speech
from playsound import playsound  # M: Used to play bot_response.mp3
from std_msgs.msg import String  # NOTE: Get explanation from ROS wiki
import keyboard


def talker():
    global pub

    print("Function complete!")

    pub.publish("function_complete")


def callback(data):
    message = data.data
    r = sr.Recognizer()

    if message == "do_function":
        r = sr.Recognizer()

        # ''' Note:
        # Might have to find a way to manually start and stop mic.
        # Also try to include timers and noise level detection, since currently it is dependant on mic activity. When mic is shut off, only it proceeds with next statement. '''
        # with sr.Microphone() as source:
        #     # # https://www.geeksforgeeks.org/speech-recognition-in-python-using-google-speech-api/
        #     # r.adjust_for_ambient_noise()

        #     audio_text = r.listen(source)
        #     # if keyboard.read_key() == "c":
        #     #     return
        #     print("Stopping listening, thanks!")
        #     ''' Push to talk function, while key is pressed, listen to user. once let go, then move onto next line. '''
        print("Enter your command:")
        audio_text = str(raw_input()).upper()

    try:

        print(len(audio_text))
        # return

        # M: Converting speech to text
        # command = r.recognize_google(audio_text)
        command = audio_text

        # M: Display user's command
        print("USER > {}\n".format(command))

        # M: Pass in user's command and retrieve bot response using AIML
        reply = k.respond(command)

        print("\nCurrent topic: " + k.getPredicate("topic") + "\n\n")

        # M: Display bot's response
        print("BOT >> {}\n\n".format(reply))

        # M: Translate bot's response into speech data
        tts = gTTS(reply, lang='en', tld='co.uk')
        # M: Save speech data into mp3 file
        tts.save('bot_response.mp3')
        # M: Play mp3 file
        playsound('bot_response.mp3')

    except Exception as e:
        print("WARNING --> Exception: {}\n".format(e))
        print("USER > ...\n")

        error_response = "Sorry, I did not get that...\n\n"

        print("BOT >> " + error_response)

        # M: Translate bot's response into speech data
        tts = gTTS(error_response, lang='en', tld='co.uk')
        # M: Save speech data into mp3 file
        tts.save('bot_response.mp3')
        # M: Play mp3 file
        playsound('bot_response.mp3')

    # M: Chatbot function is complete, so call talker() to publish function_complete message and inform chatbot_main_clean
    talker()


def listener():
    rospy.Subscriber('carry_out_function_topic', String, callback)
    # M: Keeps python from exiting until node is stopped
    rospy.spin()


if __name__ == '__main__':
    try:
        rospy.init_node('chatbot_function', anonymous=True)

        # M: Get directory path of current file. os.path.realpath(__file__) shows the path including the filename, so we wish to extract only the directory path
        path = os.path.dirname(os.path.realpath(__file__))

        # M: Concat to get path for setup.aiml file
        path = path + '/aiml_files/setup.aiml'

        # print('setup.aiml file found at: {}'.format(path))

        # M: Public interface to AIML interpreter
        k = aiml.Kernel()
        # M: Load contents of setup.aiml file into kernel
        k.learn(path)
        # M: Get response from learned AIML file. This loads all other AIML files (refer to setup.aiml)
        k.respond('LEARNING AIML FILES')

        # M: Declare that node is publishing to topic. In this case, it is the same topic as face_detection.py
        pub = rospy.Publisher('face_detection_topic', String, queue_size=10)

        listener()

    except Exception as e:
        print("Exception thrown: {}".format(e))
