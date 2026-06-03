include "map_builder.lua"
include "trajectory_builder.lua"

options = {
  map_builder = MAP_BUILDER,
  trajectory_builder = TRAJECTORY_BUILDER,
  map_frame = "map",
  tracking_frame = "imu_link",       -- 追踪坐标系设为 IMU，因为我们要融合它
  published_frame = "base_link",     -- 发布出的坐标系
  odom_frame = "odom",               -- 里程计坐标系（算法会自己推算发布）
  provide_odom_frame = true,         
  publish_frame_projected_to_2d = true,
  use_odometry = false,              
  use_nav_sat = false,
  use_landmarks = false,
  num_laser_scans = 1,               -- 1个激光雷达
  num_multi_echo_laser_scans = 0,
  num_subdivisions_per_laser_scan = 1,
  num_point_clouds = 0,
  lookup_transform_timeout_sec = 0.2,
  submap_publish_period_sec = 0.3,
  pose_publish_period_sec = 5e-3,
  trajectory_publish_period_sec = 30e-3,
  rangefinder_sampling_ratio = 1.,
  odometry_sampling_ratio = 0.001,
  fixed_frame_pose_sampling_ratio = 1.,
  imu_sampling_ratio = 1.,           -- 使用 IMU 数据
  landmarks_sampling_ratio = 1.,
}

-- ✅ 明确指定使用 2D 建图模式
MAP_BUILDER.use_trajectory_builder_2d = true

-- ✅ 2D 建图专用参数
TRAJECTORY_BUILDER_2D.use_imu_data = true       
TRAJECTORY_BUILDER_2D.min_range = 0.1
TRAJECTORY_BUILDER_2D.max_range = 16.0
TRAJECTORY_BUILDER_2D.missing_data_ray_length = 3.0

-- 对于无里程计的小车，开启实时相关性扫描匹配非常重要，防止丢位置
TRAJECTORY_BUILDER_2D.use_online_correlative_scan_matching = true

-- IMU 重力时间常数（帮助算法忽略短暂的重力抖动干扰）
TRAJECTORY_BUILDER_2D.imu_gravity_time_constant = 5.0

return options
