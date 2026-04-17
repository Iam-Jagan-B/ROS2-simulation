#!/usr/bin/env python3

import rclpy
import math
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist


class turtleController(Node):

    def __init__(self):
        super().__init__('turtle_controller')

        self.target_x = 8.0
        self.target_y = 4.0

        self.Pose_ = None   # ✅ FIX: initialize variable

        self.pose_subscription = self.create_subscription(
            Pose,
            '/turtle1/pose',
            self.pose_callback,
            10
        )

        self.cmd_vel_publisher = self.create_publisher(
            Twist,
            '/turtle1/cmd_vel',
            10
        )

        self.control_timer = self.create_timer(
            0.01,
            self.control_loop
        )

    def pose_callback(self, pose: Pose):
        self.Pose_ = pose

    def control_loop(self):

        if self.Pose_ is None:
            return

        dist_x = self.target_x - self.Pose_.x
        dist_y = self.target_y - self.Pose_.y

        # ✅ FIX: calculate distance properly
        distance = math.sqrt(dist_x**2 + dist_y**2)

        cmd_vel = Twist()

        if distance > 0.5:

            # Linear velocity
            cmd_vel.linear.x = 2 * distance

            # Angle to goal
            goal_theta = math.atan2(dist_y, dist_x)
            diff = goal_theta - self.Pose_.theta

            # Normalize angle
            if diff > math.pi:
                diff -= 2 * math.pi
            elif diff < -math.pi:
                diff += 2 * math.pi

            # Angular velocity
            cmd_vel.angular.z = 6 * diff

        else:
            # Stop turtle
            cmd_vel.linear.x = 0.0
            cmd_vel.angular.z = 0.0

        self.cmd_vel_publisher.publish(cmd_vel)


def main(args=None):
    rclpy.init(args=args)
    node = turtleController()
    rclpy.spin(node)
    rclpy.shutdown()


if __name__ == '__main__':
    main()