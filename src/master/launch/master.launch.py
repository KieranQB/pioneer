from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.substitutions import FindPackageShare
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution

import launch


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="ariaNode",
                executable="ariaNode",
                arguments=[
                        '-rp', '/dev/ttyUSB0'
                ],
            ),
            # Node(
            #     package="rviz2",
            #     executable="rviz2",
            #     name='rviz2',
            # ),
            Node(
                package='tf2_ros',
                executable='static_transform_publisher',
                arguments = ['--x', '0.5', '--y', '0.2', '--z', '0', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'base', '--child-frame-id', 'cloud']
            ),
            Node(
                package='tf2_ros',
                executable='static_transform_publisher',
                arguments = ['--x', '0.5', '--y', '0.2', '--z', '0', '--yaw', '0', '--pitch', '0', '--roll', '0', '--frame-id', 'base', '--child-frame-id', 'oak-d_frame']
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([
                    PathJoinSubstitution([
                        FindPackageShare('master'),
                        'launch',
                        'controller.launch.py'
                    ])
                ])
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([
                    PathJoinSubstitution([
                        FindPackageShare('sick_scan_xd'),
                        'launch',
                        'sick_tim_7xx.launch.py'
                    ])
                ])
            ),
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource([
                    PathJoinSubstitution([
                        FindPackageShare('depthai_examples'),
                        'launch',
                        'stereo.launch.py'
                    ])
                ])
            )
        ]
    )