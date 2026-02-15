# Odin truck slam 개선 방안 연구

# Isaac ROS 특징 요약

NVIDIA가 개발한 ROS 2 기반 하드웨어 가속 로봇 소프트웨어 플랫폼

- **하드웨어 가속**: GPU, DLA, VPU 활용하여 로봇 연산 가속 (Jetson 플랫폼 최적화)
- **ROS 2 완전 호환**: 표준 ROS 2 인터페이스 사용, 기존 생태계와 통합 용이
- **NITROS**: 노드 간 제로카피(zero-copy) 데이터 전송으로 파이프라인 성능 향상
- **컨테이너 기반 배포**: Docker로 제공되어 환경 설정 간편
- **Sim-to-Real**: NVIDIA Isaac Sim(Omniverse)과 연동

## 주요 패키지

| 분야 | 패키지 | 설명 |
| --- | --- | --- |
| 인식 | Visual SLAM (cuVSLAM) | 시각 기반 위치 추정 |
| 인식 | DNN Inference | TensorRT 기반 딥러닝 추론 |
| 내비게이션 | Nvblox | 3D 장애물 맵핑 |
| 내비게이션 | Nav2 플러그인 | GPU 가속 내비게이션 |
| 3D 인식 | Depth Estimation (ESS) | 스테레오 깊이 추정 |

---

# LiDAR 매핑 시 Isaac ROS 효과 분석

## 결론: LiDAR 단독 매핑에는 Isaac ROS 불필요

<aside>
💡

LiDAR 전용 2D SLAM은 CPU만으로 충분히 동작하며, Isaac ROS의 GPU 가속 이점이 크지 않음

</aside>

- **2D LiDAR SLAM**: `slam_toolbox`, `cartographer` 등 기존 패키지가 CPU에서도 실시간 처리 가능
- **GPU 가속 효과 제한적**: LiDAR 스캔 매칭(ICP 등)은 GPU보다 CPU에서도 효율적
- **Isaac ROS 주력 분야**: 비전(카메라) 기반 작업 — DNN 추론, 스테레오 깊이, Visual SLAM
- **Orin Nano 제약**: 4~8GB 공유 메모리로 Nvblox 등 무거운 패키지에서 메모리 부족 가능

## Isaac ROS가 빛나는 경우

- LiDAR **+ 카메라 센서 융합** (Nvblox + Visual SLAM)
- **DNN 기반 객체 인식** 추가 시
- **3D 복셀맵** 필요 시

---

# LiDAR + 일반 카메라(RGB) SLAM 방안

## 결론: 가능하며, 센서 융합으로 단일 센서보다 강력

| 센서 | 장점 | 단점 |
| --- | --- | --- |
| LiDAR | 정확한 거리 측정, 조명 무관 | 시각 정보 부족 |
| 일반 카메라 | 풍부한 시각 정보, 저렴 | 거리 정보 없음, 조명 민감 |

## 구현 방법 비교

### 방법 1: slam_toolbox + 카메라 보조 (느슨한 결합)

```
LiDAR → slam_toolbox (2D 맵 + 위치 추정)
카메라 → 객체 인식 / 시각 보조
       → robot_localization (EKF/UKF로 융합)
```

- 난이도: 중간 / Orin Nano 적합도: 높음

### 방법 2: Isaac ROS (GPU 가속, 긴밀한 결합)

```
LiDAR + 카메라 → Nvblox (3D 맵)
              → cuVSLAM (Visual SLAM)
              → Nav2 내비게이션
```

- 난이도: 높음 / Orin Nano: 메모리 주의 (8GB 권장)

### 방법 3: RTAB-Map (최종 추천)

```
LiDAR + 카메라 → RTAB-Map → 2D/3D 맵 + 위치 추정
```

- **다중 센서 네이티브 지원**: LiDAR + RGB 카메라 직접 입력
- **루프 클로저**: 카메라 시각 특징으로 루프 감지 → 맵 보정
- **2D & 3D 맵 동시 생성**
- **CPU 기반 동작**: Orin Nano에서 무리 없이 동작
- **ROS 2 지원**: `rtabmap_ros` 패키지

## 최종 비교표

| 항목 | slam_toolbox + 카메라 | Isaac ROS | **RTAB-Map** |
| --- | --- | --- | --- |
| 난이도 | 쉬움 | 어려움 | 중간 |
| Orin Nano 호환 | 최적 | 메모리 부족 가능 | 좋음 |
| 센서 융합 | 느슨한 결합 | 긴밀한 결합 | 긴밀한 결합 |
| 루프 클로저 | 제한적 | 지원 | 카메라 기반 지원 |
| 3D 맵 | 불가 | 지원 | 지원 |
| 추천도 | ★★★ | ★★ | ★★★★★ |

---

# 최종 추천

<aside>
🎯

**Jetson Orin Nano + LiDAR + 일반 카메라 → RTAB-Map 추천**

- LiDAR로 정확한 거리/맵, 카메라로 루프 클로저 + 시각 특징 보강
- Orin Nano에서 무리 없이 동작 (CPU 기반)
- ROS 2 생태계에서 가장 성숙한 멀티센서 SLAM
- 향후 깊이 카메라로 업그레이드해도 그대로 사용 가능
- 설치: `sudo apt install ros-humble-rtabmap-ros`
</aside>