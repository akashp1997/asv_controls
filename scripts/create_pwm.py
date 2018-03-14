#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import serial
import time
linear = 0
angular = 0

def listener():
	rospy.init_node("thuster_pwm")
	rospy.Subscriber("/lin/command", Float64, callback, callback_args=True)
	rospy.Subscriber("/ang/command", Float64, callback, callback_args=False)
	publish()
	rospy.spin()

def callback(data, lin):
	global linear, angular
	if lin:
		linear = data.data
	else:
		angular = data.data

def publish():
	global linear, angular
	rate = rospy.Rate(100)
	pub_l = rospy.Publisher("/left_pwm", Float64, callback)
	pub_r = rospy.Publisher("/right_pwm", Float64, callback)
	while not rospy.is_shutdown():
		left_pwm = 0.5*(linear-angular)+1500
		right_pwm = 0.5*(linear+angular)+1500
		pub_l.publish(left_pwm)
		pub_r.publish(right_pwm)
		rate.sleep()

listener()