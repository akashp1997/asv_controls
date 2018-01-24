#!/usr/bin/env python
import rospy
import geometry_msgs.msg
import std_msgs.msg
import tf

max_ang_vel = 3800
max_accel = 5
dist = 10
rate_pub = 100

velocity = geometry_msgs.msg.Twist()
left_acceleration = geometry_msgs.msg.Twist()
right_acceleration = geometry_msgs.msg.Twist()
left_velocity = geometry_msgs.msg.Twist()
right_velocity = geometry_msgs.msg.Twist()
left_max_velocity = geometry_msgs.msg.Twist(geometry_msgs.msg.Vector3(15,0,0), geometry_msgs.msg.Vector3(0,0,0.39269908169))
left_min_velocity = geometry_msgs.msg.Twist(geometry_msgs.msg.Vector3(-10,0,0), geometry_msgs.msg.Vector3(0,0,-0.26179938779))
right_max_velocity = geometry_msgs.msg.Twist(geometry_msgs.msg.Vector3(15,0,0), geometry_msgs.msg.Vector3(0,0,-0.39269908169))
right_min_velocity = geometry_msgs.msg.Twist(geometry_msgs.msg.Vector3(-10,0,0), geometry_msgs.msg.Vector3(0,0,0.26179938779))


def set_velocity():
	global left_velocity
	global right_velocity
	global velocity
	velocity.linear.x = left_velocity.linear.x + right_velocity.linear.x
	velocity.linear.z = left_velocity.linear.z + right_velocity.linear.z
	velocity.angular.x = left_velocity.angular.x + right_velocity.angular.x
	velocity.angular.z = left_velocity.angular.z + right_velocity.angular.z

def velocity_publish():
	global left_velocity
	global right_velocity
	pub = rospy.Publisher("/asv/left_thruster_controller/velocity", geometry_msgs.msg.Twist, queue_size=10)
	pub1 = rospy.Publisher("/asv/right_thruster_controller/velocity", geometry_msgs.msg.Twist, queue_size=10)
	pub2 = rospy.Publisher("/asv/velocity", geometry_msgs.msg.Twist, queue_size=10)
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		set_velocity()
		pub.publish(left_velocity)
		pub1.publish(right_velocity)
		pub2.publish(velocity)
		rate.sleep()

def command_controller():
	rospy.init_node("thruster_control")
	rospy.Subscriber("/asv/left_thruster_controller/command", std_msgs.msg.Float64, left_accel_callback)
	rospy.Subscriber("/asv/right_thruster_controller/command", std_msgs.msg.Float64, right_accel_callback)
	velocity_publish()
	rospy.spin()

def left_accel_callback(data):
	global left_acceleration, max_ang_vel, max_accel, dist, rate_pub, left_velocity, left_acceleration
	ang_vel = float(data.data)
	left_acceleration = geometry_msgs.msg.Twist(geometry_msgs.msg.Vector3((float(max_accel)*ang_vel/max_ang_vel), 0, 0), geometry_msgs.msg.Vector3(0,0,(float(max_accel)*ang_vel/max_ang_vel/dist)))
	left_velocity.linear.x += left_acceleration.linear.x/100
	left_velocity.angular.z += left_acceleration.angular.z/100
	if(left_velocity.linear.x>left_max_velocity.linear.x):
		left_velocity.linear.x = left_max_velocity.linear.x
	if(left_velocity.angular.z>left_max_velocity.angular.z):
		left_velocity.angular.z = left_max_velocity.angular.z
	if(left_velocity.linear.x<left_min_velocity.linear.x):
		left_velocity.linear.x = left_min_velocity.linear.x
	if(left_velocity.angular.z<left_min_velocity.angular.z):
		left_velocity.angular.z = left_min_velocity.angular.z

def right_accel_callback(data):
	global right_acceleration, max_ang_vel, max_accel, dist, rate_pub, right_velocity, right_acceleration
	ang_vel = float(data.data)
	right_acceleration = geometry_msgs.msg.Twist(geometry_msgs.msg.Vector3((float(max_accel)*ang_vel/max_ang_vel), 0, 0), geometry_msgs.msg.Vector3(0,0,-(float(max_accel)*ang_vel/max_ang_vel/dist)))
	right_velocity.linear.x += right_acceleration.linear.x/rate_pub
	right_velocity.angular.z += right_acceleration.angular.z/rate_pub
	if(right_velocity.linear.x>right_max_velocity.linear.x):
		right_velocity.linear.x = right_max_velocity.linear.x
	if(right_velocity.angular.z<right_max_velocity.angular.z):
		right_velocity.angular.z = right_max_velocity.angular.z
	if(right_velocity.linear.x<right_min_velocity.linear.x):
		right_velocity.linear.x = right_min_velocity.linear.x
	if(right_velocity.angular.z>right_min_velocity.angular.z):
		right_velocity.angular.z = right_min_velocity.angular.z

command_controller()