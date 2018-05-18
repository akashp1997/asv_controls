#!/usr/bin/env python

import rospy
import std_msgs.msg

def talker():
	rospy.init_node("force_talker")
	pub = rospy.Publisher("/left_force", std_msgs.msg.Float64, queue_size=10)
	pub_r = rospy.Publisher("/right_force", std_msgs.msg.Float64, queue_size=10)
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		pub.publish(1900)
		pub_r.publish(1100)
		rate.sleep()

talker()