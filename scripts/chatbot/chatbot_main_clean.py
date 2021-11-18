#!/usr/bin/env python2
import rospy  # M: Creating ROS nodes (publisher and subscriber)
from std_msgs.msg import String # M: Wrapper for String in ROS messages
from datetime import datetime # M: Making timers

def talker():
    print("Publishing do_function message!")

    ''' Note:
    Since the message is published only once per execution, there is no need for rate. '''
    pub.publish("do_function")

def callback(data):
    global lock_boolean

    # M: String message
    message = data.data

    print("message: {}; lock_boolean: {}".format(message, lock_boolean))

    if message == "face_detected" and lock_boolean:
        # M: Boolean used to lock and prevent new messages from carrying out statements inside if statement
        lock_boolean = False
        talker()
    
    elif message == "function_complete":
        # M: Set start_time to current time. Used in calculating duration
        start_time = datetime.now()

        print("Waiting for .25 second...")

        # M: Wait for .25 second before opening lock
        while ((datetime.now() - start_time).total_seconds() <= 0.25):
            continue

        print("Reopening lock!")

        # M: Reopen the lock
        lock_boolean = True         

def listener():
    # M: Subscribe to topic
    rospy.Subscriber('face_detection_topic', String, callback)
    # M: Keeps python from exiting until node is stopped
    rospy.spin()

# M: Informs that this is exectuable script
if __name__ == "__main__": 
    try:
        lock_boolean = True

        # M: Declares that node is publishing topic
        pub = rospy.Publisher('carry_out_function_topic', String, queue_size=10)

        # M: Create node
        rospy.init_node('chatbot_main', anonymous=True)

        listener()
    except Exception as e:
        print("Exception: {}".format(e))