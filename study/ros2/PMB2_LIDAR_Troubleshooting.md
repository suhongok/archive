# PMB2 Gazebo LIDAR 문제 해결 가이드

## 문제 상황

PMB2 로봇을 Gazebo 시뮬레이션에서 구동할 때 LIDAR 센서가 제대로 작동하지 않는 문제 발생

```bash
ros2 launch pmb2_gazebo pmb2_gazebo.launch.py is_public_sim:=True world_name:=simple_office_with_people
```

### 증상
- `/scan` 토픽: 발행되지 않음
- `/scan_raw` 토픽: `-inf` (음의 무한대) 값만 출력
- LIDAR가 월드의 객체를 감지하지 못함

---

## 근본 원인 분석

### 1. Namespace 파라미터 누락
LIDAR 플러그인이 ROS2 네임스페이스를 받지 못해서 토픽이 제대로 발행되지 않음

### 2. laserRetro 설정 비활성화
`base.gazebo.xacro`에서 robot footprint의 `laserRetro` 값이 0으로 설정
- ODE 물리 엔진이 ray casting을 무시함
- LIDAR가 물체를 감지할 수 없음

### 3. GPU Ray vs Ray 센서 호환성
`gpu_ray` 센서 타입이 ODE 물리 엔진과 호환성이 낮음
- GPU ray는 CUDA 기반 ray casting 사용
- ODE에서는 일반 ray 센서가 더 안정적

---

## 해결 방법

### 단계 1: Namespace 파라미터 추가

**파일 1: `/opt/ros/humble/share/pmb2_description/robots/pmb2.urdf.xacro`**

라인 90을 다음과 같이 수정:

```xml
<!-- 수정 전 -->
<xacro:base_sensors name="base" laser_model="${laser_model}" has_sonars="${has_sonars}" has_microphone="${has_microphone}"/>

<!-- 수정 후 -->
<xacro:base_sensors name="base" laser_model="${laser_model}" has_sonars="${has_sonars}" has_microphone="${has_microphone}" namespace="${namespace}"/>
```

명령어:
```bash
sudo sed -i 's/has_microphone="\${has_microphone}"\/>/has_microphone="${has_microphone}" namespace="${namespace}"\/>/' /opt/ros/humble/share/pmb2_description/robots/pmb2.urdf.xacro
```

**파일 2: `/opt/ros/humble/share/pmb2_description/urdf/base/base_sensors.urdf.xacro`**

라인 36을 다음과 같이 수정:

```xml
<!-- 수정 전 -->
<xacro:macro name="base_sensors" params="name laser_model:=sick-571 has_sonars:=false has_microphone:=false" >

<!-- 수정 후 -->
<xacro:macro name="base_sensors" params="name laser_model:=sick-571 has_sonars:=false has_microphone:=false namespace:="" >
```

명령어:
```bash
sudo sed -i '36s/.*/  <xacro:macro name="base_sensors" params="name laser_model:=sick-571 has_sonars:=false has_microphone:=false namespace:=\"\"" >/' /opt/ros/humble/share/pmb2_description/urdf/base/base_sensors.urdf.xacro
```

### 단계 2: LaserRetro 값 변경

**파일: `/opt/ros/humble/share/pmb2_description/urdf/base/base.gazebo.xacro`**

라인 37을 다음과 같이 수정:

```xml
<!-- 수정 전 -->
<laserRetro>0</laserRetro>

<!-- 수정 후 -->
<laserRetro>1000</laserRetro>
```

명령어:
```bash
sudo sed -i '37s/0/1000/' /opt/ros/humble/share/pmb2_description/urdf/base/base.gazebo.xacro
```

### 단계 3: GPU Ray에서 Ray 센서로 변경 ⭐ **가장 중요**

**파일: 모든 레이저 gazebo xacro 파일**

```bash
sudo sed -i 's/type="gpu_ray"/type="ray"/' /opt/ros/humble/share/pal_urdf_utils/urdf/laser/*.gazebo.xacro
```

수정되는 파일들:
- `sick_tim551_laser.gazebo.xacro`
- `sick_tim561_laser.gazebo.xacro`
- `sick_tim571_laser.gazebo.xacro`
- `hokuyo_urg_04lx_ug01_laser.gazebo.xacro`

### 단계 4: 월드 파일의 물체에도 laserRetro 설정 (선택사항)

**파일: `/opt/ros/humble/share/pal_gazebo_worlds/worlds/simple_office_with_people.world`**

```bash
sudo sed -i '/<\/visual>/a\      <laser_retro>1000</laser_retro>' /opt/ros/humble/share/pal_gazebo_worlds/worlds/simple_office_with_people.world
```

---

## 검증 방법

### 1. 시뮬레이션 시작
```bash
ros2 launch pmb2_gazebo pmb2_gazebo.launch.py is_public_sim:=True world_name:=simple_office_with_people
```

### 2. LIDAR 토픽 확인
```bash
ros2 topic list | grep scan
```

출력:
```
/scan_raw
```

### 3. LIDAR 데이터 확인
```bash
ros2 topic echo /scan_raw --once | head -50
```

정상 출력 예시:
```
ranges:
- 2.4567
- 2.4523
- 2.4521
- 2.4456
...
```

---

## 최종 결과

✅ LIDAR 센서 정상 작동
- `/scan_raw` 토픽에서 실제 거리값 발행 (0.05m ~ 25.0m)
- 월드의 벽과 물체 감지 가능
- SLAM, Navigation 등 다른 기능 사용 가능

---

## 권장: 로컬 워크스페이스 오버라이드 (재부팅 후에도 유지)

시스템 파일 수정 대신 **로컬 ROS2 워크스페이스에 수정**하는 것이 권장됩니다.

### 설정 방법

#### Step 1: 패키지 복제
```bash
cd ~/ros2_ws/src
git clone https://github.com/pal-robotics/pal_urdf_utils.git
git clone https://github.com/pal-robotics/pal_gazebo_worlds.git
```

#### Step 2: 로컬 복사본에 수정사항 적용
```bash
# pal_urdf_utils의 센서 타입 변경: gpu_lidar → gpu_ray → ray
sed -i 's/type="gpu_lidar"/type="gpu_ray"/g' \
  ~/ros2_ws/src/pal_urdf_utils/urdf/laser/*.gazebo.xacro
sed -i 's/type="gpu_ray"/type="ray"/g' \
  ~/ros2_ws/src/pal_urdf_utils/urdf/laser/*.gazebo.xacro
```

#### Step 3: Colcon Build
```bash
cd ~/ros2_ws
colcon build --packages-select pal_urdf_utils pal_gazebo_worlds \
  --symlink-install --allow-overriding pal_urdf_utils pal_gazebo_worlds
```

#### Step 4: 쉘 설정 파일에 등록
```bash
# ~/.bashrc 또는 ~/.zshrc에 추가
echo 'source ~/ros2_ws/install/setup.bash' >> ~/.bashrc
source ~/.bashrc
```

#### Step 5: 검증
```bash
# 로컬 패키지 사용 확인
ros2 pkg prefix pal_urdf_utils
# 출력 예: /home/sm/ros2_ws/install/pal_urdf_utils
```

### 장점
- ✅ **시스템 파일 보호** - 원본 파일 유지
- ✅ **재부팅 후 유지** - `~/.bashrc`에 영구 등록
- ✅ **패키지 업데이트 안전** - 시스템 업데이트 후에도 수정사항 유지
- ✅ **버전 관리 가능** - git으로 변경사항 추적
- ✅ **다중 환경 지원** - 여러 머신에서 쉽게 적용

---

## 참고: 수정된 파일 위치

| 파일 | 라인 | 변경 사항 |
|------|------|---------|
| pmb2.urdf.xacro | 90 | `namespace="${namespace}"` 추가 |
| base_sensors.urdf.xacro | 36 | `namespace:=""` 파라미터 추가 |
| base.gazebo.xacro | 37 | `laserRetro: 0 → 1000` |
| *.gazebo.xacro (laser) | - | `gpu_ray → ray` |
| simple_office_with_people.world | - | `laser_retro` 태그 추가 |

---

## 핵심 교훈

가장 중요한 해결책은 **GPU Ray 센서를 일반 Ray 센서로 변경**하는 것이었습니다.

- **GPU Ray**: CUDA 기반, Gazebo High Definition 환경에 최적화, 많은 리소스 필요
- **Ray**: CPU 기반, ODE 물리 엔진과 호환성 우수, 간단한 시뮬레이션에 적합

시뮬레이션 목적에 따라 적절한 센서 타입을 선택하는 것이 중요합니다.
