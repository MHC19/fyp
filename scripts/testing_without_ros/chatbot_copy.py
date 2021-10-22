import aiml
import numpy as np
import re
import os
import sounddevice as sd
import speech_recognition as sr
from datetime import datetime
from gtts import gTTS
from playsound import playsound

# Regex pattern to clean up user inputs
regex = re.compile('[^a-zA-Z0-9\s]')

# Get directory path of current file
path = os.path.dirname(os.path.realpath(__file__))
# Add string to get to setup.aiml file
path = path + '/aiml/setup.aiml'
print(path)

# Public interface to AIML interpreter
k = aiml.Kernel()
# Load contents of setup AIML file into kernel
k.learn(path)
# Get response from learned AIML file
# This will load the other AIML files
k.respond('LEARN AIML FILES')

def test_function():
    # while True:
    # Initialize recognizer class (for recognizing the speech)
    r = sr.Recognizer()

    with sr.Microphone() as source:
        audio_text = r.listen(source)
        
        # When no mic activity, close mic
        print("Time over, thanks!")

    try:
        # Converting the speech to text
        command = r.recognize_google(audio_text)

        if command == "exit":
            print("Exiting program!")
            # break

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