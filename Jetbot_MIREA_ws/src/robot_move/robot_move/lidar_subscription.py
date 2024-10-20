import rclpy.node as Node
from sensor_msgs.msg import LaserScan
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
        self.ws = 0.06
        self.AIM = 0.3
        self.Ti = 20
        self.Kp = 5
        self.Kd = 150
        self.Ki = self.Kp/self.Ti
        self.arr_of_diff = []
        self.l_pred = 0
        self.vel_ang_z = 0.0
        self.vel_lin_x = 0.0
        self.vel_publisher = VelPublisher()

    def set_velocity(self):
        self.vel_publisher.setVel(-(self.vel_lin_x + self.vel_ang_z*self.ws), -(self.vel_lin_x - self.vel_ang_z*self.ws))
    
    def listener_callback(self, msg):
        self.get_logger().info(msg.ranges)
        l = min(msg.ranges)
        self.arr_of_diff.append(l - self.AIM)
        if(len(self.arr_of_diff) > self.Ti):
            self.arr_of_diff.pop(0)
        self.vel_ang_z = (l - self.AIM)*self.Kp - (self.l_pred - l)*self.Kd + sum(self.arr_of_diff)*self.Ki
        self.vel_lin_x = 0.4
        self.l_pred = l
        self.set_velocity()
            

def main(args=None):
    rclpy.init(args=args)

    subscriber = LidarSubscription()
    rclpy.spin(subscriber)

    subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 