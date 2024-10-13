import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    scara_robot_description_dir = get_package_share_directory('scara_robot_description')
    odom_publisher_dir = get_package_share_directory('odom_publisher')

    use_rviz = LaunchConfiguration('use_rviz')
    headless = LaunchConfiguration('headless')

    declare_use_rviz_cmd = DeclareLaunchArgument(
        'use_rviz', default_value='True', description='Whether to start RVIZ'
    )

    declare_headless_cmd = DeclareLaunchArgument(
        'headless', default_value='False', description='Whether to execute gzclient)'
    )
    
    # sim world
    sim_world = IncludeLaunchDescription(
                PythonLaunchDescriptionSource([os.path.join(scara_robot_description_dir, 'launch'), '/sim_world.launch.py']),
                launch_arguments={'headless': headless}.items())
    # spawn robot
    robot_spawn = IncludeLaunchDescription(
                  PythonLaunchDescriptionSource([os.path.join(scara_robot_description_dir, 'launch'), '/robot_spawn.launch.py']))
    # start rviz
    rviz2 = IncludeLaunchDescription(
                  PythonLaunchDescriptionSource([os.path.join(scara_robot_description_dir, 'launch'), '/rviz.launch.py']),
                  condition=IfCondition(use_rviz))
    # bridge
    bridge = IncludeLaunchDescription(
             PythonLaunchDescriptionSource([os.path.join(scara_robot_description_dir, 'launch'), '/bridge.launch.py']))
    # control
    control = IncludeLaunchDescription(
              PythonLaunchDescriptionSource([os.path.join(scara_robot_description_dir, 'launch'), '/control.launch.py']))
    # odom publsiher
    odom_publisher = IncludeLaunchDescription(
                     PythonLaunchDescriptionSource([os.path.join(odom_publisher_dir, 'launch'), '/odom_publisher.launch.py']))
    
    ld = LaunchDescription()
    ld.add_action(declare_use_rviz_cmd)
    ld.add_action(declare_headless_cmd)
    ld.add_action(sim_world)
    ld.add_action(robot_spawn)
    ld.add_action(rviz2)
    ld.add_action(bridge)
    ld.add_action(control)
    ld.add_action(odom_publisher)

    return ld