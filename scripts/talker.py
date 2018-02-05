#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import geometry_msgs.msg

def talker():
    pub = rospy.Publisher('/asv/left_pwm', Float64, queue_size=10)
    pub2 = rospy.Publisher('/asv/right_pwm', Float64, queue_size=10)
    #listener = tf.TransformListener()
    rospy.init_node('talker')
    rate = rospy.Rate(100) # 10hz
    while not rospy.is_shutdown():
        #trans, rot = listener.lookupTransform('/thruster_left', '/base_footprint', rospy.Time(0));
        msg = 1600
        msg2 = 1600
        pub.publish(msg)
        pub2.publish(msg2)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass