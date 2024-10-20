#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
import rclpy
from geometry_msgs.msg import Twist


class VelPublisher(Node):

    def __init__(self):
        super().__init__("set_vel")
        self.publlisher = self.create_publisher(Twist, 'cmd_vel', 10)
        timer_period = 0.1
        self.timer = self.create_timer(timer_period, self.vel_callback)    
        self.vel_L = 0.0
        self.vel_A = 0.0

    def vel_callback(self):
        msg = Twist()
        msg.linear.x = self.vel_L
        msg.linear.y = 0.0
        msg.linear.z = 0.0
        msg.angular.x = 0.0
        msg.angular.y = 0.0
        msg.angular.z = self.vel_A

        self.publlisher.publish(msg)
        self.get_logger().info('*{};{};#'.format(self.vel_A, self.vel_L))
    
    def setVel(self, vel_A, vel_L):
        self.vel_A = vel_A
        self.vel_L = vel_L

def main(args=None):
    rclpy.init(args=args)

    publisher = VelPublisher()
    rclpy.spin(publisher)

    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 