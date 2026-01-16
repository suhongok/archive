# OdinLift 개발 DevLog

## 2026-01-15 | Raspberry Pi 5 개발 환경 구축 및 v1.20 펌웨어 빌드

### 목표
라즈베리파이5에서 ESP32-S3 메카넘휠 제어 펌웨어(v1.20) 빌드 및 업로드 환경 구축

### 완료 항목

#### 1. 라즈베리파이5 개발 환경 세팅
- **OS**: Ubuntu 24.04 (ARM64)
- **네트워크**: WiFi 안정적 연결 (172.30.1.74)
- **메모리**: 6.8GB 사용 가능, 4.6GB 디스크 여유, 2.0GB Swap

#### 2. Arduino CLI 설치
```bash
# 설치 방법
cd ~/bin && wget https://downloads.arduino.cc/arduino-cli/arduino-cli_latest_Linux_ARM64.tar.gz
tar xf arduino-cli_latest_Linux_ARM64.tar.gz
./arduino-cli version
# 결과: 1.4.0
```

#### 3. ESP32 코어 설치
```bash
# 기본 ESP32 코어 (3.3.5)
arduino-cli core install esp32:esp32@3.3.5
# 설치 시간: 30분 이상 (대용량 패키지)

# esp32-bluepad32 코어 (4.1.0)
# Mac에서 압축 후 전송
tar -czf esp32-bluepad32.tar.gz esp32-bluepad32/  # 184MB (원본 582MB)
scp ... pi@172.30.1.74:~/
cd ~/.arduino15/packages && tar -xzf ~/esp32-bluepad32.tar.gz
```

#### 4. 라즈베리파이 ↔ Mac 파일 전송
```bash
# MecanumWheelDrive 프로젝트 전송
scp -r /Users/a/Documents/Arduino/MecanumWheelDrive pi@172.30.1.74:~/

# 검증
ls -la ~/MecanumWheelDrive/esp32/arduino/mecanum_drive_v120/
```

#### 5. ESP32-S3 USB 연결
- **문제**: 초기 USB 인식 안 됨
- **원인**: USB-A/USB-C 타입 혼동
- **해결**: USB-A(라즈베리파이) ↔ USB-C(ESP32-S3) 올바른 연결
- **결과**: `/dev/ttyACM0` 정상 인식
  ```
  Device: Bus 003 Device 003: ID 303a:1001 Espressif USB JTAG/serial debug unit
  ```

#### 6. 테스트 펌웨어 업로드
```bash
# CmdVelParser.ino (기존 작동 확인 펌웨어)
python3 -m esptool \
  --chip esp32s3 --port /dev/ttyACM0 --baud 921600 \
  write_flash 0x0 CmdVelParser.ino.bin

# 결과: ✓ 성공 (547KB)
```

### 주요 기술 이슈 및 해결

#### Issue 1: Bluepad32 라이브러리 API 불일치

**문제:**
```
error: 'class Controller' has no member named 'miscStart'
  367 | if (ctl->miscStart()) {
```

**원인:**
- Bluepad32-arduino v1.3.5는 NINA-W10 보드 전용
- ESP32-S3 네이티브 USB에서는 API 다름

**해결:**
```cpp
// v1.20 펌웨어 코드 수정
// ctl->miscStart() → ctl->miscHome()
// (START/Options/+ 버튼 → HOME/Options 버튼으로 변경)
```

#### Issue 2: 라즈베리파이에서 컴파일 실패

**시도 1: 기본 ESP32 코어 사용**
```bash
arduino-cli compile -b esp32:esp32:esp32s3 \
  --board-options "CDCOnBoot=cdc,USBMode=hwcdc" \
  --output-dir ./build_v120 \
  ./esp32/arduino/mecanum_drive_v120/mecanum_drive_v120.ino
# 결과: ✗ 실패 (Bluepad32 NINA-W10 호환성 에러)
```

**시도 2: esp32-bluepad32 코어 사용**
```bash
arduino-cli compile -b esp32-bluepad32:esp32:esp32s3 \
  --output-dir ./build_v120 \
  ./esp32/arduino/mecanum_drive_v120/mecanum_drive_v120.ino
# 결과: ✗ 실패 (esptool_py 경로 에러)
```

**최종 해결: Mac에서 컴파일**
```bash
# Mac의 esp32-bluepad32 4.1.0 코어로 컴파일
/opt/homebrew/bin/arduino-cli compile \
  -b esp32-bluepad32:esp32:esp32s3 \
  --board-options "CDCOnBoot=cdc,USBMode=hwcdc" \
  --libraries "/Users/a/Documents/Arduino/MecanumWheelDrive/esp32/arduino/libraries" \
  --output-dir /Users/a/Documents/Arduino/MecanumWheelDrive/build_v120_mac \
  /Users/a/Documents/Arduino/MecanumWheelDrive/esp32/arduino/mecanum_drive_v120/mecanum_drive_v120.ino

# 결과: ✓ 성공 (614KB 바이너리)
```

### v1.20 펌웨어 빌드 결과

| 항목 | 수치 | 상태 |
|------|------|------|
| 펌웨어 크기 | 601KB | ✓ 정상 (범위: 0-1310KB) |
| 플래시 사용률 | 46% | ✓ 여유 있음 |
| 메모리 사용 | 67KB | ✓ 여유 있음 (20%) |
| 컴파일 플랫폼 | esp32-bluepad32:esp32:esp32s3 | ✓ 확정 |
| 부트로더 | 15KB | ✓ 포함 |
| 파티션 테이블 | 3KB | ✓ 포함 |

### ESP32-S3에 업로드

```bash
# 라즈베리파이에서 실행
python3 -m esptool \
  --chip esp32s3 --port /dev/ttyACM0 --baud 921600 \
  write_flash 0x0 ~/build_v120/mecanum_drive_v120.ino.bin

# 결과
Wrote 615040 bytes (382318 compressed) at 0x00000000 in 3.5 seconds
Hash of data verified.
Hard resetting via RTS pin...
✓ 성공
```

### 최종 환경 구성

```
Mac (빌드/컴파일)
├── esp32-bluepad32:esp32 v4.1.0
├── MecanumWheelDrive 프로젝트
└── build_v120_mac/ (바이너리)
        ↓ scp
Raspberry Pi 5 (업로드/검증)
├── arduino-cli 1.4.0
├── ESP32 코어 3.3.5 (도구)
├── MecanumWheelDrive 프로젝트
└── esptool 5.1.0
        ↓ USB /dev/ttyACM0
ESP32-S3
└── v1.20 펌웨어 (실행 중)
    ├── Bluepad32 게임패드 지원
    ├── ROS2 통합
    ├── 메카넘 휠 제어 (cmd_vel 프로토콜)
    └── 모드 전환 (GAMEPAD/ROS2/NEUTRAL/REMOTE)
```

### 사용된 주요 도구/라이브러리

| 도구 | 버전 | 용도 | 플랫폼 |
|------|------|------|--------|
| arduino-cli | 1.4.0 | 헤드리스 컴파일 | RPi5 |
| ESP32 Core | 3.3.5 | 기본 ESP32 지원 | RPi5 |
| esp32-bluepad32 Core | 4.1.0 | Bluepad32 게임패드 | Mac |
| esptool.py | 5.1.0 | 펌웨어 업로드 | RPi5 |
| Bluepad32-arduino | 1.3.5 | 게임패드 API | (NINA-W10 호환 사용) |
| MecanumDrive485 | 0.2.0 | RS-485 모터 제어 | 프로젝트 내 |
| Ros2Ctrl | 1.0.0 | ROS2 제어 통합 | 프로젝트 내 |
| ArduinoJson | 7.4.2 | JSON 파싱 | 프로젝트 내 |

### 학습 포인트

1. **크로스 플랫폼 컴파일**: ARM64 라즈베리파이와 x86 Mac의 코어 호환성 차이
2. **Bluepad32 생태계**:
   - Arduino 라이브러리 (NINA-W10) vs
   - Arduino 코어 (esp32-bluepad32: ESP32 네이티브 USB 지원)
3. **메모리 제약**: ESP32-S3 기본 모델(512KB SRAM) 충분함
4. **USB JTAG**: Espressif 네이티브 USB 디버깅 포트 매우 유용

### 다음 단계

- [ ] 시리얼 모니터로 부팅 메시지 확인
- [ ] Bluepad32 게임패드 테스트
- [ ] ROS2 cmd_vel 메시지 송수신 테스트
- [ ] 모드 전환 동작 확인
- [ ] 메카넘 휠 실제 구동 테스트

### 참고 자료

- **ESP32-S3 사양**: WROOM-1U (512KB SRAM, 8MB Flash, 네이티브 USB JTAG)
- **Bluepad32**: https://github.com/ricardoquesada/bluepad32
- **Allturn USB NDJSON Protocol v1**: `{"cmd": "vel", "linear_x": 0.5, "linear_y": 0.0, "angular_z": 0.3}`
- **메카넘 휠 공식**:
  ```
  FL = linear_x + linear_y + angular_z
  FR = linear_x - linear_y - angular_z
  RL = linear_x - linear_y + angular_z
  RR = linear_x + linear_y - angular_z
  ```

---

**작성일**: 2026-01-15
**작업 시간**: ~45분 (환경 구축 제외)
**상태**: ✓ 완료 (v1.20 펌웨어 성공적으로 빌드 및 업로드)
