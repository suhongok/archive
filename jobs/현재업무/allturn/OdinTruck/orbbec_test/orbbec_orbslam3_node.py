#!/usr/bin/env python3
"""
Orbbec Astro Pro + ORB-SLAM3 연동 ROS2 노드

이 노드는 Orbbec 카메라에서 RGB-D 이미지를 받아
ORB-SLAM3가 필요로 하는 형식으로 퍼블리시합니다.

의존성:
    pip install pyorbbecsdk opencv-python numpy --break-system-packages

실행:
    ros2 run your_package orbbec_orbslam3_node.py
"""

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge
import cv2
import numpy as np
import threading
import time

try:
    from pyorbbecsdk import *
except ImportError:
    print("Error: pyorbbecsdk 설치 필요")
    print("pip install pyorbbecsdk --break-system-packages")
    exit(1)


class OrbbecORBSLAM3Node(Node):
    """Orbbec 카메라를 ORB-SLAM3와 연동하는 ROS2 노드"""

    def __init__(self):
        super().__init__('orbbec_orbslam3_node')

        # 파라미터 선언
        self.declare_parameter('width', 640)
        self.declare_parameter('height', 480)
        self.declare_parameter('fps', 30)
        self.declare_parameter('align_depth', True)
        self.declare_parameter('publish_pointcloud', False)

        # 파라미터 읽기
        self.width = self.get_parameter('width').value
        self.height = self.get_parameter('height').value
        self.fps = self.get_parameter('fps').value
        self.align_depth = self.get_parameter('align_depth').value

        # Publisher 설정
        self.color_pub = self.create_publisher(Image, '/camera/rgb/image_raw', 10)
        self.depth_pub = self.create_publisher(Image, '/camera/depth/image_raw', 10)
        self.color_info_pub = self.create_publisher(CameraInfo, '/camera/rgb/camera_info', 10)
        self.depth_info_pub = self.create_publisher(CameraInfo, '/camera/depth/camera_info', 10)

        self.bridge = CvBridge()
        self.camera_param = None

        # 카메라 초기화
        self.pipeline = None
        self.config = None
        self.running = False

        if self.initialize_camera():
            self.get_logger().info("Orbbec 카메라 초기화 완료")
            self.running = True
            self.capture_thread = threading.Thread(target=self.capture_loop)
            self.capture_thread.start()
        else:
            self.get_logger().error("카메라 초기화 실패")

    def initialize_camera(self):
        """카메라 및 파이프라인 초기화"""
        try:
            ctx = Context()
            device_list = ctx.query_devices()

            if device_list.get_count() == 0:
                self.get_logger().error("Orbbec 카메라를 찾을 수 없습니다")
                return False

            device = device_list.get_device(0)
            device_info = device.get_device_info()
            self.get_logger().info(f"카메라 연결: {device_info.get_name()}")

            self.pipeline = Pipeline(device)
            self.config = Config()

            # 컬러 스트림 설정
            color_profiles = self.pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            color_profile = self.find_profile(color_profiles, self.width, self.height, self.fps)
            if color_profile:
                self.config.enable_stream(color_profile)
                self.get_logger().info(
                    f"컬러: {color_profile.get_width()}x{color_profile.get_height()}@{color_profile.get_fps()}fps"
                )

            # 깊이 스트림 설정
            depth_profiles = self.pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            depth_profile = self.find_profile(depth_profiles, self.width, self.height)
            if depth_profile:
                self.config.enable_stream(depth_profile)
                self.get_logger().info(
                    f"깊이: {depth_profile.get_width()}x{depth_profile.get_height()}@{depth_profile.get_fps()}fps"
                )

            # 깊이-컬러 정합 활성화
            if self.align_depth:
                self.config.set_align_mode(OBAlignMode.SW_MODE)
                self.get_logger().info("깊이-컬러 정합 활성화됨")

            # 파이프라인 시작
            self.pipeline.start(self.config)

            # 카메라 파라미터 저장
            self.camera_param = self.pipeline.get_camera_param()

            return True

        except Exception as e:
            self.get_logger().error(f"초기화 오류: {e}")
            return False

    def find_profile(self, profile_list, width, height, fps=None):
        """원하는 해상도의 프로파일 찾기"""
        for i in range(profile_list.get_count()):
            profile = profile_list.get_video_stream_profile(i)
            if profile.get_width() == width and profile.get_height() == height:
                if fps is None or profile.get_fps() == fps:
                    return profile
        # 정확한 매칭 없으면 첫 번째 프로파일 반환
        return profile_list.get_video_stream_profile(0) if profile_list.get_count() > 0 else None

    def create_camera_info(self, intrinsic, is_depth=False):
        """CameraInfo 메시지 생성"""
        info = CameraInfo()
        info.header.frame_id = "camera_depth_optical_frame" if is_depth else "camera_color_optical_frame"
        info.width = intrinsic.width
        info.height = intrinsic.height

        # 내부 파라미터 행렬 K
        info.k = [
            intrinsic.fx, 0.0, intrinsic.cx,
            0.0, intrinsic.fy, intrinsic.cy,
            0.0, 0.0, 1.0
        ]

        # 왜곡 계수 D
        info.d = [0.0, 0.0, 0.0, 0.0, 0.0]  # Orbbec은 보통 왜곡 보정됨

        # 투영 행렬 P
        info.p = [
            intrinsic.fx, 0.0, intrinsic.cx, 0.0,
            0.0, intrinsic.fy, intrinsic.cy, 0.0,
            0.0, 0.0, 1.0, 0.0
        ]

        # 회전 행렬 R (단위 행렬)
        info.r = [1.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 1.0]

        info.distortion_model = "plumb_bob"

        return info

    def capture_loop(self):
        """프레임 캡처 및 퍼블리시 루프"""
        while self.running and rclpy.ok():
            try:
                frames = self.pipeline.wait_for_frames(100)
                if frames is None:
                    continue

                now = self.get_clock().now().to_msg()

                color_frame = frames.get_color_frame()
                depth_frame = frames.get_depth_frame()

                # 컬러 이미지 퍼블리시
                if color_frame:
                    color_data = np.asanyarray(color_frame.get_data())

                    if color_frame.get_format() == OBFormat.RGB:
                        color_image = cv2.cvtColor(color_data, cv2.COLOR_RGB2BGR)
                    else:
                        color_image = color_data

                    color_msg = self.bridge.cv2_to_imgmsg(color_image, encoding="bgr8")
                    color_msg.header.stamp = now
                    color_msg.header.frame_id = "camera_color_optical_frame"
                    self.color_pub.publish(color_msg)

                    # CameraInfo 퍼블리시
                    if self.camera_param:
                        color_info = self.create_camera_info(self.camera_param.rgb_intrinsic, is_depth=False)
                        color_info.header.stamp = now
                        self.color_info_pub.publish(color_info)

                # 깊이 이미지 퍼블리시
                if depth_frame:
                    depth_data = np.asanyarray(depth_frame.get_data())

                    # 16UC1 형식으로 퍼블리시 (mm 단위)
                    depth_msg = self.bridge.cv2_to_imgmsg(depth_data.astype(np.uint16), encoding="16UC1")
                    depth_msg.header.stamp = now
                    depth_msg.header.frame_id = "camera_depth_optical_frame"
                    self.depth_pub.publish(depth_msg)

                    # CameraInfo 퍼블리시
                    if self.camera_param:
                        depth_info = self.create_camera_info(self.camera_param.depth_intrinsic, is_depth=True)
                        depth_info.header.stamp = now
                        self.depth_info_pub.publish(depth_info)

            except Exception as e:
                self.get_logger().error(f"캡처 오류: {e}")
                time.sleep(0.1)

    def destroy_node(self):
        """노드 종료 시 정리"""
        self.running = False
        if hasattr(self, 'capture_thread'):
            self.capture_thread.join(timeout=2.0)
        if self.pipeline:
            self.pipeline.stop()
        super().destroy_node()


def main(args=None):
    rclpy.init(args=args)

    node = OrbbecORBSLAM3Node()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
