import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # ⚠️ 务必修改为你实际 slam_car.lua 的绝对路径
    configuration_directory = '/home/wyyyz/TJ/ROS_SLAM/ylidar/slam_car_cartographer/config'
    configuration_basename = 'slam_car.lua'
    
    return LaunchDescription([
        # ========================================================================
        # 1. 发布 IMU 静态 TF (精确物理安装位置)
        # 物理位置: 后侧 6mm, 右侧 41mm, 距底盘 12mm
        # ROS坐标系(父): X前, Y左, Z上  => 偏移: x=-0.006, y=-0.041, z=0.012
        # 旋转关系: IMU物理方向(X右, Y前, Z上) 相当于 ROS标准方向 绕Z轴旋转 -90度
        # ========================================================================
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '-0.006',   # x: 后侧 6mm (-0.006m)
                '-0.041',   # y: 右侧 41mm (ROS Y轴向左为正，故右侧为负)
                '0.012',    # z: 距底盘 12mm (+0.012m)
                '0.0',  # yaw:
                '0.0',      # pitch
                '0.0',      # roll
                'base_link',# 父坐标系
                'imu_link'  # 子坐标系
            ]
        ),

        # ========================================================================
        # 2. 发布 激光雷达 静态 TF (精确物理安装位置)
        # 物理位置: 正上方，距底盘 136mm (假设前后左右无偏移，均在中心线上)
        # ========================================================================
        Node(
            package='tf2_ros',
            executable='static_transform_publisher',
            arguments=[
                '0.0',      # x: 前后无偏移
                '0.0',      # y: 左右无偏移
                '0.136',    # z: 距底盘 136mm (+0.136m)
                '1.5707',      # yaw: 默认雷达朝前 (X轴朝前)。⚠️如果雷达实际朝后安装，请改为 3.1416
                '0.0',      # pitch
                '0.0',      # roll
                'base_link',# 父坐标系
                'laser_frame' # 子坐标系 (需与雷达驱动发布的 frame_id 保持一致)
            ]
        ),

        # ========================================================================
        # 3. Cartographer 节点
        # ========================================================================
        Node(
            package='cartographer_ros',
            executable='cartographer_node',
            name='cartographer_node',
            output='screen',
            parameters=[{'use_sim_time': False}],
            arguments=['-configuration_directory', configuration_directory,
                       '-configuration_basename', configuration_basename],
            remappings=[
                ('scan', '/scan'),          # 订阅激光话题
                ('imu', '/imu/data'),       # 订阅 IMU 话题
                ('odom', '/odom')           # 订阅里程计话题 (若 lua 中 use_odometry=true)
            ]
        ),

        # ========================================================================
        # 4. 启动地图栅格化节点
        # ========================================================================
        Node(
            package='cartographer_ros',
            executable='cartographer_occupancy_grid_node',
            name='occupancy_grid_node',
            output='screen',
            parameters=[{'use_sim_time': False}],
            arguments=['-resolution', '0.05', '-publish_period_sec', '1.0']
        )
    ])