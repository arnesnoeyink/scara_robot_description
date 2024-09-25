import os
from ament_index_python.packages import get_package_share_directory
import launch
from launch_ros.actions import Node
import xacro

def generate_launch_description():

    position = [0.0, 0.0, 0.0] # [X, Y, Z]
    orientation = [0.0, 0.0, 0.0] # [Roll, Pitch, Yaw]

    pkg_name = 'scara_robot_description'
    file_subpath = 'description/robot_description.xacro'

    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw, 
        'use_sim_time': True}])
    
    spawn_entity = Node(
        package='gazebo_ros', 
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                   '-x', str(position[0]), 
                   '-y', str(position[1]), 
                   '-z', str(position[2]),
                   '-R', str(orientation[0]), 
                   '-P', str(orientation[1]), 
                   '-Y', str(orientation[2]),
                   '-entity', 'scara'],
        output='screen')
    
    rviz2 = Node(
        package='rviz2', 
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d' + os.path.join(get_package_share_directory('scara_robot_description'), 'rviz', 'scara.rviz')])

    return launch.LaunchDescription([node_robot_state_publisher,
                                     spawn_entity,
                                     rviz2])

