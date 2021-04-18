#!/usr/bin/env /home/ckjensen/anaconda3/envs/parrot_mambo/bin/python
# -*- coding: utf-8 -*-
"""
Created on Tue Mar 26 14:38:23 2019

@author: ckielasjensen
"""

from geometry_msgs.msg import TwistStamped
from std_msgs.msg import Float64
import numpy as np
import rospy

# PERIOD = 10 # ms
FREQ = 100 # Hz
R = 10 # Radius in meters
OMEGA = 0.1 #0.14
GAMMA_TIME = False


def gamma_cb(time, gamma):
    gamma.data = time.data


if __name__ == '__main__':
    rospy.init_node('sinusoid_generator', anonymous=True)
    rate = rospy.Rate(FREQ)
    pub = rospy.Publisher('/mambo/cmd_vel', TwistStamped, queue_size=10)

    twist = TwistStamped()

    twist.header.frame_id = 'odom'

    if GAMMA_TIME:
        gamma = Float64()
        rospy.Subscriber('/gamma1', Float64, lambda x: gamma_cb(x, gamma))

    initTime = rospy.Time.now()
    while not rospy.is_shutdown():

        if not GAMMA_TIME:
            t = (rospy.Time.now()-initTime).to_sec()
        else:
            t = gamma.data

        # x0 = R*np.cos(OMEGA*t)
        # y0 = R*np.sin(OMEGA*t)
        # x1 = R*np.cos(OMEGA*t+2*np.pi/3)
        # y1 = R*np.sin(OMEGA*t+2*np.pi/3)
        # x2 = R*np.cos(OMEGA*t+4*np.pi/3)
        # y2 = R*np.sin(OMEGA*t+4*np.pi/3)

        twist.twist.linear.x = R*np.cos(OMEGA*t)
        twist.twist.linear.y = R*np.cos(OMEGA*t)

        # ps0.pose.position.x = x0
        # ps0.pose.position.y = y0
        # ps1.pose.position.x = x1
        # ps1.pose.position.y = y1
        # ps2.pose.position.x = x2
        # ps2.pose.position.y = y2

        twist.header.stamp = rospy.Time.now()

        pub.publish(twist)

        rate.sleep()