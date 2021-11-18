#!/usr/bin/env python

## Simple talker demo that published std_msgs/Strings messages
## to the 'chatter' topic

# M: Need to import rospy to write a ROS node
import rospy
from std_msgs.msg import String

def talker():
    # M: Declares that node is publishing chatter topic, message type String (std_msgs.msg.String), which is a simple String container. queue_size is for when a subscriber is not receiving the messages fast enough
    pub = rospy.Publisher('chatter', String, queue_size=10)
    # M: Tells rospy name of node, which in this case is talker
    rospy.init_node('talker', anonymous=True)

    # M: 10Hz = loop 10 times per second
    # M: f = 1 / t = 1 / 10 = 0.2 s per loop
    rate = rospy.Rate(10) # 10hz

    # M: Checking if program should exit, e.g.: ^C
    while not rospy.is_shutdown():
        hello_str = "hello world %s" % rospy.get_time()

        # M: Similar to print statement
        rospy.loginfo(hello_str)

        # M: Publishes string to chatter topic
        pub.publish(hello_str)

        # M: Sleep just long enough to maintain desired rate through loop
        rate.sleep()

# M: Tells us that this is an executable script, and not a module?
if __name__ == '__main__':
    try:
        talker()
    # M: This exception will be thrown by rospy.Rate.sleep() when ctrl + c is pressed, or when node is shut down
    except rospy.ROSInterruptException:
        pass
