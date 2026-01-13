# NeuronBot2 SLAM 테스트 기록

**날짜**: 2026-01-10
**환경**: Ubuntu 22.04, ROS 2 Humble
**워크스페이스**: ~/nav2_ws

## 프로젝트 개요

NeuronBot2는 Adlink에서 제작한 ROS 2 기반 모바일 로봇 플랫폼입니다. SLAM(Simultaneous Localization and Mapping), 자율 주행, Gazebo 시뮬레이션을 지원합니다.

## 초기 설정 및 문제 해결

### 1. 빌드 문제 해결

#### 문제 1: Python setuptools 경고
```
UserWarning: Usage of dash-separated 'script-dir' will not be supported in future versions.
```

**원인**: `neuronbot2_led/setup.cfg`에서 deprecated된 dash-separated 옵션 사용

**해결**:
```bash
# neuronbot2_led/setup.cfg 수정
[develop]
script_dir=$base/lib/neuronbot2_led  # script-dir → script_dir
[install]
install_scripts=$base/lib/neuronbot2_led  # install-scripts → install_scripts
```

#### 문제 2: Source 시 Python 파일을 찾을 수 없음
```
/usr/bin/python3: can't open file '/home/sm/nav2_ws/_local_setup_util_sh.py': [Errno 2] No such file or directory
```

**원인**: `.bashrc`에서 bash 환경인데 zsh용 setup 파일을 source하려고 시도

**해결**:
```bash
# ~/.bashrc 수정 (백업: ~/.bashrc.backup)
# Before: source ~/nav2_ws/install/local_setup.zsh
# After:
source ~/nav2_ws/install/local_setup.bash
```

### 2. ROS 패키지를 찾을 수 없는 문제

#### 문제: Package not found 에러
```bash
Package 'neuronbot2_gazebo' not found: "package 'neuronbot2_gazebo' not found,
searching: ['/opt/ros/humble']"
```

**원인**: `.zshrc`에 워크스페이스 환경 설정이 누락됨

**해결**:
```bash
# ~/.zshrc에 추가 (백업: ~/.zshrc.backup)
source ~/nav2_ws/install/local_setup.zsh
```

**확인 방법**:
```bash
echo $AMENT_PREFIX_PATH
# 출력에 /home/sm/nav2_ws/install 경로들이 포함되어야 함
```

### 3. 빌드 성공

```bash
# ROS 2 환경 source
source /opt/ros/humble/setup.zsh

# 전체 워크스페이스 빌드
cd ~/nav2_ws
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release

# 결과
# Summary: 10 packages finished [0.90s]
# - neuronbot2_bringup
# - neuronbot2_description
# - neuronbot2_gazebo
# - neuronbot2_slam
# - neuronbot2_nav
# - neuronbot2_led
# - rplidar_ros2
# - serial
# - openslam_gmapping
# - slam_gmapping
```

## Gazebo 시뮬레이션 실행

### 1. Gazebo 월드 실행

```bash
source ~/.zshrc  # 환경 변수 로드
ros2 launch neuronbot2_gazebo neuronbot2_world.launch.py world_model:=mememan_world.model
```

**실행 결과**:
- ✅ Gazebo 서버 시작
- ✅ Gazebo GUI 클라이언트 시작
- ✅ 로봇 상태 발행자 실행
- ✅ NeuronBot2 로봇 spawn 성공

**로그 출력**:
```
[spawn_entity.py-4] [INFO]: Spawn status: SpawnEntity: Successfully spawned entity [nb2]
[gzserver-1] [INFO]: Wheel pair 1 separation set to [0.218000m]
[gzserver-1] [INFO]: Wheel pair 1 diameter set to [0.084000m]
[gzserver-1] [INFO]: Subscribed to [/cmd_vel]
[gzserver-1] [INFO]: Advertise odometry on [/odom]
[gzserver-1] [INFO]: Publishing odom transforms between [odom] and [base_footprint]
```

### 2. 주요 토픽 확인

```bash
# 사용 가능한 토픽 목록
ros2 topic list

# 주요 토픽:
# /clock - Gazebo 시뮬레이션 시간
# /cmd_vel - 속도 명령 (로봇 제어)
# /odom - 오도메트리 데이터
# /scan - 레이저 스캔 데이터 (RPLidar)
# /tf - 좌표 변환
# /joint_states - 조인트 상태
```

### 3. 로봇 텔레옵 (키보드 제어)

**새 터미널 열기**:
```bash
source ~/.zshrc
ros2 run teleop_twist_keyboard teleop_twist_keyboard
```

**키보드 조작법**:
- `i` - 전진
- `,` - 후진
- `j` - 좌회전
- `l` - 우회전
- `k` - 정지
- `q/z` - 속도 증가/감소

## SLAM 실행

### 1. Gmapping SLAM

```bash
# 새 터미널에서
source ~/.zshrc
ros2 launch neuronbot2_slam gmapping_launch.py open_rviz:=true use_sim_time:=true
```

### 2. Slam Toolbox

```bash
ros2 launch neuronbot2_slam slam_toolbox_launch.py open_rviz:=true use_sim_time:=true
```

### 3. Cartographer

```bash
ros2 launch neuronbot2_slam cartographer_launch.py open_rviz:=true use_sim_time:=true
```

### 4. 지도 저장

로봇을 텔레옵으로 조종하여 환경을 충분히 탐색한 후:

```bash
# 지도 저장
ros2 run nav2_map_server map_saver_cli -f ~/maps/my_map

# 결과 파일:
# - my_map.yaml (지도 메타데이터)
# - my_map.pgm (지도 이미지)
```

## 네비게이션 실행

### 1. 저장된 지도로 네비게이션

```bash
# Gazebo가 실행 중인 상태에서
ros2 launch neuronbot2_nav bringup_launch.py \
  map:=$HOME/nav2_ws/src/neuronbot2/neuronbot2_nav/map/mememan.yaml \
  open_rviz:=true \
  use_sim_time:=true
```

### 2. RViz에서 로봇 위치 설정

1. **2D Pose Estimate** 클릭
2. 지도에서 로봇의 대략적인 위치와 방향 설정

### 3. 목표 지점 설정

1. **2D Nav Goal** 클릭
2. 지도의 빈 공간을 클릭하여 목표 설정
3. 로봇이 자동으로 경로를 계획하고 이동

## 워크스페이스 구조

```
~/nav2_ws/
├── src/
│   ├── neuronbot2/
│   │   ├── neuronbot2_bringup/      # 하드웨어 초기화 및 드라이버
│   │   ├── neuronbot2_description/  # URDF 로봇 모델
│   │   ├── neuronbot2_gazebo/       # Gazebo 시뮬레이션
│   │   ├── neuronbot2_slam/         # SLAM 런치 파일
│   │   ├── neuronbot2_nav/          # Nav2 네비게이션
│   │   └── neuronbot2_tools/        # LED 제어 등 유틸리티
│   ├── rplidar_ros/                 # RPLidar 센서 드라이버
│   ├── serial/                      # 시리얼 통신 라이브러리
│   └── slam_gmapping/               # Gmapping SLAM 알고리즘
├── build/
├── install/
└── log/
```

## 주요 파라미터

### Gazebo Launch 파라미터

```bash
# 월드 선택
world_model:=mememan_world.model  # mememan 또는 phenix
```

### SLAM Launch 파라미터

```bash
open_rviz:=true      # RViz 시각화 실행 (기본값: false)
use_sim_time:=true   # 시뮬레이션 시간 사용 (실제 로봇: false)
```

### Navigation Launch 파라미터

```bash
map:=<경로/map.yaml>  # 저장된 지도 파일 경로
open_rviz:=true       # RViz 실행
use_sim_time:=true    # 시뮬레이션 시간 사용
```

## 좌표 프레임

- **base_footprint** - 로봇 베이스 프레임 (지면)
- **base_link** - 로봇 중심
- **odom** - 오도메트리 프레임 (로컬 위치)
- **map** - 글로벌 맵 프레임
- **laser_frame** - 레이저 스캐너 프레임
- **imu_link** - IMU 센서 프레임

## 문제 해결 팁

### 패키지를 찾을 수 없을 때

```bash
# 환경이 제대로 source 되었는지 확인
echo $AMENT_PREFIX_PATH

# 워크스페이스 재 source
source ~/nav2_ws/install/local_setup.zsh

# 패키지 목록 확인
ros2 pkg list | grep neuronbot2
```

### Gazebo가 느릴 때

```bash
# GUI를 닫아 CPU 부하 감소 (시뮬레이션은 계속 실행됨)
# Gazebo 창의 X 버튼 클릭

# 또는 GUI 없이 실행
export GAZEBO_MASTER_URI=http://localhost:11345
gzserver <world_file>  # 서버만 실행
```

### 빌드 문제 발생 시

```bash
# 클린 빌드
cd ~/nav2_ws
rm -rf build/ install/ log/
colcon build --symlink-install --cmake-args -DCMAKE_BUILD_TYPE=Release
```

## 다음 단계

1. ✅ Gazebo 시뮬레이션 실행 완료
2. ⬜ SLAM으로 지도 작성
3. ⬜ 작성한 지도로 자율 주행 테스트
4. ⬜ 실제 NeuronBot2 하드웨어로 테스트 (하드웨어가 있을 경우)

## 참고 자료

- [NeuronBot2 GitHub](https://github.com/Adlink-ROS/neuronbot2)
- [ROS 2 Documentation](https://docs.ros.org/en/humble/)
- [Nav2 Documentation](https://navigation.ros.org/)
- [Gazebo Documentation](http://gazebosim.org/tutorials)

## 노트

- 시뮬레이션과 실제 로봇에서 `use_sim_time` 파라미터 설정을 반드시 구분해야 함
- Gazebo 초기화에는 시간이 걸릴 수 있음 (GPU에 따라 다름)
- SLAM 중에는 로봇을 천천히 움직여야 정확한 지도 생성 가능
- 지도 저장 전에 SLAM을 종료하지 말 것
