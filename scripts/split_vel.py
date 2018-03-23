#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import std_msgs.msg
import geometry_msgs.msg
import nav_msgs.msg
import sensor_msgs.msg

odom = [0,0]
vel = [0,0]
THRUSTER_COB = 300 #Distance between thrusters and cob

def listener():
	rospy.init_node("accel_to_pwm")
	rospy.Subscriber("/vel", geometry_msgs.msg.TwistStamped, callback=pwm, callback_args=0)
	rospy.Subscriber("/cmd_vel", geometry_msgs.msg.Twist, callback=pwm, callback_args=1)
	rospy.Subscriber("/imu_data", sensor_msgs.msg.Imu, callback=pwm, callback_args=2)
	talker()
	rospy.spin()

def pwm(data, current):
	global odom, vel
	if(current==0):
		odom[0] = data.twist.linear.x
	elif current==1:
		vel = [data.linear.x, data.angular.z]
	elif current==2:
		odom[1] = data.angular_velocity.z


def talker():
	global odom, vel
	lin_odom = rospy.Publisher("/lin/odom", std_msgs.msg.Float64, queue_size=10)
	ang_odom= rospy.Publisher("/ang/odom", std_msgs.msg.Float64, queue_size=10)
	lin_cmd = rospy.Publisher("/lin/cmd", std_msgs.msg.Float64, queue_size=10)
	ang_cmd = rospy.Publisher("/ang/cmd", std_msgs.msg.Float64, queue_size=10)
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		rospy.loginfo(str(odom)+" "+str(vel))
		lin_odom.publish(odom[0])
		ang_odom.publish(odom[1])
		lin_cmd.publish(vel[0])
		ang_cmd.publish(vel[1])
		rate.sleep()

listener()