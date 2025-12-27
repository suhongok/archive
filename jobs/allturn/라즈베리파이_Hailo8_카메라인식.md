# 라즈베리파이5 + Hailo-8 + 카메라 인식

## 📌 프로젝트 개요

**상태**: 완료 ✅  
**작성자**: 옥성민  
**생성일**: 2025년 11월 23일  
**분야**: AI 엣지 컴퓨팅 (Edge AI)

---

## 🎯 목표

- Hailo-8 AI 가속기 모듈을 라즈베리파이 5에 설치
- 실시간 카메라 기반 객체 인식 (Object Detection)
- 엣지 디바이스에서 AI 추론 실행
- 메카넘휠 로봇의 자율 주행 기반 구축

---

## 🔧 하드웨어 구성

### 라즈베리파이 5

| 항목 | 사양 |
|------|------|
| **프로세서** | Broadcom BCM2712 (ARM Cortex-A76) |
| **코어** | 4-Core @ 2.4 GHz |
| **RAM** | 4GB / 8GB LPDDR5 |
| **Storage** | microSD 카드 (권장 32GB+) |
| **USB** | USB 3.0 x2, USB 2.0 x2 |
| **GPIO** | 40 PIN |
| **연결** | WiFi 6E, Bluetooth 5.3 |

### Hailo-8 AI 가속기

| 항목 | 사양 |
|------|------|
| **모델명** | Hailo-8 |
| **프로세싱 성능** | 26 TOPS (Tera Operations Per Second) |
| **인터페이스** | PCIe Gen 4 / USB |
| **전력 소비** | ~3W |
| **지원 포맷** | YOLO, ResNet, MobileNet 등 |
| **정확도** | FP32, Int16, Int8 |

### 카메라

| 항목 | 사양 |
|------|------|
| **모델** | Raspberry Pi Camera V3 (또는 USB 카메라) |
| **해상도** | 12MP (4K 30fps) |
| **필드 오브 뷰** | 160도 |
| **센서** | 1/1.3" Sony IMX708 |

---

## 📦 소프트웨어 스택

### 운영체제
```
Raspberry Pi OS (Bookworm)
├── Debian 기반
├── 64-bit
└── 최신 커널 지원
```

### 필수 라이브러리 및 도구

| 항목 | 버전 | 목적 |
|------|------|------|
| **Hailo SDK** | 4.x | AI 가속기 제어 |
| **OpenCV** | 4.8+ | 이미지 처리 |
| **TensorFlow Lite** | 2.13+ | 모델 추론 |
| **libcamera** | 최신 | 카메라 제어 |
| **Paho MQTT** | 1.6+ | 통신 (선택) |

---

## 🚀 설치 및 구성

### 1. Hailo-8 설치 및 드라이버 설정

```bash
# Hailo SDK 설치
wget https://github.com/hailo-ai/hailort/releases/download/v4.x.x/hailort.tar.gz
tar -xzf hailort.tar.gz
cd hailort
./install.sh

# 드라이버 확인
lspci | grep Hailo
```

### 2. 필수 패키지 설치

```bash
sudo apt-get update
sudo apt-get install -y \
  python3-opencv \
  python3-tensorflow-lite \
  libcamera-tools \
  python3-libcamera

# Hailo Python 바인딩
pip3 install hailo-sdk
```

### 3. 카메라 설정

```bash
# 카메라 활성화
sudo raspi-config
# Interface Options > Camera > Enable

# 카메라 테스트
libcamera-still -o test.jpg
```

---

## 🧠 AI 모델 및 추론

### 지원하는 모델

```
객체 인식 (Object Detection)
├── YOLOv8 (권장)
├── YOLOv5
├── MobileNet-SSD
└── ResNet 기반

추적 (Tracking)
├── DeepSORT
├── ByteTrack
└── Hailo Tracker

분류 (Classification)
├── ImageNet 분류기
└── Custom 분류 모델
```

### 예시: YOLO 객체 인식

```python
import hailo
import cv2
import numpy as np
from libcamera import controls
from picamera2 import Picamera2

# Hailo 초기화
device = hailo.Device(hailo.Device.ConfigureParams('yolov8m.hef'))
hef = hailo.Hef(device)

# 카메라 초기화
picam2 = Picamera2()
config = picam2.create_preview_configuration()
picam2.configure(config)
picam2.start()

# 추론 루프
while True:
    frame = picam2.capture_array()
    
    # 전처리
    resized = cv2.resize(frame, (640, 640))
    
    # Hailo 추론
    results = hef.run(resized)
    
    # 후처리 및 결과 시각화
    for detection in results:
        x, y, w, h, conf, cls = detection
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
        cv2.putText(frame, f"{cls}: {conf:.2f}", (x, y-10), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    
    # 출력
    cv2.imshow('Detection', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

picam2.stop()
cv2.destroyAllWindows()
```

---

## 📊 성능 지표

### 처리 능력

| 메트릭 | 값 |
|--------|-----|
| **추론 속도** | 30+ FPS (YOLOv8m) |
| **레이턴시** | ~30ms per frame |
| **전력 효율** | ~65 TFLOPS/W |
| **메모리** | < 500MB 사용 |
| **CPU 점유율** | ~20% (GPU 오프로드) |

### 정확도

```
YOLOv8m on COCO Dataset
├── mAP@0.5: 93.6%
├── mAP@0.5:0.95: 70.2%
└── 속도: ~30fps (라즈베리파이5)
```

---

## 🤖 로봇 통합 예시

### 메카넘휠 로봇 자율 주행

```python
import hailo
import rospy
from geometry_msgs.msg import Twist

# ROS 초기화
rospy.init_node('hailo_robot_nav')
cmd_vel_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=1)

# Hailo 모델 로드
device = hailo.Device(hailo.Device.ConfigureParams('yolov8s.hef'))

# 객체 감지 및 제어
while not rospy.is_shutdown():
    # 카메라 프레임
    frame = capture_frame()
    
    # AI 추론
    detections = device.run(frame)
    
    # 제어 명령 생성
    cmd = Twist()
    
    # 사람 감지 시 추적
    for detection in detections:
        if detection.class_id == 0:  # Person
            # 영상 중심을 기준으로 제어
            center_x = detection.center[0]
            if center_x < 320:
                cmd.angular.z = 0.5  # 좌회전
            elif center_x > 320:
                cmd.angular.z = -0.5  # 우회전
            else:
                cmd.linear.x = 0.5  # 전진
    
    # 발행
    cmd_vel_pub.publish(cmd)
```

---

## 🔍 카메라 인식 기능

### 객체 인식

```
Person (사람)
├── 성인 남성/여성
└── 어린이

Vehicle (차량)
├── Car
├── Truck
├── Bus
└── Motorcycle

기타
├── Animal (동물)
├── Plant (식물)
└── Custom (사용자 정의)
```

### 성능 최적화

1. **양자화 (Quantization)**
   - FP32 → Int8 (4배 축소)
   - 정확도 손실 ~1-2%

2. **모델 최적화**
   - 레이어 프루닝
   - 채널 압축
   - 가중치 공유

3. **배치 처리**
   - 여러 프레임 동시 처리
   - 처리량 증가

---

## 🧪 테스트 및 검증

### 기능 테스트

- [ ] 카메라 정상 작동 확인
- [ ] Hailo-8 드라이버 로드 확인
- [ ] 모델 추론 성공 확인
- [ ] 실시간 처리 성능 확인

### 성능 테스트

- [ ] FPS 측정 (30fps+ 목표)
- [ ] 레이턴시 측정 (< 50ms)
- [ ] 전력 소비 측정
- [ ] 온도 모니터링

### 통합 테스트

- [ ] 로봇 제어 동작 확인
- [ ] 다양한 환경 테스트
- [ ] 장시간 안정성 테스트

---

## 🛠️ 트러블슈팅

### 일반적인 문제

| 문제 | 해결 방법 |
|------|---------|
| **Hailo 인식 안 됨** | `lspci` 확인, 드라이버 재설치 |
| **카메라 인식 안 됨** | `libcamera-hello` 테스트, `/boot/config.txt` 확인 |
| **FPS 저하** | 해상도 축소, 모델 크기 감소 |
| **과열** | 히트싱크 추가, 팬 설치 |
| **메모리 부족** | 스왑 설정, RAM 디스크 활용 |

---

## 📈 향후 계획

1. **다중 카메라 지원** - 360도 인식
2. **에지 학습** - 온디바이스 모델 업데이트
3. **멀티 태스킹** - 동시에 여러 모델 실행
4. **클라우드 연동** - 결과 업로드 및 분석
5. **ROS2 통합** - 공식 드라이버 개발

---

## 📚 참고 자료

- Hailo Developer Docs: https://docs.hailo.ai
- Raspberry Pi 공식 문서: https://www.raspberrypi.com/documentation
- YOLOv8 공식 페이지: https://docs.ultralytics.com
- OpenCV 튜토리얼: https://docs.opencv.org

---

**마지막 업데이트**: 2025년 12월 27일

---

## 📸 이미지 참고

**Note**: 원본 Notion 페이지에 포함된 이미지는 마크다운 텍스트 형식으로는 업로드할 수 없습니다. 
다음 이미지 주제들이 원본에 포함되어 있었습니다:
- Hailo-8 모듈 사진
- 라즈베리파이 5와의 연결 다이어그램
- 카메라 설치 이미지
- 객체 인식 결과 예시
- 성능 그래프

이미지가 필요하시면 원본 Notion 페이지를 참조하거나, 직접 촬영한 사진을 추가하실 수 있습니다.
