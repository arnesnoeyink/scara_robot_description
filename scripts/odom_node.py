# #!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
import gazebo_msgs.srv  

class odom_node(Node):
    def __init__(self):
        super().__init__("odom_node")
        self.create_timer(0.1, self.timer_callback)
        self.odom_pub = self.create_publisher(Odometry, '/odom', 10)
        self.link = gazebo_msgs.srv.GetEntityState.Request()
        self.link.name = 'link_03'
        self.link.reference_frame = 'world'
        self.get_link_srv = self.create_client(gazebo_msgs.srv.GetEntityState, '/get_entity_state')
        self.odom = Odometry()
        self.odom.header.frame_id = '/odom'

    def timer_callback(self):
        self.odom_pub.publish(self.odom)

def main(args=None):
    rclpy.init(args=args)
    node = odom_node()
    while rclpy.ok():
        try:
            while not node.get_link_srv.wait_for_service(timeout_sec=1.0):
                node.get_logger().info('service not available, waiting again...')
            resp = node.get_link_srv.call_async(node.link)
            rclpy.spin_until_future_complete(node, resp)
            node.odom.pose.pose = resp.result().state.pose
            node.odom.twist.twist = resp.result().state.twist
            node.odom.header.stamp = node.get_clock().now().to_msg()
        except KeyboardInterrupt:
            pass
    rclpy.shutdown()

if __name__ == "__main__":
    main()