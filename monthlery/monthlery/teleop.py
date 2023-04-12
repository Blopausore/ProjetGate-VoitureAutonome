#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from getkey import getkey, keys
from covaps.msg import Order

HIGH_LIMIT_SPEED = 255
LOW_LIMIT_SPEED = -255
HIGH_LIMIT_ANG = 255
LOW_LIMIT_ANG = -255

class TeleopNode(Node):

    def __init__(self):
        super().__init__("Teleoperator_node")
        self.get_logger().info("Teleoperator node started")
        self.get_logger().info("press UP to speed up")
        self.get_logger().info("press DOWN to slow down")
        self.get_logger().info("press LEFT to turn left")
        self.get_logger().info("press RIGHT to turn right")
        self.get_logger().info("press I to get information on the car")
        self.get_logger().info("press S to stop the car")
        self.get_logger().info("press Q to quit")
        self.linearSpeed = 0
        self.angularPos = 0
        self.cmd_car = self.create_publisher(Order, "/monthlery/cmd_car", 10)

    def sendOrder(self, value, type):
        order = Order()
        order.val = value
        order.type = type
        self.cmd_car.publish(order)

    def readKey(self):
        res = True
        key = getkey()
        if (key == keys.UP):
            self.get_logger().info("speed up")
            if (self.linearSpeed < HIGH_LIMIT_SPEED) :
                self.linearSpeed += 1
            else :
                self.get_logger().info("reached limit")
            self.sendOrder(self.linearSpeed, "speed")
        elif (key == keys.DOWN):
            self.get_logger().info("slow down")
            if (self.linearSpeed > LOW_LIMIT_SPEED) :
                self.linearSpeed -= 1
            else :
                self.get_logger().info("reached limit")
            self.sendOrder(self.linearSpeed, "speed")
        elif (key == keys.LEFT):
            self.get_logger().info("turn left")
            if (self.angularPos < HIGH_LIMIT_ANG) :
                self.angularPos +=1
            else :
                self.get_logger().info("reached limit")
            self.sendOrder(self.angularPos,"angular")
        elif (key == keys.RIGHT):
            self.get_logger().info("turn right")
            if (self.angularPos < HIGH_LIMIT_ANG) :
                self.angularPos -= 1
            else :
                self.get_logger().info("reached limit")
            self.sendOrder(self.angularPos, "angular")
        elif (key == 'I'):
            self.get_logger().info("linear speed:" + str(self.linearSpeed))
            self.get_logger().info("angular position:" + str(self.angularPos))
        elif (key == 'S'):
            self.get_logger().info("car stopped")
            self.linearSpeed = 0
            self.angularPos = 0
            self.sendOrder(self.linearSpeed, "speed")
            self.sendOrder(self.angularPos, "angular")
        elif (key == 'Q'):
            self.get_logger().info("quit teleop")
            self.linearSpeed = 0
            self.angularPos = 0
            self.sendOrder(self.linearSpeed, "speed")
            self.sendOrder(self.angularPos, "angular")
            res = False    
        else :
            self.get_logger().info("invalid key used")
        return res

    def main(self):
        cntn = True
        while cntn :
            cntn = self.readKey()

def main(args=None):
    rclpy.init(args=args)
    node = TeleopNode()
    node.main()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
