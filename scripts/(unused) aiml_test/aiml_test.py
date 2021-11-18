#!/usr/bin/env python2.7
import aiml
import os

path = os.path.dirname(os.path.realpath(__file__))
print(path)
path = path + '/files_for_aiml/setup.aiml'

kernel = aiml.Kernel()
kernel.learn(path)
kernel.respond('LOAD FILES FOR AIML')

while True:
    print(kernel.respond(raw_input("Enter your message >> ")))