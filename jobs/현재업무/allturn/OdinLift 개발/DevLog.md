# OdinLift 개발 로그

## 2025-01-15: ESP32-S3-Relay-6CH 릴레이 테스트 구현

### 개요

Waveshare ESP32-S3-Relay-6CH 모듈의 릴레이 제어 테스트 펌웨어 구현 완료.

### 하드웨어 구성

- **모듈**: Waveshare ESP32-S3-Relay-6CH
- **연결**: 라즈베리파이 5 (172.30.1.74) USB 연결
- **시리얼 포트**: `/dev/ttyACM0` (115200 baud)

### GPIO 핀 매핑

| GPIO | 채널 | 기능 |
|------|------|------|
| GPIO 1 | CH1 | 릴레이 1 |
| GPIO 2 | CH2 | 릴레이 2 |
| GPIO 41 | CH3 | 릴레이 3 |
| GPIO 42 | CH4 | 릴레이 4 |
| GPIO 45 | CH5 | **Brake Release** (서보 브레이크 해제) |
| GPIO 46 | CH6 | **Driver Power ON** (드라이버 전원) |
| GPIO 21 | - | Buzzer |
| GPIO 38 | - | RGB LED (WS2812) |

### 서보 모터 동작 조건

```
⚠️ 서보 모터 동작 시 반드시 다음 순서로 릴레이 활성화:
1. CH6 ON (드라이버 전원 ON)
2. CH5 ON (브레이크 해제)
```

### 시리얼 명령어

| 명령어 | 설명 |
|--------|------|
| `1 on` ~ `6 on` | 개별 릴레이 ON |
| `1 off` ~ `6 off` | 개별 릴레이 OFF |
| `1 toggle` | 릴레이 토글 |
| `all on` / `all off` | 전체 제어 |
| `status` | 상태 조회 |
| `beep` | 부저 울림 |
| `help` | 도움말 |

### 프로젝트 구조

```
Odin_lift/
├── platformio.ini           # PlatformIO 설정 (ESP32-S3, USB CDC)
├── include/
│   ├── config.h             # GPIO 핀 매핑 및 상수
│   ├── relay_controller.h   # 릴레이 제어 클래스
│   └── command_parser.h     # 시리얼 명령어 파서
└── src/
    ├── main.cpp             # 메인 애플리케이션
    ├── relay_controller.cpp # 릴레이 제어 구현
    └── command_parser.cpp   # 명령어 파싱 구현
```

### 빌드 및 업로드

```bash
# 로컬 빌드
~/.platformio/penv/bin/pio run

# 라즈베리파이로 펌웨어 전송
scp .pio/build/esp32-s3-relay-6ch/*.bin pi@172.30.1.74:/tmp/

# 라즈베리파이에서 업로드
ssh pi@172.30.1.74
python3 -m esptool --chip esp32s3 --port /dev/ttyACM0 --baud 921600 \
  write-flash 0x0 /tmp/bootloader.bin 0x8000 /tmp/partitions.bin 0x10000 /tmp/firmware.bin
```

### 테스트 결과

- ✅ 전체 6채널 릴레이 ON/OFF 동작 확인
- ✅ 개별 릴레이 제어 동작 확인
- ✅ 부저 피드백 동작 확인
- ✅ 시리얼 명령어 파싱 정상 동작

### 다음 단계

- [ ] 서보 드라이버 통신 테스트 (시리얼 응답 확인 필요)
- [ ] USB NDJSON Control Protocol 구현
- [ ] 안전 인터록 로직 추가 (전원 ON → 브레이크 해제 순서 강제)

---

## 2025-01-15: 서보 드라이버 속도 제어 구현 (진행 중)

### 개요

4개의 서보 드라이버(FL/FR/RL/RR)를 RS485 Modbus RTU로 개별 속도 제어하는 기능 구현.

### 참조 코드

- MecanumWheelDrive 레포지토리의 MecanumDrive485 라이브러리 참조
- Modbus RTU 프로토콜 (115200 baud, 8N1)

### 구현 완료

1. **config.h 확장**
   - RS485 핀 정의 (TX: GPIO17, RX: GPIO18)
   - 드라이버 ID, 방향 보정값, MAX_RPM 등 상수 정의
   - Modbus 레지스터 주소 정의

2. **servo_driver.h/cpp 신규 생성**
   - Modbus RTU 통신 구현 (CRC16, read/write 레지스터)
   - 개별/전체 드라이버 속도 제어
   - 기본 주행 패턴 (전진, 후진, 횡이동, 회전)

3. **command_parser.h/cpp 확장**
   - 드라이버 명령어 추가:
     - `driver on/off` - 전원 시퀀스
     - `speed <id> <rpm>` - 개별 속도 설정
     - `fwd/rev/left/right/cw/ccw <rpm>` - 주행 명령
     - `dstatus/dcheck` - 상태 확인

4. **main.cpp 수정**
   - ServoDriver 초기화
   - 드라이버 전원 시퀀스 (CH6→CH5)
   - 안전 인터록 로직

### 빌드 결과

- ✅ 빌드 성공 (RAM: 5.9%, Flash: 9.0%)
- ✅ 펌웨어 업로드 성공

### 미해결 이슈

- ⚠️ 시리얼 통신 응답 없음 - 디버깅 필요
  - USB CDC 설정은 올바름 (ARDUINO_USB_CDC_ON_BOOT=1)
  - USB 장치는 정상 인식됨 (ttyACM0)
  - 내일 시리얼 통신 문제 해결 필요

### 신규 시리얼 명령어

| 명령어 | 설명 |
|--------|------|
| `driver on` | 드라이버 전원 ON (CH6→CH5 순서) |
| `driver off` | 드라이버 전원 OFF (CH5→CH6 순서) |
| `speed <id> <rpm>` | 개별 드라이버 속도 (id: 1-4) |
| `speed all <rpm>` | 전체 동일 속도 |
| `stop` | 전체 정지 |
| `fwd/rev <rpm>` | 전진/후진 |
| `left/right <rpm>` | 횡이동 |
| `cw/ccw <rpm>` | 회전 |
| `dstatus` | 드라이버 상태 |
| `dcheck` | 드라이버 연결 확인 |

---

## 2026-01-16: 메카넘휠 제어 시스템 구현 완료

### 개요

라즈베리파이에서 JSON 속도 명령을 수신하여 메카넘휠 역기구학으로 4바퀴 RPM을 계산하고 제어하는 시스템 구현 완료.

### 시스템 흐름

```
[라즈베리파이] --JSON(USB/UART)--> [ESP32-S3] --RS485--> [서보드라이버 1~4]
                                      │
                                      ├─ 1. 부팅 시 릴레이 ON (CH6→CH5)
                                      ├─ 2. 서보드라이버 통신 테스트
                                      ├─ 3. JSON 명령 수신 대기
                                      ├─ 4. 역기구학 계산 (x,y,omega → 4RPM)
                                      ├─ 5. 각 바퀴 RPM 설정
                                      ├─ 6. 순차 START
                                      └─ 7. 엔코더 피드백 확인
```

### JSON 명령 형식

```json
{"x": 0.5, "y": 0.0, "z": 0.0}
```
- `x`: 전진/후진 속도 (m/s), +전진 -후진
- `y`: 좌/우 횡이동 속도 (m/s), +좌 -우
- `z`: 회전 각속도 (rad/s), +반시계 -시계

### 구현 파일

| 파일 | 설명 |
|------|------|
| `include/MecanumDrive485.h` | RS485 Modbus RTU 서보 드라이버 제어 클래스 |
| `src/MecanumDrive485.cpp` | Modbus 통신 및 모션 제어 구현 |
| `include/kinematics.h` | 역기구학 파라미터 및 함수 선언 |
| `src/kinematics.cpp` | 메카넘휠 역기구학 계산 구현 |
| `include/json_command.h` | JSON 속도 명령 구조체 |
| `src/json_command.cpp` | 간단한 JSON 파서 구현 |
| `src/main.cpp` | 메인 제어 루프 |

### 서보 드라이버 레지스터 (Lichuan DS_R 485)

| 레지스터 | 주소 | 설명 |
|----------|------|------|
| PA_094 | 0x0094 | Operating mode (3=속도모드) |
| PA_091 | 0x0091 | Control command |
| PA_09E~0A3 | 0x009E~ | 가감속/속도 배치 설정 |
| PA_0A2/0A3 | 0x00A2/A3 | Target velocity (설정값) |
| PA_098/099 | 0x0098/99 | **Current velocity (실제 피드백)** |
| PA_12 | 0x0012 | Feedback velocity (16비트) |

### 주요 발견 사항

#### 1. 엔코더 피드백 읽기
- **문제**: 기존 코드가 PA_0A2/0A3 (설정값)을 읽어서 target=actual 동일
- **해결**: PA_098/099 (Current velocity)로 변경하여 실제 피드백 읽기

#### 2. Modbus 브로드캐스트
- **테스트**: 주소 0으로 브로드캐스트 시도
- **결과**: 드라이버가 브로드캐스트 미지원, 피드백 읽기 실패
- **해결**: 순차 START 방식 유지 (각 드라이버에 개별 명령)

#### 3. 제어 명령 값 (PA_091)
- **매뉴얼**: 속도 모드 시작 = 4 (Bit2)
- **실제 동작**: 값 **8** (Bit3)로 동작함
- 매뉴얼과 실제 동작이 다름

### 역기구학 수식

```
바퀴 배치 (위에서 본 모습):
  FL ---- FR
   |      |
  RL ---- RR

rpm_FL = (vx - vy - (L+W)*omega) * 60 / (2*π*r)
rpm_FR = (vx + vy + (L+W)*omega) * 60 / (2*π*r)
rpm_RL = (vx + vy - (L+W)*omega) * 60 / (2*π*r)
rpm_RR = (vx - vy + (L+W)*omega) * 60 / (2*π*r)
```

### 테스트 결과

```bash
# 전진 명령
echo '{"x":0.5,"y":0,"z":0}' > /dev/ttyACM0

# 결과
CMD: x=0.500, y=0.000, z=0.000
RPM: FL=95, FR=-95, RL=95, RR=-95
--- Speed Feedback ---
  FL: target=95, actual=91 (diff=-4)
  FR: target=-95, actual=-92 (diff=3)
  RL: target=95, actual=95 (diff=0)
  RR: target=-95, actual=-96 (diff=-1)
```

- ✅ RS485 통신 정상 (3/4 드라이버 응답, ID 2 하드웨어 문제)
- ✅ JSON 명령 파싱 정상
- ✅ 역기구학 계산 정상
- ✅ 엔코더 피드백 읽기 정상 (PA_098/099)
- ✅ 모터 동작 확인

### 다음 단계

- [ ] ID 2 드라이버 하드웨어 점검
- [ ] 라즈베리파이 ROS2 노드 연동
- [ ] 속도 PID 튜닝
- [ ] 오도메트리 계산 추가

---

## 2026-01-19: 모터 움찔거림 문제 해결

### 문제 현상

게임패드로 전진 명령 시 모터가 주기적으로 움찔거림(jitter) 발생.

### 원인 분석

`motor_task.cpp`의 타임아웃 로직이 과도하게 동작:
- `lastCmdTime` 기반 타임아웃 체크가 정상 동작 중에도 트리거
- "Command timeout - stopping" 로그가 반복 출력
- 타임아웃마다 모터 정지 → 재시작 반복으로 움찔거림 발생

### 해결 방법

#### 1. motor_task.cpp - 타임아웃 로직 제거

```cpp
// 제거된 코드:
// - TickType_t lastCmdTime 변수
// - uint32_t targetTimestamp 변수
// - 타임아웃 체크 섹션 (if ((now - lastCmdTime) > pdMS_TO_TICKS(...)))
```

타임아웃 기반 안전 기능을 command_task의 연결 끊김 감지로 대체.

#### 2. command_task.cpp - 컨트롤러 연결 끊김 감지

```cpp
if (currentMode == InputMode::GAMEPAD) {
    // 컨트롤러 연결 끊김 감지 → NEUTRAL 모드로 전환
    if (!gpData.connected) {
        modeManager.enterNeutral();
        LOG.println("[CommandTask] Controller disconnected - switching to NEUTRAL");
        continue;
    }
    // ...
}
```

#### 3. command_task.cpp - 릴레이 로그 최적화

```cpp
// 릴레이 상태는 변경 시에만 출력
static int prevCH5 = -1, prevCH6 = -1, prevServoEnabled = -1;
if (curCH5 != prevCH5 || curCH6 != prevCH6 || curServoEnabled != prevServoEnabled) {
    LOG.printf("[DEBUG] Relay CH5=%d, CH6=%d, servoEnabled=%d\n", ...);
    prevCH5 = curCH5; prevCH6 = curCH6; prevServoEnabled = curServoEnabled;
}
```

### 변경 파일

| 파일 | 변경 사항 |
|------|-----------|
| `main/rtos/motor_task.cpp` | 타임아웃 로직 완전 제거 |
| `main/rtos/command_task.cpp` | 연결 끊김 → NEUTRAL 전환, 릴레이 로그 변경시만 출력 |

### 테스트 결과

- ✅ 게임패드 전진 명령 시 움찔거림 없음
- ✅ "Command timeout" 로그 사라짐
- ✅ 컨트롤러 끄면 NEUTRAL 모드로 자동 전환
- ✅ 릴레이 로그 스팸 제거

---

## 2026-01-19: 조이스틱 Drift로 인한 모터 미정지 문제 해결

### 문제 현상

- 전진/후진 후 스틱 놓으면 → **정상 정지**
- 좌우 이동/회전 후 스틱 놓으면 → **천천히 계속 회전**

### 원인 분석

1. **조이스틱 물리적 특성**
   - 왼쪽 Y축 (전진/후진): 놓으면 정확히 중립 복귀
   - 왼쪽 X축 (좌우): drift 있음 - 놓아도 데드존 밖(51~70)에 걸림
   - 오른쪽 X축 (회전): 마찬가지로 drift 발생

2. **작은 입력이 RPM으로 변환**
   ```
   스틱값 65 → normalized ≈ 0.032 → vy ≈ 0.016 m/s → 약 10~30 RPM 생성
   ```

3. **RampController의 즉시 정지 조건**
   ```cpp
   if (_targetRPM == 0 && abs(_currentRPM) <= threshold) → 즉시 정지
   ```
   - `_targetRPM == 0` 조건이 있어서 target이 10 RPM이면 적용 안 됨

### 해결 방법

정규화 후 작은 값(5% 이하)을 0으로 클램핑하여 drift 무시.

#### config.h

```cpp
// 정규화 입력 클램핑 임계값 (drift 방지)
#define NORMALIZED_INPUT_THRESHOLD   0.05f
```

#### bt_controller.cpp

```cpp
// 정규화 후 작은 값 클램핑 (drift 방지)
if (fabsf(normLY) < NORMALIZED_INPUT_THRESHOLD) normLY = 0;
if (fabsf(normLX) < NORMALIZED_INPUT_THRESHOLD) normLX = 0;
if (fabsf(normRX) < NORMALIZED_INPUT_THRESHOLD) normRX = 0;
```

### 변경 파일

| 파일 | 변경 사항 |
|------|-----------|
| `include/config.h` | `NORMALIZED_INPUT_THRESHOLD` 상수 추가 |
| `src/bt_controller.cpp` | 정규화 후 각 축 클램핑 로직 추가 |

### 테스트 결과

- ✅ 좌우 이동 후 스틱 놓기 → 모터 완전 정지
- ✅ 회전 후 스틱 놓기 → 모터 완전 정지
- ✅ 전진/후진 기존 동작 유지

---

## 2026-01-19: 저속 RPM 정지 안됨 버그 수정

### 문제 현상

```
[DEBUG] v1.20: tgt=[0,0,0] cur=[0.0,0.0,0.0] rpm=[18,18,-18,-18]
```
- ESP32는 이미 0 명령을 보냄 (`tgt=0, cur=0`)
- 하지만 모터는 여전히 18 RPM으로 저속 회전 지속

### 원인 분석

#### 1. RPM_DEADBAND 문제
```cpp
static const int32_t RPM_DEADBAND = 30;  // 기존값
```
- `abs(targetRpm - lastSentRpm)` > 30 일 때만 명령 전송
- 저속(18~23 RPM)에서는 변화량이 30 미만 → 0 명령이 전송되지 않음

#### 2. 피드백 확인 로직 부재
- 드라이버가 명령을 놓쳤을 경우 재전송 메커니즘 없음
- 실제 모터 속도와 명령값 불일치 감지 불가

### 해결 방법

#### 1. RPM_DEADBAND 축소

**파일: `main/rtos/motor_task.cpp`**
```cpp
// 변경 전
static const int32_t RPM_DEADBAND = 30;

// 변경 후
static const int32_t RPM_DEADBAND = 10;
```

#### 2. 피드백 기반 명령 재전송 로직 추가

**파일: `main/rtos/motor_task.cpp`**
```cpp
} else {
    // 명령 전송 없을 때: 피드백 확인하여 불일치 시 재전송
    static uint32_t lastFeedbackCheckMs = 0;
    uint32_t now = millis();

    // 200ms마다 피드백 확인
    if (now - lastFeedbackCheckMs >= 200) {
        lastFeedbackCheckMs = now;

        bool needResend = false;
        int32_t actualRpm[4] = {0};

        for (int i = 0; i < 4; i++) {
            int32_t speed = 0;
            if (drive->readSpeed(DRIVER_IDS[i], speed)) {
                actualRpm[i] = speed;
                // 실제 속도와 전송한 명령 비교
                if (abs(speed - lastSentRpm[i]) > RPM_DEADBAND) {
                    needResend = true;
                }
            }
        }

        if (needResend) {
            // 명령 재전송 (현재 목표 RPM으로)
            for (int i = 0; i < 4; i++) {
                drive->setSpeed(DRIVER_IDS[i], FIXED_RAMP_TIME_MS, targetRpm[i], FIXED_RAMP_TIME_MS);
            }
            LOG.printf("[MotorTask] Resend! cmd=[%ld,%ld,%ld,%ld] actual=[%ld,%ld,%ld,%ld]\n",
                       targetRpm[0], targetRpm[1], targetRpm[2], targetRpm[3],
                       actualRpm[0], actualRpm[1], actualRpm[2], actualRpm[3]);
            memcpy(lastSentRpm, targetRpm, sizeof(lastSentRpm));
        }
    }
}
```

### 동작 흐름

```
motorControlTask() (50Hz 주기)
     │
     ├─ 타겟 설정 → ramp 업데이트 → targetRpm 계산
     │
     ├─ targetRpm 변경됨? (|변화| > 10)
     │      ├─ YES → 드라이버에 전송
     │      │
     │      └─ NO → 200ms마다 피드백 확인
     │               │
     │               └─ 실제 RPM과 lastSentRpm 차이 > 10?
     │                       └─ YES → targetRpm으로 재전송 + 로그
```

### 프로젝트 정리

사용되지 않는 폴더 삭제:
- `src/` - 빌드에 사용 안 됨 (실제 소스는 `main/`)
- `include/` - 빌드에 사용 안 됨 (헤더는 `main/`에 포함)
- `lib/` - 비어있음
- `test/` - 비어있음

### 최종 프로젝트 구조

```
Odin_lift/
├── main/                # ★ 실제 소스 코드
│   ├── rtos/            # RTOS 태스크 파일
│   │   ├── motor_task.cpp
│   │   ├── command_task.cpp
│   │   └── ...
│   ├── config.h
│   ├── sketch.cpp
│   └── ...
├── components/          # ESP-IDF 컴포넌트
├── tools/scripts/       # 빌드/배포 스크립트
├── platformio.ini
└── ...
```

### 변경 파일

| 파일 | 변경 사항 |
|------|-----------|
| `main/rtos/motor_task.cpp` | RPM_DEADBAND 30→10, 피드백 기반 재전송 로직 추가 |

### 테스트 결과

```
[MotorTask] Resend! cmd=[0,0,0,0] actual=[0,15,-1,-1]
```

- ✅ 저속 RPM에서도 0 명령 전송됨
- ✅ 피드백 불일치 감지 및 재전송 동작
- ✅ 모터 완전 정지 확인
