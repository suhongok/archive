# ESP32-S3 Native USB 기반 JSON 통신 구축

## 📌 프로젝트 개요

**상태**: 진행 중  
**작성자**: 옥성민  
**생성일**: 2025년 12월 19일  
**마지막 수정**: 2025년 12월 23일

---

## 🎯 목표

- ESP32-S3 마이크로컨트롤러의 Native USB 포트를 활용한 통신 구축
- JSON 기반의 구조화된 명령 프로토콜 개발
- 메카넘휠 로봇의 속도 제어 (cmd_vel) 구현
- ROS2 호환성 고려

---

## 🔧 기술 사양

### 하드웨어

| 항목 | 상세 |
|------|------|
| **MCU** | ESP32-S3 (Dual-core, 32-bit) |
| **USB** | Native USB 2.0 (High-Speed) |
| **RAM** | 520 KB |
| **Flash** | 8 MB (기본) |
| **GPIO** | 45개 |

### 통신 프로토콜

#### **Allturn USB NDJSON Control Protocol v1**

**프로토콜 이름**: Allturn USB NDJSON Control Protocol  
**버전**: 1.0  
**형식**: NDJSON (Newline Delimited JSON)  
**목적**: 메카넘휠 로봇 속도 제어

#### 기본 구조

```json
{
  "cmd": "vel",
  "linear_x": 0.5,
  "linear_y": 0.0,
  "angular_z": 0.3,
  "timestamp": 1703338020
}
```

#### 필드 설명

| 필드 | 타입 | 범위 | 설명 |
|------|------|------|------|
| `cmd` | string | - | 명령 타입 ("vel", "stop", "status") |
| `linear_x` | float | -1.0 ~ 1.0 | 전진/후진 속도 |
| `linear_y` | float | -1.0 ~ 1.0 | 좌측/우측 이동 속도 |
| `angular_z` | float | -1.0 ~ 1.0 | 시계/반시계 회전 속도 |
| `timestamp` | int | - | Unix 타임스탬프 |

#### 명령 타입

```
1. vel - 속도 명령
   {
     "cmd": "vel",
     "linear_x": 0.5,
     "linear_y": 0.0,
     "angular_z": 0.0
   }

2. stop - 정지 명령
   {
     "cmd": "stop"
   }

3. status - 상태 조회
   {
     "cmd": "status"
   }

4. calibrate - 캘리브레이션
   {
     "cmd": "calibrate"
   }
```

#### 응답 포맷

```json
{
  "status": "ok",
  "cmd": "vel",
  "battery": 85,
  "temperature": 32.5,
  "timestamp": 1703338020
}
```

---

## 💻 개발 환경

### 소프트웨어 스택

| 항목 | 도구/라이브러리 |
|------|-----------------|
| **개발 환경** | VS Code + PlatformIO |
| **펌웨어** | Arduino Framework for ESP32 |
| **USB 라이브러리** | TinyUSB (내장) |
| **JSON 파싱** | ArduinoJson 6.x |
| **게임컨트롤러** | Bluepad32 |

### 핵심 라이브러리

1. **ArduinoJson**: JSON 직렬화/역직렬화
2. **TinyUSB**: USB CDC (COM 포트) 에뮬레이션
3. **Bluepad32**: 무선 게임 컨트롤러 지원
4. **ESP32 HAL**: 모터 제어 PWM

---

## 🛠️ 구현 세부사항

### 1. USB 설정

```cpp
// USB Serial 초기화
void setup() {
  Serial.begin(115200);
  while (!Serial) {
    delay(100);
  }
  
  Serial.println("ESP32-S3 USB CDC Ready");
}
```

### 2. JSON 파싱

```cpp
void parseCommand(String jsonStr) {
  StaticJsonDocument<256> doc;
  DeserializationError error = deserializeJson(doc, jsonStr);
  
  if (error) {
    Serial.println("{\"status\": \"error\", \"message\": \"JSON parse failed\"}");
    return;
  }
  
  const char* cmd = doc["cmd"];
  float linear_x = doc["linear_x"] | 0.0;
  float linear_y = doc["linear_y"] | 0.0;
  float angular_z = doc["angular_z"] | 0.0;
  
  // 로봇 제어
  controlMecanum(linear_x, linear_y, angular_z);
  
  // 응답 전송
  sendStatus();
}
```

### 3. 속도 제어 (메카넘휠)

메카넘휠 제어 공식:

```
FL(Front-Left)  = linear_x + linear_y + angular_z
FR(Front-Right) = linear_x - linear_y - angular_z
RL(Rear-Left)   = linear_x - linear_y + angular_z
RR(Rear-Right)  = linear_x + linear_y - angular_z
```

### 4. 타이밍 제어

```cpp
void loop() {
  // USB로부터 데이터 수신
  if (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    parseCommand(command);
  }
  
  // 모터 제어 주기: 50Hz (20ms)
  if (millis() - lastControlTime > 20) {
    updateMotorControl();
    lastControlTime = millis();
  }
  
  // 상태 보고: 100ms 주기
  if (millis() - lastStatusTime > 100) {
    sendTelemetry();
    lastStatusTime = millis();
  }
}
```

---

## 📊 성능 사양

| 항목 | 값 |
|------|-----|
| **USB 대역폭** | 480 Mbps (이론) |
| **실제 처리량** | 약 50-100 cmd/sec |
| **명령 응답 시간** | < 5ms |
| **모터 제어 주기** | 20ms (50Hz) |
| **상태 보고 주기** | 100ms (10Hz) |

---

## 🧪 테스트 계획

### Phase 1: 기본 통신 테스트
- [ ] USB 연결 확인
- [ ] JSON 송수신 검증
- [ ] 프로토콜 호환성 확인

### Phase 2: 모터 제어 테스트
- [ ] 단일 모터 제어
- [ ] 메카넘휠 4개 모터 동시 제어
- [ ] 속도 정확성 검증

### Phase 3: 통합 테스트
- [ ] ROS2 with cmd_vel 호환성
- [ ] 야외 주행 테스트
- [ ] 안정성 및 신뢰성 검증

### Phase 4: 최적화
- [ ] 통신 속도 최적화
- [ ] 전력 소비 최적화
- [ ] 보안 강화 (암호화)

---

## 📋 필수 라이브러리

```ini
[platformio]
lib_deps =
    bblanchon/ArduinoJson@^6.20.0
    bluepad32
    esp32-hal
    espressif/esp32-ota@^2.0.0
```

---

## 🔌 포트 및 핀 배치

### USB
- USB D+: GPIO 20
- USB D-: GPIO 19

### 모터 제어 PWM
| 모터 | PWM Pin | Direction Pin |
|------|---------|---------------|
| FL (Front-Left) | GPIO 5 | GPIO 6 |
| FR (Front-Right) | GPIO 7 | GPIO 8 |
| RL (Rear-Left) | GPIO 9 | GPIO 10 |
| RR (Rear-Right) | GPIO 11 | GPIO 12 |

### 센서
| 센서 | Pin | 프로토콜 |
|------|-----|---------|
| IMU (MPU6050) | GPIO 21, 22 | I2C |
| 배터리 전압 | GPIO A0 | ADC |
| 온도 센서 | GPIO 3 | 1-Wire |

---

## 🔗 관련 문서

- [올턴 회사 분석](올턴_회사_분석.md)
- [기술 개발 항목](기술_개발_항목.md)
- [업무일지 12월](업무일지_12월.md)

---

## 🚀 향후 계획

1. **Bluepad32 게임컨트롤러 지원** - 무선 조종 기능 추가
2. **ROS2 통합** - nav_msgs/Twist 호환성
3. **센서 퓨전** - IMU 기반 안정성 향상
4. **OTA 업데이트** - 무선 펌웨어 업그레이드
5. **보안 강화** - TLS 암호화 통신

---

**마지막 업데이트**: 2025년 12월 27일
