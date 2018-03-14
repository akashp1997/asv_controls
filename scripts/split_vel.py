#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import std_msgs.msg
import geometry_msgs.msg
import nav_msgs.msg

odom = [0,0]
vel = [0,0]
THRUSTER_COB = 300 #Distance between thrusters and cob

def listener():
	rospy.init_node("accel_to_pwm")
	rospy.Subscriber("/odom", nav_msgs.msg.Odometry, callback=pwm, callback_args=True)
	rospy.Subscriber("/cmd_vel", geometry_msgs.msg.Twist, callback=pwm, callback_args=False)
	talker()
	rospy.spin()

def pwm(data, current):
	if(current):
		odom = [data.twist.twist.linear.x, data.twist.twist.angular.z]
	else:
		vel = [data.linear.x, data.angular.z]


def talker():
	global odom, vel
	lin_odom = rospy.Publisher("/lin/odom", std_msgs.msg.Float64, queue_size=10)
	ang_odom= rospy.Publisher("/ang/odom", std_msgs.msg.Float64, queue_size=10)
	lin_cmd = rospy.Publisher("/lin/cmd", std_msgs.msg.Float64, queue_size=10)
	ang_cmd = rospy.Publisher("/ang/cmd", std_msgs.msg.Float64, queue_size=10)
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		lin_odom.publish(odom[0])
		ang_odom.publish(odom[1])
		lin_cmd.publish(vel[0])
		ang_cmd.publish(vel[1])
		rate.sleep()

listener()