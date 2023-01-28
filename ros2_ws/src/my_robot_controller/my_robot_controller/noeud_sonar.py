#!/usr/bin/env python3

import rospy
from sensor_msgs import RANGE
import RPi._GPIO as gpio
import time
import sys
import signal
import rclpy
from rclpy.node import Node 


class Noeud_Sonar(Node):




    def __init__(self, vitesse, trig, echo ):
        super().__init__("noeud_sonar")
        self.get_logger().info("démarrage du sonar")
        self.count=0
        self.trig= trig # à choisir
        self.echo= echo 
        self.create_timer(1,self.sonar)
        self.vitesse = vitesse # cm/s
        self.pub_array = []

    def sonar(self):
        #def pin d'entrée et de sortie
        gpio.setup(self.trig, gpio.OUT)
        gpio.setup(self.echo, gpio.IN)

        #Trigger broche truig et attend broche echo

        time.sleep(0.5)
        gpio.output(self.trig, False)
        time.sleep(0.1)
        gpio.output(self.trig, True) #envoie sig
        time.sleep(0.00001)
        gpio.output(self.trig, False)
        while gpio.input(self.echo) == False :
            start = time.time()
        while gpio.input(self.echo) == True :
            end = time.time()
        
        T = end - start
        distance = T * self.vitesse/2

        #Publication de distance dans le bon topic 

        topic_name="preprocessing_sonar/"
        pub=rospy.Publisher(topic_name,RANGE,queue_size=3)
        self.pub_array.append(pub)
        self.loginfo("publisher ok")
        
        distance = round(distance, 3) #info utile 

        print ('Center distance : %f cm'% distance)

        gpio.cleanup()
        sys.exit(0)
    

def main(args=None):
    rclpy.init(args=args)
    node= Noeud_Sonar(34.029,2,3)
    rclpy.spin(node) #continue tant qu'on a pas appuyé sur ^c
    rclpy.shutdown()


if __name__=="__main__": 
    main()