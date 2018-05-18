#!/usr/bin/env python

import rospy
import std_msgs.msg

file = open("/home/akashp1997/pid_tune.txt", "w")

def listener():
	rospy.init_node("pid_analysis")
	rospy.Subscriber("/lin/odom", std_msgs.msg.Float64, callback)
	rospy.spin()

def callback(data):
	file.write(str(data.data)+"\n")
try:
	listener()
except:
	file.close()