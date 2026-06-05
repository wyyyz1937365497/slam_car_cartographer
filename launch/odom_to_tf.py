#!/usr/bin/env python3
   
import rclpy
from rclpy.node import Node
from nav_msgs.msg import Odometry
from geometry_msgs.msg import TransformStamped
from tf2_ros import TransformBroadcaster

class OdomToTF(Node):
    def __init__(self):
        super().__init__('odom_to_tf_node')
        # 创建 TF 广播器
        self.tf_broadcaster = TransformBroadcaster(self)
        # 订阅 ESP32 发来的 /odom 话题
        self.subscription = self.create_subscription(
            Odometry,
            '/odom',
            self.odom_callback,
            10)

    def odom_callback(self, msg):
        # 构建 TF 消息
        t = TransformStamped()
        
        # 设置时间戳和坐标系
        t.header.stamp = msg.header.stamp
        t.header.frame_id = 'odom'
        t.child_frame_id = 'base_link'
        
        # 从 /odom 话题中提取平移信息
        t.transform.translation.x = msg.pose.pose.position.x
        t.transform.translation.y = msg.pose.pose.position.y
        t.transform.translation.z = 0.0
        
        # 从 /odom 话题中提取旋转信息 (四元数)
        t.transform.rotation = msg.pose.pose.orientation
        
        # 广播 TF
        self.tf_broadcaster.sendTransform(t)

def main(args=None):
    rclpy.init(args=args)
    node = OdomToTF()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
