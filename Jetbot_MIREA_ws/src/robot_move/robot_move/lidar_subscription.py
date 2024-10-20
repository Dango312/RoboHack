import rclpy
from rclpy.node import Node
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
from robot_move.set_vel import VelPublisher

class LidarSubscription(Node):
    def __init__(self):
        super().__init__('lidar_subscription')
        self.subscription = self.create_subscription(
            LaserScan,
            'scan',
            self.listener_callback,
            10
        )  
        self.publlisher = self.create_publisher(Twist, 'cmd_vel', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.vel_callback)  

        self.ws = 0.06
        self.AIM = 0.3
        self.Ti = 20
        self.Kp = 2
        self.Kd = 15
        self.Ki = self.Kp/(self.Ti)
        self.arr_of_diff = []
        self.l_pred = 0
        self.vel_ang_z = 0.0
        self.vel_lin_x = 0.0
        self.vel_publisher = VelPublisher()


    def vel_callback(self):
        msg = Twist()
        msg.linear.x = -self.vel_lin_x
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = -self.vel_ang_z

        self.publlisher.publish(msg)
        self.get_logger().info('*{};{};#'.format(-self.vel_ang_z, -self.vel_lin_x))

    #def set_velocity(self):
    #    self.vel_publisher.setVel(-(self.vel_lin_x + self.vel_ang_z*self.ws), -(self.vel_lin_x - self.vel_ang_z*self.ws))
    
    def listener_callback(self, msg):
        l = min(msg.ranges)
        self.get_logger().info(f'{l}')
        self.arr_of_diff.append(l - self.AIM)
        if(len(self.arr_of_diff) > self.Ti):
            self.arr_of_diff.pop(0)
        self.vel_ang_z = (l - self.AIM)*self.Kp - (self.l_pred - l)*self.Kd + sum(self.arr_of_diff)*self.Ki
        if(self.vel_ang_z < -0.75):
            self.vel_ang_z = -0.75
        if(self.vel_ang_z > 0.75):
            self.vel_ang_z = 0.75 
        self.vel_lin_x = 0.4
        self.l_pred = l
            

def main(args=None):
    rclpy.init(args=args)

    subscriber = LidarSubscription()
    rclpy.spin(subscriber)

    subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 