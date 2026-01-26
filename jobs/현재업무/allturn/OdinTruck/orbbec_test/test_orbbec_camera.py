#!/usr/bin/env python3
"""
Orbbec Astro Pro 카메라 테스트 스크립트
ROS2 없이 OrbbecSDK를 직접 사용하여 카메라 기능을 테스트합니다.

사용법:
    pip install pyorbbecsdk opencv-python numpy --break-system-packages
    python3 test_orbbec_camera.py
"""

import cv2
import numpy as np
import sys
import time

try:
    from pyorbbecsdk import *
except ImportError:
    print("Error: pyorbbecsdk가 설치되지 않았습니다.")
    print("설치 방법: pip install pyorbbecsdk --break-system-packages")
    sys.exit(1)


class OrbbecCameraTester:
    def __init__(self):
        self.pipeline = None
        self.config = None
        self.device = None

    def initialize(self):
        """카메라 초기화"""
        print("=" * 50)
        print("Orbbec Astro Pro 카메라 테스트")
        print("=" * 50)

        # Context 생성 및 디바이스 검색
        ctx = Context()
        device_list = ctx.query_devices()

        if device_list.get_count() == 0:
            print("❌ 연결된 Orbbec 카메라가 없습니다.")
            print("\n확인사항:")
            print("  1. 카메라가 USB에 연결되어 있는지 확인")
            print("  2. lsusb | grep -i orbbec 명령으로 확인")
            print("  3. udev 규칙이 설치되어 있는지 확인")
            return False

        # 첫 번째 디바이스 선택
        self.device = device_list.get_device(0)
        device_info = self.device.get_device_info()

        print(f"\n✅ 카메라 발견!")
        print(f"  - 이름: {device_info.get_name()}")
        print(f"  - 시리얼: {device_info.get_serial_number()}")
        print(f"  - 펌웨어: {device_info.get_firmware_version()}")

        # 파이프라인 및 설정
        self.pipeline = Pipeline(self.device)
        self.config = Config()

        return True

    def test_color_stream(self):
        """컬러 스트림 테스트"""
        print("\n[테스트 1] 컬러 스트림")
        print("-" * 30)

        try:
            # 컬러 스트림 프로파일 검색
            profile_list = self.pipeline.get_stream_profile_list(OBSensorType.COLOR_SENSOR)
            if profile_list.get_count() == 0:
                print("❌ 컬러 센서를 찾을 수 없습니다.")
                return False

            # 640x480 @ 30fps 프로파일 찾기
            color_profile = None
            for i in range(profile_list.get_count()):
                profile = profile_list.get_video_stream_profile(i)
                if (profile.get_width() == 640 and
                    profile.get_height() == 480 and
                    profile.get_fps() == 30):
                    color_profile = profile
                    break

            if color_profile is None:
                color_profile = profile_list.get_video_stream_profile(0)

            print(f"  해상도: {color_profile.get_width()}x{color_profile.get_height()}")
            print(f"  FPS: {color_profile.get_fps()}")
            print(f"  포맷: {color_profile.get_format()}")

            self.config.enable_stream(color_profile)
            print("✅ 컬러 스트림 설정 완료")
            return True

        except Exception as e:
            print(f"❌ 컬러 스트림 설정 실패: {e}")
            return False

    def test_depth_stream(self):
        """깊이 스트림 테스트"""
        print("\n[테스트 2] 깊이 스트림")
        print("-" * 30)

        try:
            profile_list = self.pipeline.get_stream_profile_list(OBSensorType.DEPTH_SENSOR)
            if profile_list.get_count() == 0:
                print("❌ 깊이 센서를 찾을 수 없습니다.")
                return False

            # 640x480 프로파일 찾기
            depth_profile = None
            for i in range(profile_list.get_count()):
                profile = profile_list.get_video_stream_profile(i)
                if (profile.get_width() == 640 and
                    profile.get_height() == 480):
                    depth_profile = profile
                    break

            if depth_profile is None:
                depth_profile = profile_list.get_video_stream_profile(0)

            print(f"  해상도: {depth_profile.get_width()}x{depth_profile.get_height()}")
            print(f"  FPS: {depth_profile.get_fps()}")
            print(f"  포맷: {depth_profile.get_format()}")

            self.config.enable_stream(depth_profile)
            print("✅ 깊이 스트림 설정 완료")
            return True

        except Exception as e:
            print(f"❌ 깊이 스트림 설정 실패: {e}")
            return False

    def test_ir_stream(self):
        """IR 스트림 테스트"""
        print("\n[테스트 3] IR 스트림")
        print("-" * 30)

        try:
            profile_list = self.pipeline.get_stream_profile_list(OBSensorType.IR_SENSOR)
            if profile_list.get_count() == 0:
                print("⚠️ IR 센서를 찾을 수 없습니다 (일부 모델에서 지원 안함).")
                return False

            ir_profile = profile_list.get_video_stream_profile(0)
            print(f"  해상도: {ir_profile.get_width()}x{ir_profile.get_height()}")
            print(f"  FPS: {ir_profile.get_fps()}")
            print("✅ IR 스트림 사용 가능")
            return True

        except Exception as e:
            print(f"⚠️ IR 스트림 미지원: {e}")
            return False

    def get_camera_intrinsics(self):
        """카메라 내부 파라미터 조회"""
        print("\n[테스트 4] 카메라 내부 파라미터")
        print("-" * 30)

        try:
            # 카메라 파라미터 가져오기
            camera_param = self.pipeline.get_camera_param()

            # 컬러 카메라 내부 파라미터
            color_intrinsic = camera_param.rgb_intrinsic
            print("\n  [컬러 카메라 내부 파라미터]")
            print(f"    fx: {color_intrinsic.fx:.3f}")
            print(f"    fy: {color_intrinsic.fy:.3f}")
            print(f"    cx: {color_intrinsic.cx:.3f}")
            print(f"    cy: {color_intrinsic.cy:.3f}")
            print(f"    해상도: {color_intrinsic.width}x{color_intrinsic.height}")

            # 깊이 카메라 내부 파라미터
            depth_intrinsic = camera_param.depth_intrinsic
            print("\n  [깊이 카메라 내부 파라미터]")
            print(f"    fx: {depth_intrinsic.fx:.3f}")
            print(f"    fy: {depth_intrinsic.fy:.3f}")
            print(f"    cx: {depth_intrinsic.cx:.3f}")
            print(f"    cy: {depth_intrinsic.cy:.3f}")
            print(f"    해상도: {depth_intrinsic.width}x{depth_intrinsic.height}")

            print("\n✅ 카메라 파라미터 조회 완료")
            print("\n  💡 이 값들을 ORB-SLAM3 설정 파일에 사용하세요!")

            return camera_param

        except Exception as e:
            print(f"❌ 카메라 파라미터 조회 실패: {e}")
            return None

    def run_live_preview(self, duration=10):
        """실시간 미리보기"""
        print(f"\n[테스트 5] 실시간 미리보기 ({duration}초)")
        print("-" * 30)
        print("  'q' 키를 눌러 종료")

        try:
            self.pipeline.start(self.config)
            print("✅ 파이프라인 시작됨")

            start_time = time.time()
            frame_count = 0

            while True:
                # 타임아웃 확인
                if time.time() - start_time > duration:
                    print(f"\n  {duration}초 경과, 테스트 종료")
                    break

                # 프레임 가져오기
                frames = self.pipeline.wait_for_frames(100)
                if frames is None:
                    continue

                color_frame = frames.get_color_frame()
                depth_frame = frames.get_depth_frame()

                # 컬러 이미지 변환
                if color_frame:
                    color_data = np.asanyarray(color_frame.get_data())
                    if color_frame.get_format() == OBFormat.RGB:
                        color_image = cv2.cvtColor(color_data, cv2.COLOR_RGB2BGR)
                    else:
                        color_image = color_data

                    cv2.imshow("Color", color_image)

                # 깊이 이미지 변환 및 시각화
                if depth_frame:
                    depth_data = np.asanyarray(depth_frame.get_data())
                    depth_colormap = cv2.applyColorMap(
                        cv2.convertScaleAbs(depth_data, alpha=0.03),
                        cv2.COLORMAP_JET
                    )
                    cv2.imshow("Depth", depth_colormap)

                frame_count += 1

                # 키 입력 확인
                if cv2.waitKey(1) & 0xFF == ord('q'):
                    print("\n  사용자 종료 요청")
                    break

            elapsed = time.time() - start_time
            print(f"\n  총 프레임: {frame_count}")
            print(f"  평균 FPS: {frame_count/elapsed:.1f}")

            self.pipeline.stop()
            cv2.destroyAllWindows()
            print("✅ 실시간 미리보기 완료")
            return True

        except Exception as e:
            print(f"❌ 미리보기 실패: {e}")
            return False

    def cleanup(self):
        """리소스 정리"""
        if self.pipeline:
            try:
                self.pipeline.stop()
            except:
                pass
        cv2.destroyAllWindows()


def main():
    tester = OrbbecCameraTester()

    try:
        # 1. 초기화
        if not tester.initialize():
            return 1

        # 2. 스트림 테스트
        tester.test_color_stream()
        tester.test_depth_stream()
        tester.test_ir_stream()

        # 3. 카메라 파라미터
        tester.get_camera_intrinsics()

        # 4. 실시간 미리보기 (옵션)
        print("\n" + "=" * 50)
        response = input("실시간 미리보기를 실행하시겠습니까? (y/n): ")
        if response.lower() == 'y':
            tester.run_live_preview(duration=30)

        print("\n" + "=" * 50)
        print("✅ 모든 테스트 완료!")
        print("=" * 50)
        return 0

    except KeyboardInterrupt:
        print("\n\n테스트 중단됨")
        return 1
    finally:
        tester.cleanup()


if __name__ == "__main__":
    sys.exit(main())
