#!/usr/bin/env python3
from functools import partial
import random
import math

import rclpy
from rclpy.node import Node
from turtlesim.srv import Spawn


class TurtleSpawner(Node):
    def __init__(self):
        super().__init__('turtle_spawner')

        self.turtle_name_prefix = "turtle"
        self.turtle_counter = 0

        self.spawn_client = self.create_client(Spawn, "/spawn")

        # Timer: spawn a new turtle every 2 seconds
        self.spawn_turtle_timer = self.create_timer(2.0, self.spawn_new_turtle)

    def spawn_new_turtle(self):
        self.turtle_counter += 1

        name = self.turtle_name_prefix + str(self.turtle_counter)
        x = random.uniform(0.0, 11.0)
        y = random.uniform(0.0, 11.0)
        theta = random.uniform(0.0, 2 * math.pi)

        self.call_spawn_service(name, x, y, theta)

    def call_spawn_service(self, turtle_name, x, y, theta):
        while not self.spawn_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Waiting for spawn service...")

        request = Spawn.Request()
        request.name = turtle_name
        request.x = x
        request.y = y
        request.theta = theta

        future = self.spawn_client.call_async(request)

        # Pass request safely to callback
        future.add_done_callback(
            partial(self.callback_call_spawn_service, request=request)
        )

    def callback_call_spawn_service(self, future, request):
        try:
            response = future.result()

            if response is not None and response.name != "":
                self.get_logger().info(f"New alive turtle: {response.name}")
                self.get_logger().info(
                    f"Turtle {request.name} spawned at "
                    f"({request.x:.2f}, {request.y:.2f}, {request.theta:.2f})"
                )
            else:
                self.get_logger().error("Failed to spawn turtle")

        except Exception as e:
            self.get_logger().error(f"Service call failed: {str(e)}")


def main(args=None):
    rclpy.init(args=args)

    node = TurtleSpawner()
    rclpy.spin(node)

    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()