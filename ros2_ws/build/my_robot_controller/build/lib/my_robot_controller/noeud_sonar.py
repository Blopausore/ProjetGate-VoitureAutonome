#!/usr/bin/env python3


import RPi.GPIO as gpio
import time
import sys
import signal
import rclpy
from rclpy.node import Node 


class Noeud_Sonar(Node):

    def __init__(self):
        super().__init__("noeud_sonar")
        self.get_logger().info("Le noeud est créé")



    def main(args=None):
        rclpy.init(args=args)

        node= Noeud_Sonar()
        rclpy.spin(node)

        count =0
        print("hello :", count )
        count+=1


        rclpy.shutdown()


if __name__=="__main__": 
    main()