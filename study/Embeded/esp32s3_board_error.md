# ESP32-S3 보드 USB 미인식 에러 해결 가이드

## 문제 상황

**증상**: ESP32-S3 Uno 보드에 프로그램 업로드 후 USB 포트가 인식되지 않음

```
업로드 전: ✅ USB 포트 감지됨 (/dev/cu.usbmodem*)
프로그램 업로드: ✅ 성공
업로드 후: ❌ USB 포트 미인식
```

## 근본 원인

**ESP32-S3 Uno는 Native USB 직접 통신 방식**이므로:
- `CDCOnBoot=default` (Disabled) ❌ → USB 통신 비활성화됨
- `CDCOnBoot=cdc` (Enabled) ✅ → USB 통신 정상 작동

### 보드별 USB 통신 방식

| 보드 | USB 칩 | CDC 설정 | 이유 |
|------|--------|---------|------|
| ESP32-S3 Dev Module | CH340C (외부 칩) | `CDCOnBoot=default` | 외부 칩이 시리얼 담당 |
| **ESP32-S3 Uno** | CH340C (외부 칩) | **`CDCOnBoot=default`** | **보드 자체에서 USB 처리** |
| ESP32-S3 DevKit | Native USB | `CDCOnBoot=cdc` | Native USB 지원 | **arduino 설정에서는 enable **

## 🔨 복구 절차

### Step 1: BOOT 모드로 강제 진입

**필요한 버튼**:
- **BOOT 버튼** (GPIO0, 작은 버튼)
- **RESET 버튼** (보드 우측)

**복구 시퀀스** (매우 중요!):

```
① BOOT 버튼을 누른 상태로 유지 (손가락으로 계속 누르고 있음)
                ↓
② RESET 버튼을 한 번 눌렀다 떼기 (~1초)
                ↓
③ BOOT 버튼 떼기
                ↓
④ 약 1-2초 대기
                ↓
⑤ 포트 확인
```

### Step 2: 포트 재인식 확인

```bash
# 포트 목록 확인
arduino-cli board list

# 정상 결과 예시:
# Port       Type          Board Name            FQBN                     Core
# /dev/cu.usbmodem14201   Serial Port (USB)     Arduino Nano 33 IoT      arduino:samd:nano_33_iot
```

### Step 3: 올바른 설정으로 재업로드

```bash
# ✅ 올바른 방법 (CDCOnBoot=cdc)
arduino-cli compile \
  --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc \
  esp32/arduino/RobotLED_Control

arduino-cli upload \
  -p /dev/cu.usbmodem* \
  --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc \
  esp32/arduino/RobotLED_Control
```

**포트 찾기 팁** (정확한 포트명 확인):
```bash
# macOS/Linux
arduino-cli board list | grep usb

# 또는 모든 포트 나열
ls /dev/tty.* | grep usb
```

### Step 4: 업로드 완료 후 검증

```bash
# 시리얼 모니터로 정상 작동 확인
screen /dev/cu.usbmodem* 115200

# 또는 Python으로 테스트
python3 << 'EOF'
import serial
import time

port = "/dev/cu.usbmodem*"  # 실제 포트로 수정
ser = serial.Serial(port, 115200)
time.sleep(1)

# LED 제어 명령 전송
ser.write(b'{"mode":"ros2"}\n')
print("Command sent successfully!")

time.sleep(1)
ser.close()
EOF
```

## 💡 주요 포인트

### BOOT 모드의 역할
- **프로그램 보호**: 새 코드를 받기 위해 기존 프로그램 무시
- **플래시 쓰기 대기**: ROM bootloader가 시리얼 통신을 위해 대기
- **포트 인식**: USB 포트가 다시 인식되는 상태

### CDC On Boot 설정의 의미
```cpp
CDCOnBoot=cdc (Enabled)
  ↓
ESP32-S3이 부팅될 때 Native USB를 시리얼 포트로 활성화
  ↓
컴퓨터에서 /dev/cu.usbmodem* 로 인식
```

```cpp
CDCOnBoot=default (Disabled)
  ↓
Native USB 비활성화 (외부 칩이 있는 경우만 사용)
  ↓
컴퓨터에서 포트 미인식 ❌
```

## 🚀 예방 방법

### 1. Arduino IDE에서 올바른 설정

**Tools 메뉴**:
```
Board:              ESP32S3 Dev Module (또는 ESP32-S3)
USB CDC On Boot:    Enabled ✅
Upload Mode:        USB-OTG (또는 기본값)
USB Mode:           Hardware CDC and JTAG (또는 기본값)
```

### 2. arduino-cli 사용 시

항상 컴파일, 업로드 모두에서 `CDCOnBoot=cdc` 지정:
```bash
# 컴파일
arduino-cli compile --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc .

# 업로드
arduino-cli upload -p /dev/cu.usbmodem* --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc .
```

### 3. 스크립트 자동화

```bash
#!/bin/bash
# upload_esp32s3.sh

PORT=${1:-/dev/cu.usbmodem14201}
SKETCH_DIR=${2:-.}

echo "🔄 Compiling..."
arduino-cli compile --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc "$SKETCH_DIR" || exit 1

echo "📤 Uploading..."
arduino-cli upload -p "$PORT" --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc "$SKETCH_DIR" || exit 1

echo "✅ Upload complete!"
```

사용법:
```bash
chmod +x upload_esp32s3.sh
./upload_esp32s3.sh /dev/cu.usbmodem14201 ./my_sketch
```

## 🆘 만약 복구 안 되면?

### 최후의 수단: 플래시 초기화

```bash
# BOOT 모드 진입 후

# 1. 플래시 전체 삭제
esptool.py --port /dev/cu.usbmodem* erase_flash

# 2. 기다렸다가 RESET 버튼 누르기
# (또는 esptool이 자동으로 처리)

# 3. 프로그램 재업로드
arduino-cli upload -p /dev/cu.usbmodem* \
  --fqbn esp32:esp32:esp32s3:CDCOnBoot=cdc \
  ./my_sketch
```

## 📋 체크리스트

- [ ] BOOT 모드 진입 성공 (포트 감지됨)
- [ ] `CDCOnBoot=cdc` 설정 확인
- [ ] 컴파일 성공
- [ ] 업로드 성공 (~10초 소요)
- [ ] 업로드 후 포트 재인식 확인 (`arduino-cli board list`)
- [ ] 시리얼 모니터/Python으로 통신 테스트

## 참고 자료

- [Espressif ESP32-S3 기술 사양](https://www.espressif.com/sites/default/files/documentation/esp32-s3_datasheet_en.pdf)
- [Arduino IDE Board Manager - ESP32](https://github.com/espressif/arduino-esp32)
- [esptool 문서](https://github.com/espressif/esptool)

---

**작성일**: 2025-12-29
**보드**: ESP32-S3 Uno
**상태**: ✅ 해결됨
