import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
#from nav_msgs.msg import Odometry
import tf2_ros
from std_msgs.msg import Float32MultiArray
#from geometry_msgs.msg import PoseStamped, TransformStamped

number_laser_points = 1081
'''
def convertToAIdata2(obs, theta=90, number_points=18):
    angle_by_point = 360 / number_laser_points
    opening_index_0 = int((180 - theta) / angle_by_point)
    opening_index_1 = int((180 + theta) / angle_by_point)
    # Add points and so enlarged the opening angle until we got a suitable number of points
    while not ((opening_index_1 - opening_index_0) % number_points)  == 0 :
        if add_coast :
	    opening_index_0 -= 1
        else :
	    opening_index_1 += 1
    step = (opening_index_1 - opening_index_0)//number_points
    ai_list = [[laser_scan] for laser_scan in obs[opening_index_0 : opening_index_1 : step]]
    return ai_list
'''
def convertToAIdata(scanList) :
    length = len(scanList)
    indexStart = int(length/8)
    indexFinal = int(length*7/8)
    ListwithoutBackward = scanList[indexStart : indexFinal]
    lastList = []
    step = int(len(ListwithoutBackward)/18)
    for i in range(18):
        lastList.append(ListwithoutBackward[i*step])
    print(len(lastList))
    return lastList




class LidarToAi(Node):
    def __init__(self):
        super().__init__('laser_to_ai')
        self.sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.pub = self.create_publisher(Float32MultiArray,'/covaps/toAI', 10)

    def scan_callback(self, scan_msg):
        self.get_logger().info(str(scan_msg.ranges[500]))
        msg = Float32MultiArray()   
        #msg.data = convertToAIdata2(scan_msg.ranges)
        msg.data = convertToAIdata(scan_msg.ranges)
        self.pub.publish(msg)

def main(args=None):
    rclpy.init(args=args)
    node = LidarToAi()
    rclpy.spin(node)
    rclpy.shutdown()
    
if __name__ == '_main_':
    main()
