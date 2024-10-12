import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription

def generate_launch_description():

    scara_robot_description_dir = get_package_share_directory('scara_robot_description')
    odom_publisher_dir = get_package_share_directory('odom_publisher')
    
    # sim world
    sim_world = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(scara_robot_description_dir, 'launch'), '/sim_world.launch.py']))
    # spawn robot
    robot_spawn = IncludeLaunchDescription(
                  PythonLaunchDescriptionSource([os.path.join(scara_robot_description_dir, 'launch'), '/robot_spawn.launch.py']))
    # bridge
    bridge = IncludeLaunchDescription(
             PythonLaunchDescriptionSource([os.path.join(scara_robot_description_dir, 'launch'), '/bridge.launch.py']))
    # control
    control = IncludeLaunchDescription(
              PythonLaunchDescriptionSource([os.path.join(scara_robot_description_dir, 'launch'), '/control.launch.py']))
    # odom publsiher
    odom_publisher = IncludeLaunchDescription(
                     PythonLaunchDescriptionSource([os.path.join(odom_publisher_dir, 'launch'), '/odom_publisher.launch.py']))
    
    return LaunchDescription([
        sim_world,
        robot_spawn,
        bridge,
        control,
        odom_publisher
        ])