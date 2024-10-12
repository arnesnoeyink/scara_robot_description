from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    GzRosBridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        output='screen',
        arguments=[
            '/world/empty/control@ros_gz_interfaces/srv/ControlWorld',
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock'
        ]
    )

    return LaunchDescription([GzRosBridge])
