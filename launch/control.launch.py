from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():

    pid_controller_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["pid_controller", "--controller-manager", "/controller_manager"],
    )

    joint_state_broadcaster_spawner = Node(
        package="controller_manager",
        executable="spawner",
        arguments=["joint_state_broadcaster", "--controller-manager", "/controller_manager"],
    )

    return LaunchDescription([
        joint_state_broadcaster_spawner,
        pid_controller_spawner
        ])




