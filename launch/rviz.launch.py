import os
import xacro
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    ld = LaunchDescription()
    
    rviz2 = Node(
            package='rviz2', 
            executable='rviz2',
            name='rviz2',
            output='screen',
            arguments=['-d' + os.path.join(get_package_share_directory('scara_robot_description'), 'rviz', 'scara.rviz')])
    

    ld.add_action(rviz2)

    return ld