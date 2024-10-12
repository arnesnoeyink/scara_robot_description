import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from pathlib import Path
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration

def generate_launch_description():

    scara_robot_description_dir = get_package_share_directory('scara_robot_description')

    gazebo_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            os.path.join(scara_robot_description_dir, 'worlds'), ':' +
            str(Path(scara_robot_description_dir).parent.resolve())
            ])
    
    arguments = LaunchDescription([
                DeclareLaunchArgument('world', default_value='test_world',
                          description='Gz sim World'),
                                     ])

    gazebo = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('ros_gz_sim'), 'launch'), '/gz_sim.launch.py']),
            launch_arguments=[
                ('gz_args', [LaunchConfiguration('world'),
                                '.sdf',
                                ' -v 4',
                                ' -r']
                )])
    
    return LaunchDescription([
        gazebo_resource_path,
        arguments,
        gazebo
        ])