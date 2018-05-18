#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import serial
import time
linear = 0
angular = 0

c = 0.8 #Ratio of max back thrust to max forward thrust
r = 0.3 #Difference between thruster and COB of boat

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
	global linear, angular, c
	rate = rospy.Rate(100)
	pub_l = rospy.Publisher("/left_pwm", Float64, queue_size=10)
	pub_r = rospy.Publisher("/right_pwm", Float64, queue_size=10)
	while not rospy.is_shutdown():
		pwm_l = int(1500+linear-angular)
		pwm_r = int(1500+linear+angular)
		if(pwm_l>1900):
			pwm_l = 1900
		if(pwm_l<1100):
			pwm_l = 1100
		if(pwm_r>1900):
			pwm_r = 1900
		if(pwm_r<1100):
			pwm_r = 1100
		pub_l.publish(pwm_l)
		pub_r.publish(pwm_r)

		#rospy.loginfo("%d %d" % (int(1500+linear-angular),int(1500+linear+angular)))
		rate.sleep()

listener()
