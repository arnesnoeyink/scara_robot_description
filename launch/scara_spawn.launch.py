import os
from ament_index_python.packages import get_package_share_directory
import launch
import xacro
from pathlib import Path
from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription, RegisterEventHandler, TimerAction, DeclareLaunchArgument, SetEnvironmentVariable
from launch.event_handlers import OnProcessStart
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition, UnlessCondition
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    #position = [0.0, 0.0, 0.0] # [X, Y, Z]
    #orientation = [0.0, 0.0, 0.0] # [Roll, Pitch, Yaw]

    #robot_description_path = os.path.join(get_package_share_directory('robot_description'))
    #acs_robot_sim_path = os.path.join(get_package_share_directory('robot_gazebo'))

    robotXacroName ='scara'
    pkg_name = 'scara_robot_description'
    file_subpath = 'description/robot_description.xacro'
    world_file_path = os.path.join(get_package_share_directory('scara_robot_description'),'world', 'world.sdf')
    world_path = '/home/arne/jazzy_ws/install/scara_robot_description/share/scara_robot_description/world/world.sdf'


    xacro_file = os.path.join(get_package_share_directory(pkg_name),file_subpath)
    robot_description_raw = xacro.process_file(xacro_file).toxml()
    scara_robot_description_dir = get_package_share_directory('scara_robot_description')

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_raw, 
        'use_sim_time': True}])
    
    # Set gazebo sim resource path
    gazebo_resource_path = SetEnvironmentVariable(
        name='GZ_SIM_RESOURCE_PATH',
        value=[
            os.path.join(scara_robot_description_dir, 'worlds'), ':' +
            str(Path(scara_robot_description_dir).parent.resolve())
            ]
        )

    arguments = LaunchDescription([
                DeclareLaunchArgument('world', default_value='test_world',
                          description='Gz sim World'),
                                     ]
    )

    gazebo = IncludeLaunchDescription(
            PythonLaunchDescriptionSource([os.path.join(
                get_package_share_directory('ros_gz_sim'), 'launch'), '/gz_sim.launch.py']),
            launch_arguments=[
                ('gz_args', [LaunchConfiguration('world'),
                                '.sdf',
                                ' -v 4',
                                ' -r']
                )
            ]
            )

    # gazebo_rosPackageLaunch = PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('ros_gz_sim'), 'launch', 'gz_sim.launch.py'))

    # gz_sim = IncludeLaunchDescription(
    #     gazebo_rosPackageLaunch, 
    #     launch_arguments={'gz_args': ['-r -v -v4 empty.sdf'], 'on_exit_shutdwon': 'true' }.items()
    # )
    # gz_sim = IncludeLaunchDescription(
    #     gazebo_rosPackageLaunch, 
    #     launch_arguments={'gz_args': ['-r -v -v4' + world_path], 'on_exit_shutdwon': 'true' }.items()
    # )
    
    # DONE
    spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[ 
            '-name', robotXacroName, 
            '-topic', 'robot_description'
        ],
        output='screen'
    )

    # DONE
    GzRosBridge = Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            output='screen',
            arguments=[
                '/world/empty/control@ros_gz_interfaces/srv/ControlWorld',
                '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
                '/joint_states@sensor_msgs/msg/JointState[gz.msgs.Model',
                '/scara/base_link_link_01_position_controller/command@std_msgs/msg/Float64@gz.msgs.Double',
                '/scara/link_01_link_02_position_controller/command@std_msgs/msg/Float64@gz.msgs.Double',
                '/scara/link_02_link_03_position_controller/command@std_msgs/msg/Float64@gz.msgs.Double'
                #,
                #'/world/empty/remove@ros_gz_interfaces/srv/DeleteEntity',
            ]
        )
    # bridge_params = os.path.join(scara_robot_description_dir, 'config', 'bridge_parameters.yaml')

    # startGazeboRosBridgeCmd = Node(
    #     package='ros_gz_bridge',
    #     executable='parameter_bridge',
    #     arguments=[
    #     '--ros-args', 
    #     '-p',
    #     f'config_file:={bridge_params}',   
    # ],
    # output='screen',
    # )
    
    # DONE
    rviz2 = Node(
        package='rviz2', 
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d' + os.path.join(get_package_share_directory('scara_robot_description'), 'rviz', 'scara.rviz')])

    return launch.LaunchDescription([
        node_robot_state_publisher,
        arguments,
        gazebo_resource_path,
        gazebo,
        # startGazeboRosBridgeCmd,
        spawn_entity,
        rviz2,
        GzRosBridge
        ])
