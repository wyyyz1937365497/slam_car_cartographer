import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # ⚠️ 务必修改为你刚才创建的 slam_car.lua 的绝对路径
    configuration_directory = '/home/wyyyz/TJ/ROS_SLAM/ylidar/slam_car_cartographer/config'
    configuration_basename = 'slam_car.lua'

    return LaunchDescription([
        # 1. 发布 IMU 静态 TF (根据实际安装位置修改平移和旋转)
    # 1. 发布 IMU 静态 TF (根据实际安装位置：后67.43mm, 右34.46mm, 上41mm)
    # 1. 发布 IMU 静态 TF (精确安装位置：后67.43mm, 右34.46mm, 上41mm)
    # ROS坐标系: X前, Y左, Z上 => 偏移: x=-0.06743, y=-0.03446, z=0.041
    Node(
        package='tf2_ros',
        executable='static_transform_publisher',
        arguments=['-0.06743', '-0.03446', '0.041', '0', '0', '0', 'base_link', 'imu_link']
    ),
Node(
    package='tf2_ros',
    executable='static_transform_publisher',
    arguments=[
        '0.06',  # x平移（前方60mm，+0.06m）
        '0',     # y平移（中心线上，0m）
        '0.134',     # z平移（高度一致，0m）
        '0',  # roll（绕x轴0°，弧度）
        '0',     # pitch（绕y轴0°）
        '3.1416',     # yaw（绕z轴0°）
        'base_link',  # 父坐标系
        'laser_frame' # 子坐标系
    ]
),

    Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': False}],
            arguments=['-configuration_directory', configuration_directory,
                       '-configuration_basename', configuration_basename],
            remappings=[
                ('scan', '/scan'),          # 订阅你的激光话题
                ('imu', '/imu/data'),        # 订阅你的 IMU 话题
                ('odom', '/odom') 
            ]
        ),

        # 3. 启动地图栅格化节点 (将 Cartographer 的 submap 转为 /map 话题供 RViz 显示)
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='occupancy_grid_node',
            output='screen',
            parameters=[{'use_sim_time': False}],
            arguments=['-resolution', '0.05', '-publish_period_sec', '1.0']
        )
    ])
