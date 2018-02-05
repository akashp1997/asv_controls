#!/usr/bin/env python
import rospy
import geometry_msgs.msg
import std_msgs.msg

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
left_cmd = 1500
right_cmd = 1500
velocity = geometry_msgs.msg.Twist()

def listener():
	rospy.init_node("rpm_controller")
	rospy.Subscriber("/asv/left_thruster/command", std_msgs.msg.Float64, callback, callback_args=True)
	rospy.Subscriber("/asv/right_thruster/command", std_msgs.msg.Float64, callback, callback_args=False)
	global left_cmd, right_cmd, velocity
	rate = rospy.Rate(RATE_PUB)
	pub = rospy.Publisher("/asv/velocity", geometry_msgs.msg.Twist, queue_size=10)
	while not rospy.is_shutdown():
		linear = (left_cmd+right_cmd-(ZERO_PWM*2))*MAX_ACCEL/(MAX_PWM-ZERO_PWM)
		angular = (right_cmd-left_cmd)*MAX_ANG_ACCEL/(MAX_PWM-ZERO_PWM)
		accel = geometry_msgs.msg.Twist(geometry_msgs.msg.Vector3(linear,0,0), geometry_msgs.msg.Vector3(0,0,angular))
		velocity.linear.x += accel.linear.x/RATE_PUB
		velocity.angular.z += accel.angular.z/RATE_PUB
		rospy.loginfo(velocity)
		pub.publish(velocity)
		rate.sleep()
	rospy.spin()

def callback(data, args):
	global left_cmd, right_cmd
	left = args
	if(left):
		left_cmd = data.data
	else:
		right_cmd = data.data

listener()