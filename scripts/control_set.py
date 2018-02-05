#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import std_msgs.msg
import geometry_msgs.msg
import nav_msgs.msg

THRUSTER_COB = 0.3

def talker():
	rospy.init_node("thruster_control_splitter")
	rospy.Subscriber("/cmd_vel", geometry_msgs.msg.Twist, callback)
	rospy.Subscriber("/odom", nav_msgs.msg.Odometry, feedback)
	rospy.spin()

def callback(data):
	x = data.linear.x
	z = data.angular.z
	pub_l = rospy.Publisher("/left_thruster/cmd_vel", std_msgs.msg.Float64, queue_size=10)
	pub_r = rospy.Publisher("/right_thruster/cmd_vel", std_msgs.msg.Float64, queue_size=10)
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		if(not data):
			w_l = 0
			w_r = 0
		w_l = 0.5*(x/THRUSTER_COB-z)
		w_r = 0.5*(x/THRUSTER_COB+z)
		pub_l.publish(w_l)
		pub_r.publish(w_r)
		rate.sleep()

def feedback(data):
	x = data.twist.twist.linear.x
	z = data.twist.twist.angular.z
	pub_l = rospy.Publisher("/left_thruster/odom", std_msgs.msg.Float64, queue_size=10)
	pub_r = rospy.Publisher("/right_thruster/odom", std_msgs.msg.Float64, queue_size=10)
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		if(not data):
			w_l = 0
			w_r = 0
		w_l = 0.5*(x/THRUSTER_COB-z)
		w_r = 0.5*(x/THRUSTER_COB+z)
		pub_l.publish(w_l)
		pub_r.publish(w_r)
		rate.sleep()	

talker()