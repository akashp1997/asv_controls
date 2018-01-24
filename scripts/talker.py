#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import geometry_msgs.msg

def talker():
    pub = rospy.Publisher('/asv/left_thruster_controller/command', Float64, queue_size=10)
    pub1 = rospy.Publisher('/asv/right_thruster_controller/command', Float64, queue_size=10)
    rospy.init_node('talker', anonymous=True)
    rate = rospy.Rate(100) # 10hz
    while not rospy.is_shutdown():
        rpm1 = 3800
        rpm2 = 3800
        pub.publish(rpm1)
        pub1.publish(rpm2)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass