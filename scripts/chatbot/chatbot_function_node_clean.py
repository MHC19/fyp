#!/usr/bin/env python2
import aiml  # M: Working with AIML files
import os # M: Get path of files 
import rospy  # M: Creating ROS nodes (publisher and subscriber)
import speech_recognition as sr  # M: Recognizing user speech
from gtts import gTTS  # M: Convert text to speech
from playsound import playsound  # M: Play mp3 files
from std_msgs.msg import String # M: Wrapper for String in ROS messages

def talker():
    global pub
    pub.publish("function_complete")

    # Troubleshooting
    # print("Function complete!")

def callback(data):
    # M: messages from subscribed ROS topic
    message = data.data

    if message == "do_function":
        r = sr.Recognizer()
        
        try:
            ''' 
            Note:
            Problem: Code stays stuck on listen() as it's dependant on mic activity. Only when mic is completely silent, will it continue with following statements.
            Future improvement: Include way to manually start or stop the mic. Could use timers and noise level detection as well.
            '''
            with sr.Microphone() as source:
                # # https://www.geeksforgeeks.org/speech-recognition-in-python-using-google-speech-api/
                # r.adjust_for_ambient_noise(source, duration=1)

                # https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst
                # M: timeout used for when user takes too long to mention command
                # Improvement: Method to stop listen() - either push to talk, or key to end
                audio_text = r.listen(source)

            # M: Converting speech to text
            command = r.recognize_google(audio_text)

            # M: Display user's command
            print("USER > {}\n".format(command))

            # M: Retrieve bot response from AIML files
            reply = k.respond(command)

            # M: Display bot's response
            print("BOT >> {}\n\n".format(reply))

            # M: Translate bot's response into speech data
            tts = gTTS(reply, lang='en', tld='co.uk')
            # M: Save speech data into mp3 file
            tts.save('bot_response.mp3')
            # M: Play mp3 file
            playsound('bot_response.mp3')
        
        except Exception as e:
            # Troubleshooting
            # print("WARNING --> Exception: {}\n".format(e))

            print("USER > ...\n")

            error_response = "Sorry, I did not get that...\n\n"

            print("BOT >> " + error_response)

            # M: Translate bot's response into speech data
            tts = gTTS(error_response, lang='en', tld='co.uk')
            # M: Save speech data into mp3 file
            tts.save('bot_response.mp3')
            # M: Play mp3 file
            playsound('bot_response.mp3')

        
        # M: Chatbot function is complete, so call talker() to publish function_complete message and inform chatbot_main_clean to change lock_boolean
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

        print('setup.aiml file found at: {}'.format(path))

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