#!/usr/bin/env python2
import aiml  # M: Used in requesting AIML chatbot responses
import os  # M: Used to get path of files
import rospy  # M: Used in creating ROS nodes (publisher and subscriber)
import speech_recognition as sr  # M: Used for recognizing user speech
from gtts import gTTS  # M: Used in translating text response into speech
from playsound import playsound  # M: Used to play bot_response.mp3
from std_msgs.msg import String
from datetime import datetime

# ----- (CURRENTLY UNUSED) - may use for publishing to speaker node
# # --- Setting up pub and sub stuff
# # M: Used to publish topic for USB speaker
# ''' M:
# Process flow: face_detection face detected -> chatbot.py listens to user commands -> retrieves bot response based on matching patterns in aiml files -> saves to mp3 file -> publishes to bot USB speaker '''
# def talker():
#     # M: Topic - Name: Speech, Type: String (requires import from std_msgs), queue_size: 10
#     # M: Might have to do some remapping for the topic that the USB speaker will be subscribed to in launch files
#     pub = rospy.Publisher('speech', String, queue_size=5)
#     # M: Tells rospy name of node
#     rospy.init_node('speech_recognition', anonymous=True)
#     # M: Rate at which messages are published. In this case, 5Hz
#     rate = rospy.Rate(5.0)
#     # M: Initialize recognizer class (for recognizing speech)
#     r = sr.Recognizer()

# M: Callback used to carry out chatbot functionality

''' Note:
It needs to receive the messages, but do nothing. '''

# def callback2(data):
#     if data.data == "function_complete":
        
#         print("Back here!")
#         print(lock_boolean)

def talker():
    print("Sending message to node!!!")

    

    # M: 10Hz = loop 10 times per second
    # M: f = 1 / t = 1 / 10 = 0.2 s per loop
    # rate = rospy.Rate(60) # 60hz

    pub.publish("do_function")

def callback(data):
    global lock_boolean
    # print(lock_boolean)

    # # TEST CODE
    # rospy.loginfo("Message received: %s" % data.data)

    # if data.data == "face_detected" and lock_boolean:
    #     lock_boolean = False

    #     # Initialize recognizer class (for recognizing the speech)
    #     r = sr.Recognizer()

    #     with sr.Microphone() as source:
    #         # https://www.geeksforgeeks.org/speech-recognition-in-python-using-google-speech-api/
    #         r.adjust_for_ambient_noise(source)
    #         audio_text = r.listen(source)

    #         # When no mic activity, close mic
    #         print("Time over, thanks!")

    #     try:
    #         # Converting the speech to text
    #         command = r.recognize_google(audio_text)

    #         if command == "exit":
    #             print("Exiting program!")
    #             return

    #         # Display user's command
    #         print("user > %s" % command)

    #         # Pass in user command to aiml file and retrieve bot response
    #         reply = k.respond(command)
    #         # Display bot response
    #         print("BOT >> %s" % reply)

    #         # Translate the bot response into speech
    #         tts = gTTS(reply, lang='en', tld='co.uk')
    #         # Save the speech into mp3 file to play
    #         tts.save('bot_response.mp3')
    #         # Play bot response
    #         playsound('bot_response.mp3')

    #     # Exception handling for mic cannot properly detect speech
    #     except Exception as e:
    #         print(e)
    #         print("user > ...")
    #         print("BOT >> Sorry, I did not get that...")
        
    #     start_time = datetime.now()

    #     while (datetime.now() - start_time).total_seconds() <= 5:
    #         continue
        
    #     lock_boolean = True
    
    # elif data.data == "face_detected" and not lock_boolean:
    #     pass

    # if completion_function == "completed":
    #     lock_boolean = True
    message = data.data

    print("message: {}; lock_boolean: {}".format(message, lock_boolean))

    if message == "face_detected" and lock_boolean:
        lock_boolean = False
        talker()
    elif message == "function_complete":
        start_time = datetime.now()

        print("Waiting for 5 seconds...")
        while (datetime.now() - start_time).total_seconds() <= 5:
            continue
        lock_boolean = True
    



def listener():
    # MQ: Shouldn't I move this somewhere else since this same node would be used as pub and sub, not only in listener?
    # MQ: Should I only create the chatbot node when there is a signal coming in? So once there is no signal, it dies?
    rospy.init_node('chatbot', anonymous=True)

    # M: Declare that node subscribes to topic. Messages received are passed to callback as first argument
    rospy.Subscriber('face_detection_topic', String, callback)
    # rospy.Subscriber('chatbot_function_topic', String, callback2)

    


    # M: Keeps python from exiting until node is stopped
    rospy.spin()


# M: Informs us that this is an executable script
if __name__ == '__main__':
    try:
        # # QM: Insert regex maybe?

        # ######### SETUP SECTION ########
        # # M: Get directory path of current file
        # # NM: os.path.realpath(__file__) shows the path including the filename, so we wish to extract only the directory path
        # path = os.path.dirname(os.path.realpath(__file__))
        # # M: Concat to get path for setup.aiml file
        # path = path + '/aiml_files/setup.aiml'

        # print("setup_aiml file found at: %s" % path)

        # # M: Public interface to AIML interpreter
        # k = aiml.Kernel()
        # # M: Load the contents of setup AIML file into Kernel
        # k.learn(path)
        # # M: Get response from learned AIML file
        # # M: This will load the other AIML files
        # k.respond('LEARNING AIML FILES')

        lock_boolean = True
        # M: Declares that node is publishing chatter topic, message type String (std_msgs.msg.String), which is a simple String container. queue_size is for when a subscriber is not receiving the messages fast enough
        pub = rospy.Publisher('chatbot_topic', String, queue_size=10)

        listener()
    # M: Catch exceptions, such as when user presses ctrl+c
    except Exception as e:
        print(e)
