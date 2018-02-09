#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import geometry_msgs.msg

def talker():
    rospy.init_node('talker', anonymous=True)
    pub = rospy.Publisher('/cmd_vel', geometry_msgs.msg.Twist, queue_size=10)
    rate = rospy.Rate(100) # 10hz
    while not rospy.is_shutdown():
    	twist = geometry_msgs.msg.Twist(geometry_msgs.msg.Vector3(1,0,0), geometry_msgs.msg.Vector3(0,0,0.3))
    	pub.publish(twist)
        #rospy.loginfo(twist)
        #pub2.publish(cur_vel)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass