#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

class MonNoeud(Node):

    def __init__(self):
        super().__init__("premier_noeud")
        self.get_logger().info("hello ros 2")

def main(args=None):

    rclpy.init(args=args)
    node = MonNoeud()
    rclpy.spin(node)
    rclpy.shutdown()



if __name__=='__main__':
    main()

