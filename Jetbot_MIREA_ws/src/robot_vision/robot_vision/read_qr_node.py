#!/usr/bin/env python3
#read_qr_node.py
import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2 
import rclpy
import sys


from message_filters import Subscriber, TimeSynchronizer

class ReadQRs(Node):

    def __init__(self):
        super().__init__("read_qr_node")
        self.flag = False

        self.subscription = self.create_subscription(Image, '/color/image_raw', self.img_callback, 10)
        self.br = CvBridge()

    def img_callback(self, data):
        self.get_logger().info('node qr run')
        current_frame = self.br.imgmsg_to_cv2(data)
        qrCodeDetector = cv2.QRCodeDetector()
        decodedText, points, _ = qrCodeDetector.detectAndDecode(current_frame)
        if decodedText not in ['']:
            with open('QR_data.txt', 'a+') as f:
                f.write(str(decodedText)+ '\n')
                sys.exit()

     
def main(args=None):
    rclpy.init(args=args)
    read_qrs = ReadQRs()
    rclpy.spin(read_qrs)
    read_qrs.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()