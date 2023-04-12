##
#%%
import numpy
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from nav_msgs.msg import Odometry
from nav_msgs.msg import OccupancyGrid
from math import sqrt, atan, pi
import os

from std_msgs.msg import Float32MultiArray
from stable_baselines3 import PPO

from covaps.msg import Order
print(os.getcwd())
models_path = "./src/"

model_name = "model"

class AI(Node):
    number_laser_points = 1081
    model = PPO.load(models_path + model_name)#mettre le nom du dossier qui contient le modèle

    def __init__(self, **kargs):
        super().__init__("ai_node")

        self.laser_scan = Odometry()
        self.occupancy = OccupancyGrid()
        self.odometry = Odometry()

        ## PUBLISHER

        self.cmd_vel_publisher = self.create_publisher(
                Twist, "ai_node/topic/twist", 10
        )

        ## SUBSCRIBER
        self.laser_scan_subscriber = self.create_subscription(
            Odometry, "localisation/topic/odometry",self.callback_laser_scan,10
        )
        self.occupancy_grid_subscriber = self.create_subscription(
            OccupancyGrid, "map_server/topic/occupancy_grid",self.callback_occupancy,10
        )
        self.odometry_subscriber = self.create_subscription(
            Odometry, "odometry/topic/odometry",self.callback_odometry,10
        )
        self.get_logger().info("AI abstract node has been started")

    def callback_laser_scan(self,odometry : Odometry):
        self.laser_scan = odometry

    def callback_occupancy(self,occupancy : OccupancyGrid):
        self.occupancy = occupancy

    def callback_odometry(self,odometry : Odometry):
        self.odometry = odometry


##
#%%

class AINode(AI):
    def __init__(self, **kargs):
        super().__init__(**kargs)

        # Publisher
        self.cmd_car = self.create_publisher(Order, "/monthlery/cmd_car", 10)
        # Subscriber
        self.sub_car = self.create_subscription(
                Float32MultiArray, "/covaps/toAI", self.callback_pub, 10
        )
        
        # End initialize
        self.get_logger().info(" node has been started")
        

    def callback_pub(self, array : Float32MultiArray):
        
        data = wrapperDupauvre(array.data) 
        action, _ = self.model.predict(
            data,
            deterministic=True
        )
        
        self.get_logger().info(str(array.data[0]))
        Sx, Sy = numpy.float32(action[0]), numpy.float32(action[1])

        linear_speed, angular_speed = get_lin_and_ang_speed(Sx, Sy)

        order_angular = create_order("angular", angular_speed)
        self.cmd_car.publish(order_angular)
        order_linear = create_order("speed", linear_speed)
        self.cmd_car.publish(order_linear)
        
        self.get_logger().info("Model predict: {}".format(str(action[0])))
    
    def angle_opening(self, obs, theta=45, number_points=17):
        ''' Return the point that are in the opening angle in the direction of the car
        PARAMETERS
        ----------
            theta : float
                Angle in degree
        '''
        angle_by_point = 360 / self.number_laser_points
        opening_index_0 = int((180 - theta) / angle_by_point)
        opening_index_1 = int((180 + theta) / angle_by_point)
        add_coast = True #True for index_0 and so False for index_1
        # Add points and so enlarged the opening angle until we got a suitable number of points
        while not (opening_index_1 - opening_index_0) % number_points == 0:
            if add_coast:
                opening_index_0-=1
            else:
                opening_index_1+=1
            add_coast = not add_coast
        step = (opening_index_1 - opening_index_0)//number_points

        return obs[opening_index_0 : opening_index_1 : step]
        
##
#%%


        
                
        

##
#%%


        
def create_order(type_, val_):
    order = Order()
    order.val = int(val_)
    order.type = type_
    return order

def get_lin_and_ang_speed(Sx, Sy):
    linear_speed = sqrt(Sx**2 + Sy**2)
    if Sx ==0:
        if Sy > 0:
            angular_speed = pi/2
        elif Sy < 0:
            angular_speed = -pi/2
        else:
            angular_speed = 0
    else:
        angular_speed = atan(Sy/Sx)
    if Sx < 0:
        linear_speed = -linear_speed
    return linear_speed, angular_speed

def wrapperDupauvre(listfloat) :
    returnedList = []
    for val in listfloat :
        returnedList.append([val])
    return returnedList

def main(args=None):

    rclpy.init(args=args)
    node = AINode()
    rclpy.spin(node)
    rclpy.shutdown()

