#!/usr/bin/env
import rospy

import dynamic_reconfigure.client

def callback(config):
    rospy.loginfo("Config set to {int_param}, {double_param}, {str_param}, {bool_param}, {size}".format(**config))

if __name__ == "__main__":
    rospy.init_node("dynamic_client")

    rospy.wait_for_service("/lin/pid")
    client = dynamic_reconfigure.client.Client("/lin/pid", timeout=30, config_callback=callback)

    r = rospy.Rate(1)
    while not rospy.is_shutdown():
        client.get_configuration()
        r.sleep()