from launch import LaunchDescription
from launch_ros.actions import Node
import os
from ament_index_python.packages import get_package_share_directory

import launch


def generate_launch_description():
    return LaunchDescription(
        [
            Node(
                package="nmea_navsat_driver",
                executable="nmea_serial_driver",
                parameters=[
                    os.path.join(
                        get_package_share_directory("master"), "config/gps.yaml"
                    )
                ],
            ),
        ]
    )

