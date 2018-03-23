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
		if angular==0:
			if linear>=0:
				x = linear/2
				y = linear/2
			else:
				x = -linear/(2*c)
				y = -linear/(2*c)
		elif angular>0:
			x = (0.5/c)*(angular/0.3-linear)
			y = (0.5)*(angular/0.3+linear)
		else:
			x = (0.5)*(angular/0.3+linear)
			y = (0.5/c)*(angular/0.3-linear)
		if x>400:
			x = 400
		if x<-400:
			x = -400
		if y>400:
			y = 400
		if y<-400:
			y = 400
		pub_l.publish(x+1500)
		pub_r.publish(y+1500)
		rate.sleep()

listener()
