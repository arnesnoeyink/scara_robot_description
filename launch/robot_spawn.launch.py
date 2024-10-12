import os
import xacro
from launch import LaunchDescription
from ament_index_python.packages import get_package_share_directory
from launch_ros.actions import Node


def generate_launch_description():

    robotXacroName ='scara'
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
        package='ros_gz_sim',
        executable='create',
        arguments=[ 
            '-name', robotXacroName, 
            '-topic', 'robot_description'
        ],
        output='screen'
    )

    rviz2 = Node(
        package='rviz2', 
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d' + os.path.join(get_package_share_directory('scara_robot_description'), 'rviz', 'scara.rviz')])

    return LaunchDescription([
        node_robot_state_publisher,
        spawn_entity,
        rviz2
        ])
