#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
import serial

class VelSubscriber(Node):

    def __init__(self):
        super().__init__("read_vel")
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.vel_callback, 10)
        #timer_period = 0.5
        #self.timer = self.create_timer(timer_period, self.vel_callback)    
        self.ser = serial.Serial('/dev/ttyUSB1', 115200)

    def vel_callback(self, msg):

        data2 = '*{};{};#'.format(msg.linear.x, msg.angular.z)
        data2 = '{}'.format(data2)
        data2 = str.encode(data2)

        self.ser.write(data2)
        self.get_logger().info('*{};{};#'.format(msg.linear.x, msg.angular.z))

    #def setVel(self, vel_A, vel_L):
    #    self.vel_A = vel_A
    #    self.vel_L = vel_L

def main(args=None):
    rclpy.init(args=args)

    subscriber = VelSubscriber()
    rclpy.spin(subscriber)

    subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 