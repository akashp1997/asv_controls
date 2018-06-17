#!/usr/bin/env python
import rospy

import dynamic_reconfigure.client

rospy.init_node("dynamic_client")

def callback(data):
	rospy.loginfo(data)

client = dynamic_reconfigure.client.Client("/lin/pid", timeout=0.1)

r = rospy.Rate(1)


count = 1
while not rospy.is_shutdown():
	conf = client.get_configuration()
	rospy.loginfo(conf)
	client.update_configuration(conf)
	rospy.loginfo("Update")
	count += 1
	r.sleep()