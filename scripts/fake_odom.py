#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import geometry_msgs.msg
import nav_msgs.msg
import tf

odom = nav_msgs.msg.Odometry()
posewithcovariance = geometry_msgs.msg.PoseWithCovariance()
pose = geometry_msgs.msg.Pose()
twistwithcovariance = geometry_msgs.msg.TwistWithCovariance()

def listener():
	rospy.init_node("fake_odom")
	rospy.Subscriber("/asv/velocity", geometry_msgs.msg.Twist, odom_generator)
	rospy.spin()

def odom_generator(velocity):
	global odom
	global posewithcovariance
	global twistwithcovariance
	global pose
	rate_pub = 100
	rate = rospy.Rate(rate_pub)
	twist = velocity
	pose.position.x += twist.linear.x/rate_pub
	pose.position.y += twist.linear.y/rate_pub
	pose.position.z += twist.linear.z/rate_pub
	quat = tf.transformations.quaternion_from_euler(twist.angular.x/100, twist.angular.y/100, twist.angular.z/100)
	pose.orientation.w += quat[0]
	pose.orientation.x += quat[1]
	pose.orientation.y += quat[2]
	pose.orientation.z += quat[3]
	covariance = [0]*36
	posewithcovariance.covariance = covariance
	posewithcovariance.pose = pose
	twistwithcovariance.covariance = covariance
	twistwithcovariance.twist = twist
	odom.header.stamp = rospy.Time()
	odom.header.frame_id = "odom"
	odom.child_frame_id = "base_footprint"
	tf_broadcaster = tf.TransformBroadcaster()
	tf_broadcaster.sendTransform((pose.position.x, pose.position.y, pose.position.z), (pose.orientation.w, pose.orientation.x, pose.orientation.y, pose.orientation.z), rospy.Time(), "base_link", "world")
	odom.pose = posewithcovariance
	odom.twist = twistwithcovariance
	pub = rospy.Publisher("/odom", nav_msgs.msg.Odometry, queue_size=10)
	pub.publish(odom)
	rate.sleep()

listener()