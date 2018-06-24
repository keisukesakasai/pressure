#! /usr/bin/env python3                                                                                      

import rospy
import std_msgs
import pressure.msg

import sys
import time
import NASCORX_System.device.TPG261 as TPG261

if __name__=='__main__':
    # initialize parameters
    # ---------------------
    nodename = 'tpg261_status'
    topicname = 'tpg261'
    rospy.init_node(nodename)
    host = rospy.get_param('~host')
    rate = rospy.get_param('~rate')

    # setup devices
    # -------------
    try:
        pfeiffer = TPG261.tpg261(host)
    except OSError as e:
        rospy.logerr("{e.strerror}. host={host}".format(**locals()))
        sys.exit()

    # setup ros
    # ---------
    pub = rospy.Publisher(topicname, pressure.msg.tpg261_values, queue_size=1)

    # start loop
    # ----------
    while not rospy.is_shutdown():
        ret = pfeiffer.query_pressure()

        d = pressure.msg.tpg261_values()
        d.ch1_value = ret
        pub.publish(d)

        time.sleep(rate)
        continue
