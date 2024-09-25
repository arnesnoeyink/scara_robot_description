import os
from ament_index_python.packages import get_package_share_directory
import launch
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, TimerAction
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    gazebo =    IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')))
    

    scara_spawn_urdf =  IncludeLaunchDescription(
                        PythonLaunchDescriptionSource(
                        os.path.join(get_package_share_directory('scara_robot_description'), 'launch', 'scara_spawn_urdf.launch.py')))
    

    return launch.LaunchDescription([
        gazebo,
        scara_spawn_urdf
        ])