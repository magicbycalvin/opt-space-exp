#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 18 00:02:11 2021

@author: ckjensen
"""

from geometry_msgs.msg import PoseStamped, PointStamped, Twist, TwistStamped
import numpy as np
from pyparrot.Minidrone import Mambo
import rospy
import tf


class MamboCommander:
    def __init__(self, ble_addr):
        self._cmd_sub = rospy.Subscriber('cmd_vel', TwistStamped)
        self._pos_pub = rospy.Publisher('pose', PoseStamped, queue_size=10)
        self._vel_pub = rospy.Publisher('twist', TwistStamped, queue_size=10)

        rospy.loginfo('Initializing mambo connection...')
        self.mambo = Mambo(ble_addr, use_wifi=False)
        self.mambo.connect(3)
        self.mambo.smart_sleep(1)
        self.mambo.ask_for_state_update()
        self.mambo.smart_sleep(1)
        rospy.loginfo('Mambo connection initialized.')

        # self.mambo.set_user_sensor_callback(self.send_pos, None)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        rospy.loginfo('Landing mambo...')
        self.mambo.safe_land(5)
        self.mambo.smart_sleep(3)
        rospy.loginfo('Mambo safely landed.')

        rospy.loginfo('Closing mambo connection...')
        self.mambo.disconnect()
        rospy.loginfo('Mambo connection closed.')

    def send_cmd(self, data):
        xvel = data.twist.linear.x
        yvel = data.twist.linear.y
        zpos = data.twist.linear.z

        self.mambo.fly_direct(roll=xvel, pitch=yvel, yaw=0.0, vertical_movement=zpos)

    def send_state(self):
        pose = PoseStamped()
        twist = TwistStamped()
        now = rospy.Time.now()
        pose.header.stamp = now
        twist.header.stamp = now
        pose.header.frame_id = 'odom'
        twist.header.frame_id = 'odom'

        sensor_data = self.mambo.sensors.sensors_dict
        pose.pose.position.x = sensor_data['DronePosition_posx']
        pose.pose.position.y = sensor_data['DronePosition_posy']
        pose.pose.position.z = sensor_data['DronePosition_posz']
        pose.pose.orientation.z = sensor_data['DronePosition_psi']
        twist.twist.linear.x = self.mambo.sensors.speed_x
        twist.twist.linear.y = self.mambo.sensors.speed_y

        self._pos_pub.publish(pose)
        self._vel_pub.publish(twist)


if __name__ == '__main__':
    rospy.init_node('mambo_ctrl', anonymous=True)
    ble_addr = rospy.get_param('ble_address')
    # ns = rospy.get_namespace()
    freq = rospy.get_param('ctrl_freq', 100)
    rate = rospy.Rate(freq)

    with MamboCommander(ble_addr) as mambo:
        mambo.mambo.safe_takeoff(5)
        while not rospy.is_shutdown():
            # run forever until ros is shut down
            rate.sleep()