#!/usr/bin/env python
import rospy
from std_msgs.msg import Float64
import geometry_msgs.msg

def talker():
    pub = rospy.Publisher('/asv/left_force', geometry_msgs.msg.Wrench, queue_size=10)
    pub2 = rospy.Publisher('/asv/right_force', geometry_msgs.msg.Wrench, queue_size=10)
    #listener = tf.TransformListener()
    rospy.init_node('talker')
    rate = rospy.Rate(100) # 10hz
    while not rospy.is_shutdown():
        #trans, rot = listener.lookupTransform('/thruster_left', '/base_footprint', rospy.Time(0));
        msg = geometry_msgs.msg.Wrench(geometry_msgs.msg.Vector3(1,0,0), geometry_msgs.msg.Vector3(0,0,0.1))
        msg2 = geometry_msgs.msg.Wrench(geometry_msgs.msg.Vector3(1,0,0), geometry_msgs.msg.Vector3(0,0,-1))
        pub.publish(msg)
        pub2.publish(msg2)
        rate.sleep()

if __name__ == '__main__':
    try:
        talker()
    except rospy.ROSInterruptException:
        pass