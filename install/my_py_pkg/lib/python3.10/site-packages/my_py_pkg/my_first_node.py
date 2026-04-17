#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

class my_node(Node):
    def __init__(self):
        super().__init__('my_first_node')
        self.get_logger().info('Hello ROS2')
        self.create_timer(1.0, self.timer_callback)
        self.counter=0
    def timer_callback(self):
        self.counter += 1
        self.get_logger().info(f'ROS2 timer callback {self.counter}')
        

def main (args=None):
    rclpy.init(args=args)
    node=my_node()
    rclpy.spin(node)
    rclpy.shutdown() 

if __name__=='__main__':
    main()   