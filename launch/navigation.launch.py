import os
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # ⚠️ 务必修改为你刚保存的地图 yaml 文件的绝对路径
    map_yaml_file = '/home/wyyyz/TJ/ROS_SLAM/ylidar/my_map.yaml'
    
    # ⚠️ 务必修改为你接下来要创建的 Nav2 参数文件的绝对路径
    nav2_params_file = '/home/wyyyz/TJ/ROS_SLAM/ylidar/slam_car_cartographer/config/nav2_params.yaml'

    return LaunchDescription([
        # 1. 发布静态 TF (和建图时保持完全一致！)
        Node(
            package='tf2_ros', executable='static_transform_publisher',
            arguments=['-0.06743', '-0.03446', '0.041', '0', '0', '0', 'base_link', 'imu_link']
        ),
        Node(
            package='tf2_ros', executable='static_transform_publisher',
            arguments=['0.06', '0', '0.134', '0', '0', '3.1416', 'base_link', 'laser_frame']
        ),
        Node(
             executable='/home/wyyyz/TJ/ROS_SLAM/ylidar/slam_car_cartographer/launch/odom_to_tf.py',
             output='screen'
         ),

        # 2. 启动地图服务器 (加载你保存的地图)
        Node(
            package='nav2_map_server', executable='map_server',
            parameters=[{'yaml_filename': map_yaml_file, 'use_sim_time': False}],
            output='screen'
        ),

        # 3. 启动 AMCL 定位节点 (在地图中找自己)
        Node(
            package='nav2_amcl', executable='amcl',
            parameters=[nav2_params_file, {'use_sim_time': False}],
            output='screen'
        ),

        # 4. 启动 Nav2 导航主程序 (包含规划器、控制器、恢复器等)
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                os.path.join(get_package_share_directory('nav2_bringup'), 'launch', 'navigation_launch.py')
            ),
            launch_arguments={
                'use_sim_time': 'False',
                'params_file': nav2_params_file
            }.items()
        )
    ])
