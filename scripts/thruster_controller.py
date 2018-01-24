#!/usr/bin/env python
import rospy
import geometry_msgs.msg
import std_msgs.msg

rospy.init_node("base_controller")

def velocity_listener():
	rospy.Subscriber("cmd_vel", geometry_msgs.msg.Twist, publisher)
	rospy.spin()

def publisher(twist):
	left_pub = rospy.Publisher("/asv/left_thruster_controller/command")
	max_velocity = 3800
	rate = rospy.Rate(1000)
	velocity = 0
	time = 3000 # in ms
	for i in range(time):
		velocity += std_msgs.msg.float64(float(max_velocity)/time)
	else:
		velocity = max_velocity
	left_pub.publisher(velocity)
	rate.sleep()
