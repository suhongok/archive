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

---

## 2026-01-20: 오른쪽 조이스틱 전진/후진 기능 추가

### 문제점

`bt_controller.cpp`에서 오른쪽 조이스틱의 Y축(`axisRY()`)을 전혀 읽지 않음.
기존에는 오른쪽 스틱 X축만 읽어서 회전(omega)에만 사용됨.

### 요구사항

- 오른쪽 조이스틱: `|RY| > |RX|` 이면 전진/후진, 아니면 회전
- 왼쪽 + 오른쪽 스틱 vx 값은 합산 (클램핑으로 과속 방지)

### 해결 방법

#### 1. 오른쪽 Y축 읽기 추가

**파일: `src/bt_controller.cpp`**
```cpp
// 오른쪽 스틱 (회전 또는 전진/후진)
int16_t rx = ctl->axisRX();  // -512 ~ +512
int16_t ry = ctl->axisRY();  // -512 ~ +512 (상향 음수) ★ 추가
```

#### 2. 정규화 추가

```cpp
float normRY = normalizeAxis(-ry, joystickConfig.deadzone);  // Y축 반전 (상향 양수)
```

#### 3. 조건 분기 및 속도 계산 변경

```cpp
// 오른쪽 스틱: |RY| > |RX| 이면 전진/후진, 아니면 회전
float rightVx = 0.0f;
float rightOmega = 0.0f;

if (fabsf(normRY) > fabsf(normRX)) {
    // Y축 우세: 전진/후진 모드
    rightVx = normRY * joystickConfig.maxVx;
} else {
    // X축 우세 또는 동일: 회전 모드
    rightOmega = -normRX * joystickConfig.maxOmega;
}

// 속도 계산 (왼쪽 + 오른쪽 합산)
input.vx = normLY * joystickConfig.maxVx + rightVx;
input.vy = -normLX * joystickConfig.maxVy;
input.omega = rightOmega;
```

### 동작 요약

| 입력 | 조건 | 결과 |
|------|------|------|
| 오른쪽 스틱 ↑ | `\|RY\| > \|RX\|` | 전진 (vx에 합산) |
| 오른쪽 스틱 ↓ | `\|RY\| > \|RX\|` | 후진 (vx에 합산) |
| 오른쪽 스틱 ← | `\|RX\| >= \|RY\|` | 시계방향 회전 |
| 오른쪽 스틱 → | `\|RX\| >= \|RY\|` | 반시계방향 회전 |

### 변경 파일

| 파일 | 변경 사항 |
|------|-----------|
| `src/bt_controller.cpp` | RY축 읽기, normRY 정규화, 조건 분기 및 합산 로직 추가 |

### 빌드 결과

- ✅ 빌드 성공 (RAM: 20.4%, Flash: 8.9%)

### 테스트 결과

- ✅ 오른쪽 스틱 ↑↓ 전진/후진 동작 확인
- ✅ 오른쪽 스틱 ←→ 회전 동작 유지
- ✅ 왼쪽 + 오른쪽 스틱 조합 동작 확인

---

## 2026-01-21: 블루투스 컨트롤러 MAC 주소 필터링 구현

### 배경

2개의 ESP32-S3 보드가 각각 특정 블루투스 리모컨에만 연결되도록 MAC 주소 기반 필터링 필요.

### 구현 내용

#### 1. MAC 주소 로깅 기능 추가

**파일: `src/bt_controller.cpp`**
```cpp
#include "config.h"

extern "C" {
#include "bt/uni_bt_allowlist.h"
}

// onConnectedController() 콜백에 MAC 주소 출력 추가
ControllerProperties props = ctl->getProperties();
LOG.printf("[BT] MAC Address: %02X:%02X:%02X:%02X:%02X:%02X\n",
              props.btaddr[0], props.btaddr[1], props.btaddr[2],
              props.btaddr[3], props.btaddr[4], props.btaddr[5]);
```

#### 2. Allowlist 필터링 기능 추가

**파일: `src/bt_controller.cpp`**
```cpp
void btControllerSetup() {
    // ...
#ifdef ALLOWED_CONTROLLER_MAC
    bd_addr_t allowed = ALLOWED_CONTROLLER_MAC;
    uni_bt_allowlist_remove_all();
    uni_bt_allowlist_add_addr(allowed);
    uni_bt_allowlist_set_enabled(true);
    LOG.printf("[BT] Allowlist enabled for MAC: %02X:%02X:%02X:%02X:%02X:%02X\n",
               allowed[0], allowed[1], allowed[2],
               allowed[3], allowed[4], allowed[5]);
#else
    LOG.println("[BT] Allowlist disabled (any controller can connect)");
#endif
    // ...
}
```

#### 3. config.h에 MAC 주소 설정 옵션 추가

**파일: `src/config.h`**
```cpp
// ============================================
// Bluetooth Controller Filtering (MAC Address Allowlist)
// ============================================
// 보드별 설정:
// - Odin Lift 보드: 리모컨 1 (F4:6A:D7:9A:E0:4A)
// - 다른 ESP32 보드: 리모컨 2 (C0:D6:D5:EF:3D:1E)
#define ALLOWED_CONTROLLER_MAC  {0xF4, 0x6A, 0xD7, 0x9A, 0xE0, 0x4A}
```

### 사용 방법

1. **MAC 주소 확인**: `ALLOWED_CONTROLLER_MAC` 주석 처리 후 빌드/업로드, 컨트롤러 연결 시 시리얼 모니터에서 MAC 확인
2. **필터링 활성화**: `config.h`에 확인된 MAC 주소 설정 후 재빌드/업로드

### 확인된 리모컨 MAC 주소

| 리모컨 | MAC 주소 |
|--------|----------|
| 리모컨 1 | `F4:6A:D7:9A:E0:4A` |
| 리모컨 2 | `C0:D6:D5:EF:3D:1E` |

### 변경 파일

| 파일 | 변경 사항 |
|------|-----------|
| `src/bt_controller.cpp` | allowlist 헤더 추가, MAC 로깅, allowlist 설정 |
| `src/config.h` | `ALLOWED_CONTROLLER_MAC` 설정 옵션 추가 |

### 테스트 결과

- ✅ 컨트롤러 연결 시 MAC 주소 출력
- ✅ 허용된 MAC 주소의 컨트롤러만 연결 성공
- ✅ 다른 컨트롤러 연결 시도 시 무시됨

---

## 2026-01-21: 구형 RF 리모컨 지원 추가 (진행 중)

### 개요

Allturn 구형 RF 리모컨을 ESP32-S3에 연결하여 REMOTE 모드로 로봇 제어 기능 구현.

### 리모컨 프로토콜 사양

| 항목 | 값 |
|------|-----|
| 통신 | UART 38400 baud, 8N1 |
| 방향 | RX only (수신 전용) |
| 프레임 | 4바이트 패턴 매칭 |
| TTL | 150ms (타임아웃 시 정지) |

### 버튼 패턴 매핑

| 패턴 (HEX) | 액션 | 설명 |
|------------|------|------|
| `00 18 00 18` | POWER_ON | REMOTE ↔ NEUTRAL 토글 |
| `00 00 00 00` | ESTOP | 비상정지 → NEUTRAL |
| `01 88 01 88` | FORWARD | 전진 (60% × speedScale) |
| `02 88 02 88` | BACKWARD | 후진 (60% × speedScale) |
| `04 88 04 88` | LEFT | 좌회전 (30% × speedScale) |
| `08 88 08 88` | RIGHT | 우회전 (30% × speedScale) |
| `08 48 08 48` | SPEED_UP | 속도 +10% |
| `04 48 04 48` | SPEED_DOWN | 속도 -10% |

### 모드 우선순위

```
REMOTE > GAMEPAD > ROS2 > NEUTRAL
```

- REMOTE 모드에서는 게임패드/JSON 명령 무시
- 리모컨 power_on 버튼으로 어떤 모드에서든 NEUTRAL로 전환 가능

### 구현 파일

#### 신규 생성

| 파일 | 설명 |
|------|------|
| `src/Allturn_Remote_v2.h` | RF 리모컨 드라이버 헤더 |
| `src/Allturn_Remote_v2.cpp` | UART 수신, 패턴 매칭, 콜백 처리 |

#### 수정

| 파일 | 변경 사항 |
|------|-----------|
| `src/config.h` | RC_RX_PIN(GPIO9), RC_BAUD(38400), RC_TTL_MS(150) 추가 |
| `src/ModeManager.h` | `InputMode::REMOTE` 추가, `enterRemote()`, `toggleByRemoteButton()` |
| `src/ModeManager.cpp` | REMOTE 모드 전환 로직, onJsonReceived에서 REMOTE 체크 |
| `src/rtos/rtos_config.h` | `RemoteCmdData` 구조체, `g_remoteQueue` 추가 |
| `src/rtos/rtos_init.cpp` | `g_remoteQueue` 생성 |
| `src/rtos/bluepad32_task.cpp` | 리모컨 poll/tick 호출, 콜백 등록, 큐 업데이트 |
| `src/rtos/command_task.cpp` | REMOTE 모드 처리 (모터 백분율 직접 전달) |
| `src/sketch.cpp` | `allturn_remote_v2::begin()` 초기화 추가 |
| `src/CMakeLists.txt` | `Allturn_Remote_v2.cpp` 빌드 대상 추가 |

### 핀 설정

```cpp
#define RC_RX_PIN       9       // 리모컨 UART RX (GPIO9)
#define RC_TX_PIN       -1      // TX 미사용 (수신 전용)
#define RC_BAUD         38400   // 리모컨 통신 속도
#define RC_TTL_MS       150     // 명령 타임아웃 (ms)
```

### 빌드 결과

- ✅ 빌드 성공 (RAM: 20.4%, Flash: 8.9%)
- ✅ 펌웨어 업로드 성공

### 현재 상태

- ⚠️ UART 수신 데이터 없음
- 리모컨 보드 측 설정 확인 필요 (TX 출력 활성화 여부)
- GPIO 9 연결 상태 확인 필요

### 디버그 로그 추가

시작 시:
```
[Remote] Setting up Serial2 on RX=GPIO9, baud=38400
[Remote] Serial2 initialized, available=0
[Remote] Ready on GPIO9 @ 38400 baud
```

수신 시 (예상):
```
[Remote] RX: 0x00 (idx=0)
[Remote] RX: 0x18 (idx=1)
[Remote] RX: 0x00 (idx=2)
[Remote] RX: 0x18 (idx=3)
[Remote] Frame: 00 18 00 18
[Remote] POWER_ON pressed
```

### 다음 단계

- [ ] 리모컨 보드 TX 출력 설정 확인
- [ ] GPIO 9 배선 확인 (리모컨 TX → ESP32 RX)
- [ ] 오실로스코프로 신호 확인
- [ ] 다른 GPIO 핀으로 테스트 (GPIO 9가 특수 용도일 경우)

---

## 2026-02-02: FR, RL 휠 회전 방향 버그 수정

### 문제 현상

- 전후진: 정상 동작 ✓
- 제자리 회전: FR, RL 방향이 반대로 회전

### 원인 분석

메카넘 역기구학 수식에서 ORI 보정이 전진/회전 모두에 동일하게 적용되어, 회전 시 FR과 RL 방향이 반전됨.

```cpp
// 기존 수식 (문제)
float FLp = x - y + z;
float FRp = x + y - z;  // 회전(z) 부호 틀림
float RLp = x + y + z;  // 회전(z) 부호 틀림
float RRp = x - y - z;
```

### 해결 방법

**파일: `src/rtos/motor_task.cpp`** (줄 101-104)

```cpp
// 수정된 수식
float FLp = x - y + z;
float FRp = x + y + z;   // 회전 방향 수정: -z → +z
float RLp = x + y - z;   // 회전 방향 수정: +z → -z
float RRp = x - y - z;
```

### 변경 파일

| 파일 | 변경 사항 |
|------|-----------|
| `src/rtos/motor_task.cpp` | FR, RL 역기구학 회전(z) 부호 수정 |

### 테스트 항목

- [ ] 전후진 - 4개 휠 동일 방향 회전 확인
- [ ] 시계 방향 회전 - FL, RR 전진 / FR, RL 후진
- [ ] 반시계 방향 회전 - FR, RL 전진 / FL, RR 후진

---

## 2026-02-04: RF 리모컨 Start 버튼 후 릴레이 꺼짐 문제 해결

### 문제 현상

RF 리모컨의 start(power_on) 버튼을 누르면 릴레이가 켜졌다가 **약 150ms 후에 자동으로 꺼지는 문제**

### 근본 원인

```
1. RF 리모컨 특성: 버튼을 누르고 있는 동안만 신호 전송
2. TTL 타임아웃(150ms): 신호가 없으면 connected = false
3. CommandTask 로직: !remoteData.connected 시 즉시 NEUTRAL 모드 전환 → 릴레이 OFF
```

**기존 흐름:**
```
start 버튼 누름 → REMOTE 모드 → 릴레이 ON
       ↓
버튼에서 손 뗌 → 신호 중단
       ↓ (150ms 후)
TTL 타임아웃 → connected = false
       ↓
CommandTask 감지 → NEUTRAL 전환 → 릴레이 OFF ❌
```

### 해결 방안: 하이브리드 상태 관리

**핵심 아이디어:** "신호 활성 상태"와 "모드 활성(armed) 상태"를 분리

| 상태 | TTL | 역할 | 제어 대상 |
|------|-----|------|----------|
| `signalActive` | 150ms | 신호 수신 여부 | **모터** (정지/동작) |
| `remoteArmed` | 60초 | 모드 활성 상태 | **릴레이** (ON/OFF), 모드 유지 |

**비유:**
- `signalActive` = 무전기로 **말하고 있는 중** (PTT 버튼 누르고 있음)
- `remoteArmed` = 무전기 **전원 ON** (대기 상태, 언제든 통신 가능)

### 구현 내용

#### 1. Allturn_Remote_v2.cpp 수정

```cpp
// 새 상수
static const uint32_t SAFETY_TIMEOUT_MS = 60000;  // 60초 안전 타임아웃

// 하이브리드 상태 관리
static bool signalActive = false;   // 150ms 이내 신호 수신 (모터 제어용)
static bool remoteArmed = false;    // REMOTE 모드 활성 - start 버튼 토글 (릴레이 ON 유지)
```

**POWER_ON 처리 변경 (토글 방식):**
```cpp
case Action::POWER_ON:
    remoteArmed = !remoteArmed;  // 토글
    LOG.printf("[Remote] POWER_ON pressed --> armed=%s\n", remoteArmed ? "true" : "false");
    if (startCallback) startCallback();
    break;
```

**tick() 함수 변경:**
```cpp
void tick() {
    uint32_t now = millis();

    // 1. 신호 활성 TTL 체크 (150ms) - 모터 정지, 릴레이 유지
    if (signalActive && (now - lastRxMs > TTL_MS)) {
        LOG.println("[Remote] Signal TTL timeout - stopping motors (150ms)");
        signalActive = false;
        currentTwist = {0, 0};
        if (twistCallback) twistCallback(currentTwist);
    }

    // 2. 안전 타임아웃 체크 (60초) - armed 해제 → NEUTRAL 전환
    if (remoteArmed && lastRxMs > 0 && (now - lastRxMs > SAFETY_TIMEOUT_MS)) {
        LOG.println("[Remote] Safety timeout - disarming (60s)");
        remoteArmed = false;
        signalActive = false;
        currentTwist = {0, 0};
        if (twistCallback) twistCallback(currentTwist);
    }
}
```

#### 2. Allturn_Remote_v2.h API 추가

```cpp
bool isSignalActive();     // 150ms 이내 신호 수신 여부
bool isArmed();            // REMOTE 모드 활성 여부
void setArmed(bool armed); // 외부에서 armed 상태 설정
```

#### 3. rtos_config.h 구조체 확장

```cpp
struct RemoteCmdData {
    int8_t linPct;
    int8_t turnPct;
    bool powerPressed;
    bool estop;
    bool connected;      // armed 상태 (모드 유지)
    bool signalActive;   // 신호 활성 (모터 제어) ★ 추가
    uint32_t timestamp;
};
```

#### 4. bluepad32_task.cpp 수정

```cpp
remoteQueueData.connected = allturn_remote_v2::isArmed();       // armed 상태
remoteQueueData.signalActive = allturn_remote_v2::isSignalActive(); // 신호 활성
```

### 수정 파일 목록

| 파일 | 변경 사항 |
|------|-----------|
| `src/Allturn_Remote_v2.cpp` | armed 상태 관리, 60초 안전 타임아웃, start 토글 방식 |
| `src/Allturn_Remote_v2.h` | `isSignalActive()`, `isArmed()`, `setArmed()` API 추가 |
| `src/rtos/rtos_config.h` | `RemoteCmdData`에 `signalActive` 필드 추가 |
| `src/rtos/bluepad32_task.cpp` | 새 API 사용 |
| `src/rtos/command_task.cpp` | 디버그 로그 개선 |

### 예상 동작 시나리오

#### 정상 사용
1. start 버튼 누름 → `remoteArmed=true` → REMOTE 모드 → **릴레이 ON**
2. 방향 버튼 누르고 있음 → `signalActive=true` → 모터 동작
3. 방향 버튼 뗌 → 150ms 후 `signalActive=false` → 모터 정지, **릴레이 ON 유지** ✓
4. start 버튼 다시 누름 → `remoteArmed=false` → NEUTRAL → **릴레이 OFF**

#### 리모컨 분실/배터리 방전
1. REMOTE 모드 활성 상태에서 신호 끊김
2. 150ms 후 모터 정지
3. **60초 후 자동으로 NEUTRAL 전환** → 릴레이 OFF (안전 장치)

### 시리얼 로그

```
[Remote] POWER_ON pressed --> armed=true       # start 버튼으로 REMOTE 모드 진입
[Remote] Signal TTL timeout - stopping motors (150ms)  # 버튼 뗀 후 모터만 정지
[Remote] POWER_ON pressed --> armed=false      # start 다시 누르면 NEUTRAL
[Remote] Safety timeout - disarming (60s)      # 60초 무신호 시 안전 해제
```

### 빌드 및 업로드 결과

- ✅ 빌드 성공 (RAM: 20.4%, Flash: 8.9%)
- ✅ 펌웨어 업로드 성공

### 테스트 항목

- [ ] start 버튼 눌러 REMOTE 모드 진입 → 릴레이 ON 확인
- [ ] 버튼에서 손 뗀 후 릴레이가 **계속 ON인지** 확인
- [ ] 방향 버튼 테스트 (누르면 이동, 떼면 정지)
- [ ] start 버튼 다시 눌러 NEUTRAL 전환 확인
- [ ] 60초 무신호 후 자동 NEUTRAL 전환 확인

---

## 2026-02-04: RF 리모컨 속도 상한 조절 기능 추가

### 개요

RF 리모컨의 SPEED_UP/SPEED_DOWN 버튼으로 최대 속도 상한 조절 기능 구현.

### 동작 방식

```
[기존]
전진 버튼 → linPct = 36% (고정) → motor_task ramp → 실제 RPM

[변경 후]
SPEED_UP → maxSpeedPct = 75% (상한 증가)
전진 버튼 → linPct = 45% (60% × 75%) → motor_task ramp → 더 높은 RPM
```

### 버튼 매핑

| 패턴 (HEX) | 액션 | 설명 |
|------------|------|------|
| `08 48 08 48` | SPEED_UP | 최대 속도 +15% |
| `04 48 04 48` | SPEED_DOWN | 최대 속도 -15% |

### 속도 설정

| 항목 | 값 |
|------|-----|
| 기본 최대 속도 | 60% |
| 증감 단위 | 15% |
| 최소값 | 15% |
| 최대값 | 100% |
| 디바운싱 | 150ms |

### 구현 내용

#### Allturn_Remote_v2.h
- `Action` 열거형에 `SPEED_UP`, `SPEED_DOWN` 추가

#### Allturn_Remote_v2.cpp
- 상수: `SPEED_STEP=15`, `MIN_SPEED_PCT=15`, `DEFAULT_MAX_SPEED=60`, `SPEED_DEBOUNCE_MS=150`
- 상태 변수: `speedScale` → `maxSpeedPct` (int8_t)
- 패턴: `PATTERN_SPEED_UP`, `PATTERN_SPEED_DOWN` 추가
- 이동 명령: `BASE_PCT * maxSpeedPct / 100` 으로 목표 속도 계산
- SPEED_UP/DOWN: 150ms 디바운싱 적용, maxSpeedPct만 변경

### 변경 파일

| 파일 | 변경 사항 |
|------|-----------|
| `src/Allturn_Remote_v2.h` | `SPEED_UP`, `SPEED_DOWN` 액션 추가 |
| `src/Allturn_Remote_v2.cpp` | 속도 상한 조절 로직, 패턴 매칭, 디바운싱 |

### 빌드 및 업로드 결과

- ✅ 빌드 성공 (RAM: 20.4%, Flash: 8.9%)
- ✅ 펌웨어 업로드 성공

### 테스트 항목

- [ ] 전진 버튼 → `linPct=36` (60% × 60%) 확인
- [ ] SPEED_UP 1회 → `maxSpeed=75%` 로그 확인
- [ ] 전진 버튼 → `linPct=45` (60% × 75%) 확인
- [ ] SPEED_DOWN 2회 → `maxSpeed=45%` 로그 확인
