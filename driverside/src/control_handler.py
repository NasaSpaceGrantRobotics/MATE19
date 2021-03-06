#!/usr/bin/env python2
from ControlScheme import ControlScheme
import rospy
import yaml
from sensor_msgs.msg import Joy
from std_msgs.msg import Int8
import sys

# Calls the interpretJoyMsg method of the scheme ControlScheme whenever a joy message is received
# then it sends a twist message and a toggle message for the direction and light respectively


def receive_joy_data(data):
    scheme.interpret_joy_msg(data.axes, data.buttons)


def receive_scheme_index(data):
    print(data)
    print("scheme index : ", scheme.index)
    scheme.set_index(data.data)
    print(scheme.index)


if __name__ == "__main__":
    scheme = ControlScheme(rospy.myargv(argv=sys.argv)[1])
    scheme.parse_xml()
    scheme.interpret_joy_msg([None]*8, [None]*11)
    try:
        rospy.init_node("ControlHandler")
        rospy.Subscriber("joy", Joy, receive_joy_data)
        rospy.Subscriber("gui", Int8, receive_scheme_index)
        rate = rospy.Rate(50)
        while not rospy.is_shutdown():
            scheme.send_target_message()
            scheme.send_toggle_message()
            rate.sleep()
    except rospy.ROSInterruptException:
        pass
