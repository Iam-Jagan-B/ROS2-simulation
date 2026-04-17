#!/usr/bin/env python3
from tokenize import String

import rclpy
from rclpy.node import Node
from example_interfaces.msg import String
class RobotNewsStation(Node):
    def __init__(self):
        super().__init__('robot_news_station')
        self.publishers_=self.create_publisher(String, 'news', 10)
        self.timer_= self.create_timer(0.5, self.timer_callback)
    def timer_callback(self):
        self.publish_news("Hello, ROS2!")
    def publish_news(self, news):
        msg=String()
        msg.data=news
        self.publishers_.publish(msg)
        self.get_logger().info(f'Published news: {news}')

def main (args=None):
    rclpy.init(args=args)
    node=RobotNewsStation()
    rclpy.spin(node)
    rclpy.shutdown() 

if __name__=='__main__':
    main()   