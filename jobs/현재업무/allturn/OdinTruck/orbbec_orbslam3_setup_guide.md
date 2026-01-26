# Orbbec Astro Pro + ORB-SLAM3 연동 가이드

Ubuntu + ROS2 환경에서 Orbbec Astro Pro 카메라를 테스트하고 ORB-SLAM3와 연동하는 전체 과정입니다.

---

## 1. 시스템 요구사항

- **OS**: Ubuntu 22.04 (ROS2 Humble) 또는 Ubuntu 24.04 (ROS2 Iron/Jazzy)
- **카메라**: Orbbec Astro Pro (또는 Astro Pro Plus)
- **의존성**: OpenCV 4.x, Eigen3, Pangolin, g2o

---

## 2. Orbbec SDK 설치

### 2.1 udev 규칙 설정 (카메라 인식)

```bash
# Orbbec udev 규칙 다운로드 및 설치
cd /tmp
wget https://raw.githubusercontent.com/orbbec/OrbbecSDK/main/scripts/99-obsensor-libusb.rules
sudo cp 99-obsensor-libusb.rules /etc/udev/rules.d/
sudo udevadm control --reload-rules && sudo udevadm trigger
```

### 2.2 OrbbecSDK 설치

```bash
# 의존성 설치
sudo apt update
sudo apt install -y libusb-1.0-0-dev libudev-dev cmake build-essential

# OrbbecSDK 클론 및 빌드
cd ~/
git clone https://github.com/orbbec/OrbbecSDK.git
cd OrbbecSDK
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install
```

### 2.3 카메라 연결 테스트

```bash
# 카메라 연결 후 USB 장치 확인
lsusb | grep -i orbbec
# 예상 출력: Bus 00x Device 00x: ID 2bc5:xxxx Orbbec

# SDK 예제로 테스트
cd ~/OrbbecSDK/build/bin
./DepthViewer
```

---

## 3. ROS2 Orbbec 패키지 설치

### 3.1 orbbec_camera ROS2 패키지

```bash
# ROS2 워크스페이스 생성
mkdir -p ~/ros2_ws/src
cd ~/ros2_ws/src

# orbbec_camera 패키지 클론
git clone https://github.com/orbbec/OrbbecSDK_ROS2.git

# 의존성 설치
cd ~/ros2_ws
rosdep install --from-paths src --ignore-src -r -y

# 빌드
colcon build --symlink-install
source install/setup.bash
```

### 3.2 카메라 실행 및 테스트

```bash
# Astro Pro 실행
ros2 launch orbbec_camera astra.launch.py

# 다른 터미널에서 토픽 확인
ros2 topic list | grep -E "color|depth|camera_info"

# 예상 토픽:
# /camera/color/image_raw
# /camera/color/camera_info
# /camera/depth/image_raw
# /camera/depth/camera_info
# /camera/depth/points  (포인트클라우드)
```

### 3.3 rviz2로 시각화

```bash
# rviz2 실행
rviz2

# 추가할 디스플레이:
# - Image: /camera/color/image_raw
# - Image: /camera/depth/image_raw
# - PointCloud2: /camera/depth/points
```

---

## 4. ORB-SLAM3 설치

### 4.1 의존성 설치

```bash
sudo apt install -y \
    libopencv-dev \
    libeigen3-dev \
    libglew-dev \
    libboost-all-dev \
    libssl-dev \
    cmake \
    build-essential
```

### 4.2 Pangolin 설치 (시각화 라이브러리)

```bash
cd ~/
git clone --recursive https://github.com/stevenlovegrove/Pangolin.git
cd Pangolin
mkdir build && cd build
cmake ..
make -j$(nproc)
sudo make install
```

### 4.3 ORB-SLAM3 빌드

```bash
cd ~/
git clone https://github.com/UZ-SLAMLab/ORB_SLAM3.git
cd ORB_SLAM3

# Vocabulary 압축 해제
cd Vocabulary
tar -xf ORBvoc.txt.tar.gz
cd ..

# 빌드 스크립트 실행
chmod +x build.sh
./build.sh
```

---

## 5. Orbbec 카메라 캘리브레이션 파일 생성

ORB-SLAM3는 카메라 내부 파라미터가 필요합니다.

### 5.1 카메라 정보 확인

```bash
# ROS2 카메라 실행 후
ros2 topic echo /camera/color/camera_info --once
ros2 topic echo /camera/depth/camera_info --once
```

### 5.2 ORB-SLAM3 설정 파일 (orbbec_astro.yaml)

```yaml
%YAML:1.0

#--------------------------------------------------------------------------------------------
# Camera Parameters (Orbbec Astro Pro)
#--------------------------------------------------------------------------------------------
Camera.type: "PinHole"

# 카메라 해상도
Camera.width: 640
Camera.height: 480

# RGB 카메라 내부 파라미터 (camera_info에서 확인)
Camera.fx: 554.254
Camera.fy: 554.254
Camera.cx: 320.5
Camera.cy: 240.5

# 왜곡 계수 (일반적으로 Orbbec은 0에 가까움)
Camera.k1: 0.0
Camera.k2: 0.0
Camera.p1: 0.0
Camera.p2: 0.0

# RGB-D 모드 설정
Camera.RGB: 1
DepthMapFactor: 1000.0  # 깊이값 스케일 (mm -> m)

# 프레임레이트
Camera.fps: 30

#--------------------------------------------------------------------------------------------
# ORB Parameters
#--------------------------------------------------------------------------------------------
ORBextractor.nFeatures: 1000
ORBextractor.scaleFactor: 1.2
ORBextractor.nLevels: 8
ORBextractor.iniThFAST: 20
ORBextractor.minThFAST: 7

#--------------------------------------------------------------------------------------------
# Viewer Parameters
#--------------------------------------------------------------------------------------------
Viewer.KeyFrameSize: 0.05
Viewer.KeyFrameLineWidth: 1.0
Viewer.GraphLineWidth: 0.9
Viewer.PointSize: 2.0
Viewer.CameraSize: 0.08
Viewer.CameraLineWidth: 3.0
Viewer.ViewpointX: 0.0
Viewer.ViewpointY: -0.7
Viewer.ViewpointZ: -1.8
Viewer.ViewpointF: 500.0
```

---

## 6. ORB-SLAM3 + Orbbec 연동 (ROS2)

### 6.1 ROS2 래퍼 설치

```bash
cd ~/ros2_ws/src

# ORB-SLAM3 ROS2 래퍼 클론
git clone https://github.com/zang09/ORB_SLAM3_ROS2.git

# ORB_SLAM3 경로 설정
export ORB_SLAM3_ROOT_DIR=~/ORB_SLAM3

# 빌드
cd ~/ros2_ws
colcon build --packages-select orbslam3_ros2
source install/setup.bash
```

### 6.2 실행

**터미널 1: Orbbec 카메라**
```bash
source ~/ros2_ws/install/setup.bash
ros2 launch orbbec_camera astra.launch.py
```

**터미널 2: ORB-SLAM3 RGB-D 모드**
```bash
source ~/ros2_ws/install/setup.bash
ros2 run orbslam3_ros2 rgbd \
    ~/ORB_SLAM3/Vocabulary/ORBvoc.txt \
    ~/ros2_ws/src/ORB_SLAM3_ROS2/config/orbbec_astro.yaml
```

---

## 7. 토픽 리매핑 (필요시)

Orbbec 토픽과 ORB-SLAM3 입력 토픽이 다를 경우:

```bash
ros2 run orbslam3_ros2 rgbd \
    ~/ORB_SLAM3/Vocabulary/ORBvoc.txt \
    ~/ros2_ws/src/ORB_SLAM3_ROS2/config/orbbec_astro.yaml \
    --ros-args \
    -r /camera/rgb:=/camera/color/image_raw \
    -r /camera/depth:=/camera/depth/image_raw
```

---

## 8. 트러블슈팅

### 카메라 인식 안됨
```bash
# USB 권한 확인
ls -la /dev/bus/usb/*/*
# udev 규칙 재적용
sudo udevadm control --reload-rules && sudo udevadm trigger
# 카메라 재연결
```

### Depth 이미지 노이즈
```bash
# launch 파일에서 필터 활성화
ros2 launch orbbec_camera astra.launch.py enable_depth_filter:=true
```

### ORB-SLAM3 초기화 실패
- 특징점이 부족한 환경 (흰 벽 등) 피하기
- 카메라를 천천히 이동
- `ORBextractor.nFeatures` 값 증가

### 깊이-컬러 정합 불량
```bash
# depth_to_color 정합 활성화
ros2 launch orbbec_camera astra.launch.py align_depth:=true
```

---

## 9. 성능 최적화 팁

1. **해상도 조정**: 640x480이 실시간 처리에 적합
2. **프레임레이트**: 30fps 권장 (CPU 부하 고려)
3. **특징점 수**: 환경에 따라 500-2000 조정
4. **GPU 가속**: CUDA 지원 OpenCV로 빌드시 성능 향상

---

## 10. 추가 리소스

- [Orbbec SDK GitHub](https://github.com/orbbec/OrbbecSDK)
- [OrbbecSDK ROS2](https://github.com/orbbec/OrbbecSDK_ROS2)
- [ORB-SLAM3 공식](https://github.com/UZ-SLAMLab/ORB_SLAM3)
- [ORB-SLAM3 ROS2 래퍼](https://github.com/zang09/ORB_SLAM3_ROS2)
