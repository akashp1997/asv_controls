#!/usr/bin/env python
import rospy

import geometry_msgs.msg

rospy.init_node("vel_talker")
msg = geometry_msgs.msg.Twist()
def talker():
	pub = rospy.Publisher("/cmd_vel", geometry_msgs.msg.Twist, queue_size=10)
	rate = rospy.Rate(100)
	while not rospy.is_shutdown():
		msg.angular.z = 0.3
		pub.publish(msg)
		rate.sleep()

talker()