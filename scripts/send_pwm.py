#!/usr/bin/env python
import serial
import rospy
import socket
import std_msgs.msg

rospy.init_node("send_pwm")
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
rate = rospy.Rate(100)
sock.connect(("192.168.0.100", 60000))

#if(rospy.has_param("~host")):
#	host = rospy.get_param("~host")
#if(rospy.has_param("~port")):
#	port = int(rospy.get_param("~port"))

pwml = 1500
pwmr = 1500

def listener():
	rospy.Subscriber("/left_pwm", std_msgs.msg.Float64, callback, callback_args=True)
	rospy.Subscriber("/right_pwm", std_msgs.msg.Float64, callback, callback_args=False)
	talker()
	rospy.spin()

def callback(data, left):
	global pwml, pwmr
	if(left):
		pwml = int(data.data)
	else:
		pwmr = int(data.data)

def talker():
	global pwml, pwmr
	while not rospy.is_shutdown():
		if(pwml>1900):
			pwml = 1900
		if(pwml<1100):
			pwml = 1100
		if(pwmr>1900):
			pwmr = 1900
		if(pwmr<1100):
			pwmr = 1100
		sock.send("%d:%d:|"%(pwml,pwmr))
		rospy.loginfo("%d:%d:|"%(pwml,pwmr))
		rate.sleep()

listener()