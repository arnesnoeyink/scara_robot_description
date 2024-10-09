import os
from ament_index_python.packages import get_package_share_directory
import launch
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

def generate_launch_description():
    
    scara_spawn =   IncludeLaunchDescription(PythonLaunchDescriptionSource(
                    os.path.join(get_package_share_directory('scara_robot_description'), 'launch', 'scara_spawn.launch.py')))

    scara_control =     IncludeLaunchDescription(PythonLaunchDescriptionSource(
                        os.path.join(get_package_share_directory('scara_robot_description'), 'launch', 'scara_control.launch.py')))

    return launch.LaunchDescription([
        scara_spawn
        # ,
        # scara_control
        ])