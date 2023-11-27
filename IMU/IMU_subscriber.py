#!/usr/bin/env python3
#coding=UTF-8

import rospy
import tf
from tf.transformations import *
from sensor_msgs.msg import Imu
import time

class IMUCommunication():
    def __init__(self) -> None:
        self.roll = 0
        self.pitch = 0
        self.yaw = 0 

    def callback(self, data):
        (r,p,y) = tf.transformations.euler_from_quaternion((data.orientation.x,data.orientation.y,data.orientation.z,data.orientation.w))

        self.roll = r*180/3.1415926
        self.pitch = p*180/3.1415926
        self.yaw = y*180/3.1415926

    def get_imu(self, function):
        rospy.init_node('get_imu', anonymous=True)
        rospy.Subscriber("/handsfree/imu", Imu, self.callback)
        frequency = 0.5
        rate = rospy.Rate(frequency)
        while not rospy.is_shutdown():
            function(-self.pitch)
            # print(self.pitch) #put the needed function here
            rate.sleep()
    
    def print_pitch(self):
        print(self.pitch)

if __name__ == '__main__':
    imuCommunication = IMUCommunication()
    imuCommunication.get_imu(imuCommunication.print_pitch)
