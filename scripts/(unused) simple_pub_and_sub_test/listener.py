#!/usr/bin/env python

## Simple talker demo that listens to std_msgs/Strings published 
## to the 'chatter' topic

import rospy
from std_msgs.msg import String

def callback(data):
    rospy.loginfo(rospy.get_caller_id() + 'I heard: %s', data.data)

def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    # M: Tells rospy name of subscriber node
    # M: Anon = True allows for multiple listener.py nodes
    rospy.init_node('listener', anonymous=True)

    # M: Declares that node subscribes to chatter topic, and when new messages are received, callback is invoked with the message as the first argument
    rospy.Subscriber('face_detection_topic', String, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if __name__ == '__main__':
    listener()
