#!/usr/bin/env python2
import rospy
import yaml
from std_msgs.msg import Int8
from std_msgs.msg import Float64
from geometry_msgs.msg import Twist

# Calls the interpretJoyMsg method of the scheme ControlScheme whenever a joy message is received
# then it sends a twist message and a toggle message for the direction and light respectively


def receive_trans_x(data):
    control_effort.linear.x = data.data


def receive_trans_y(data):
    control_effort.linear.y = data.data


def receive_trans_z(data):
    control_effort.linear.z = data.data


def receive_rot_x(data):
    control_effort.angular.x = data.data


def receive_rot_y(data):
    control_effort.angular.y = data.data


def receive_rot_z(data):
    control_effort.angular.z = data.data


if __name__ == "__main__":
    twist_publisher = rospy.Publisher('/control_effort_final', Twist, queue_size=1)
    control_effort = Twist()

    print("test")
    try:
        rospy.init_node("VectorRecombiner")
        rospy.Subscriber("/control_effort/trans/x", Float64, receive_trans_x)
        rospy.Subscriber("/control_effort/trans/y", Float64, receive_trans_y)
        rospy.Subscriber("/control_effort/trans/z", Float64, receive_trans_z)
        rospy.Subscriber("/control_effort/rot/x", Float64, receive_rot_x)
        rospy.Subscriber("/control_effort/rot/y", Float64, receive_rot_y)
        rospy.Subscriber("/control_effort/rot/z", Float64, receive_rot_z)

        rate = rospy.Rate(10)
        while not rospy.is_shutdown():
            rate.sleep()
            twist_publisher.publish(control_effort)
    except rospy.ROSInterruptException:
        pass
