#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import std_msgs.msg
import geometry_msgs.msg
import nav_msgs.msg

THRUSTER_COB = 0.3
cmd_vel = [0,0]
odom = [0,0]


def listener():
	rospy.init_node("thruster_control_splitter")
	rospy.Subscriber("/cmd_vel", geometry_msgs.msg.Twist, callback, callback_args=True)
	rospy.Subscriber("/odom", nav_msgs.msg.Odometry, callback, callback_args=False)
	talker()
	rospy.spin()

def callback(data, cmd):
	global cmd_vel, odom
	"""This function publishes the required angular velocity for each thruster as float value."""
	if cmd==True:
		cmd_vel = [data.linear.x, data.angular.z]
		#rospy.loginfo(cmd_vel)
	else:
		odom = [data.twist.twist.linear.x, data.twist.twist.angular.z]

def talker():
	global cmd_vel, odom
	cmd_pub_l = rospy.Publisher("/left_thruster/cmd_vel", std_msgs.msg.Float64, queue_size=10)
	cmd_pub_r = rospy.Publisher("/right_thruster/cmd_vel", std_msgs.msg.Float64, queue_size=10)
	odom_pub_l = rospy.Publisher("/left_thruster/odom", std_msgs.msg.Float64, queue_size=10)
	odom_pub_r = rospy.Publisher("/right_thruster/odom", std_msgs.msg.Float64, queue_size=10)
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		l_cmd = 0.5*(cmd_vel[0]/THRUSTER_COB-cmd_vel[1])
		r_cmd = 0.5*(cmd_vel[0]/THRUSTER_COB+cmd_vel[1])
		l_odom = 0.5*(odom[0]/THRUSTER_COB-odom[1])
		r_odom = 0.5*(odom[0]/THRUSTER_COB+odom[1])
		cmd_pub_l.publish(l_cmd)
		cmd_pub_r.publish(r_cmd)
		odom_pub_l.publish(l_odom)
		odom_pub_r.publish(r_odom)
		rospy.loginfo(str(l_cmd)+" "+str(r_cmd)+"|"+str(l_odom)+" "+str(r_odom))
		rate.sleep()

listener()