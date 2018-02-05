#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import std_msgs.msg
import geometry_msgs.msg
import nav_msgs.msg

MASS = 25
MAX_FORCE = 50
THRUSTER_COB = 0.3
NO_THRUSTERS = 2
MAX_PWM = 1900
ZERO_PWM = 1500
MIN_PWM = 1100
RATIO = ((MAX_FORCE/MASS/NO_THRUSTERS)*THRUSTER_COB)/(MAX_PWM-ZERO_PWM)

def listener():
	rospy.init_node("accel_to_pwm")
	rospy.Subscriber("/left_thruster/command", std_msgs.msg.Float64, callback=pwm, callback_args=True)
	rospy.Subscriber("/right_thruster/command", std_msgs.msg.Float64, callback=pwm, callback_args=False)
	rospy.spin()

def pwm(data, left):
	if(left):
		pub = rospy.Publisher("/left_pwm", std_msgs.Float64, queue_size=10)
	else:
		pub = rospy.Publisher("/right_pwm", std_msgs.Float64, queue_size=10)
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		pub.publish(1500+data.data/RATIO)
		rate.sleep()

listener()