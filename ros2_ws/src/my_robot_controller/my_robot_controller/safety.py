#!/usr/bin/env python3

import rospy
from sensor_msgs import RANGE
from std_msgs import Bool
import RPi._GPIO as gpio
import time
import rclpy
from rclpy.node import Node 


class Safety():


    def __init__(self):

        self.range = 3
        
        self.sub_sonar =rospy.Subscriber("preprocessing_sonar/", RANGE, 3)
        rospy.loginfo("subscriber set")

        self.pub_safety = rospy.Publisher("topic/publisher", Bool, queue_size=3)
        rospy.loginfo("Publisher set")

    def update_range(self, message): #fonction active à chaque fois qu'un message est publié par le sonar
        
        self.range=message.range

    def control_action(self) :
        range= self.range
        if self.range < Distance_min : 
            stop_action =


def listener(args=None):
    rclpy.init(args=args)
    rospy.Subscriber("chatter", String, callback)
    node= Safety()
    rclpy.spin(node) #continue tant qu'on a pas appuyé sur ^c
    rclpy.shutdown()



if __name__=="__main__": 
    try:
        listener()
    except rospy.ROSInterruptException:
        pass
