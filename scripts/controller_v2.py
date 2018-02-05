#!/usr/bin/env python
import rospy
import geometry_msgs.msg
import std_msgs.msg
import math

MAX_PWM = 1900				#of each thruster
ZERO_PWM = 1500
MIN_PWM = 1100
MAX_LINEAR_ACCEL = 4				#linear accel of the boat
NO_THRUSTER = 2				#no of thrusters in the boat
MAX_TIME = 2				#in s
MAX_ACCEL = MAX_LINEAR_ACCEL/NO_THRUSTER	#linear accel per thruster
THRUSTER_COB = 0.3			#cob to each thruster
MAX_ANG_ACCEL = MAX_ACCEL/THRUSTER_COB
RATE_CHANGE_ACCEL_PWM = MAX_ANG_ACCEL/(MAX_PWM-ZERO_PWM)
RATE_CHANGE_ACCEL = RATE_CHANGE_ACCEL_PWM/MAX_TIME
RATE_PUB = 100				#100hz
pwm = [1500,1500]
cmd_vel = geometry_msgs.msg.Twist()
cur_vel = geometry_msgs.msg.Twist()
pid = [0.95,0,0]

def listener():
	global pwm
	rospy.init_node("thruster_controller")
	rospy.Subscriber("/cmd_vel", geometry_msgs.msg.Twist, callback, callback_args=True)
	rospy.Subscriber("/asv/velocity", geometry_msgs.msg.Twist, callback, callback_args=False)
	pub_l = rospy.Publisher("/asv/left_thruster/command", std_msgs.msg.Float64, queue_size=10)
	pub_r = rospy.Publisher("/asv/right_thruster/command", std_msgs.msg.Float64, queue_size=10)
	rate = rospy.Rate(RATE_PUB)
	while not rospy.is_shutdown():
		pwm = pwm_fun(pwm)
		rpm_l = pwm[0]-pwm[1]*0.5
		rpm_r = pwm[0]+pwm[1]*0.5
		rospy.loginfo(cur_vel)
		pub_l.publish(rpm_l)
		pub_r.publish(rpm_r)
		rate.sleep()

	rospy.spin()

def callback(data, args):
	cmd = args
	if(cmd):
		cmd_vel = data
	else:
		cur_vel = data

def pwm_fun(arr):
	return [arr[0]+pid[0]*(cmd_vel.angular.z-cur_vel.angular.z)*(400/MAX_ANG_ACCEL), arr[1]+pid[0]*(cmd_vel.angular.z-cur_vel.angular.z)*(800/MAX_ANG_ACCEL)]


listener()