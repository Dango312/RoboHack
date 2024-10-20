import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Quaternion
import serial


class OdometryPublisher(Node):

    def __init__(self):
        super().__init__("odometry_publisher")
        self.publlisher = self.create_publisher(Odometry, 'odom', 10)
        timer_period = 0.5
        self.timer = self.create_timer(timer_period, self.vel_callback)    
        self.ser = serial.Serial('/dev/ttyUSB1', 115200)

    def vel_callback(self):
        msg = Odometry()
        response = self.ser.readline().decode('utf-8')
        [x, y, v_l, v_a] = response.split(";")

        msg.header.stamp = self.get_clock().now().to_msg()
        msg.pose.pose.position.x = x
        msg.pose.pose.position.y = y
        msg.pose.pose.position.z = 0
        msg.pose.pose.orientation = Quaternion(
            x=0,
            y=0,
            z=0,
            w=1
        )
        msg.twist.twist.linear.x = v_l
        msg.twist.twist.angular.z = v_a

        self.publlisher.publish(msg)
        self.get_logger().info('*{};{};{};{}#'.format(v_a, v_l, x, y))

def main(args=None):
    rclpy.init(args=args)

    publisher = OdometryPublisher()
    rclpy.spin(publisher)

    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main() 