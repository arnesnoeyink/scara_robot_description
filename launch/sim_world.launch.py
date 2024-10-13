import os
import tempfile
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from pathlib import Path
from launch import LaunchDescription
from launch.event_handlers import OnShutdown
from launch.conditions import IfCondition
from launch.actions import IncludeLaunchDescription, DeclareLaunchArgument, SetEnvironmentVariable, ExecuteProcess, OpaqueFunction, RegisterEventHandler
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, PythonExpression

def generate_launch_description():

    scara_robot_description_dir = get_package_share_directory('scara_robot_description')

    headless = LaunchConfiguration('headless')
    world = LaunchConfiguration('world')
    use_simulator = LaunchConfiguration('use_simulator')

    declare_headless_cmd = DeclareLaunchArgument(
        'headless', 
        default_value='False', 
        description='Whether to execute gzclient'
    )

    declare_world_cmd = DeclareLaunchArgument(
        'world', 
        default_value= os.path.join(scara_robot_description_dir, 'worlds', 'test_world.sdf'), 
        description='Gz sim World'
    )

    declare_use_simulator_cmd = DeclareLaunchArgument(
        'use_simulator',
        default_value='True',
        description='Whether to start the simulator',
    )

    gz_sim_server = ExecuteProcess(
        cmd=['gz', 'sim', '-r', '-s', world],
        output='screen',
        condition=IfCondition(use_simulator)
    )

    gz_sim_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('ros_gz_sim'),
                         'launch',
                         'gz_sim.launch.py')
        ),
        condition=IfCondition(PythonExpression(
            [use_simulator, ' and not ', headless])),
        launch_arguments={'gz_args': ['-v 4 -g']}.items(),
    )

    ld = LaunchDescription()
    ld.add_action(declare_headless_cmd)
    ld.add_action(declare_use_simulator_cmd)
    ld.add_action(declare_world_cmd)
    ld.add_action(gz_sim_server)
    ld.add_action(gz_sim_client)

    return ld