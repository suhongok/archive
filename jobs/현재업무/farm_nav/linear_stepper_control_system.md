# 리니어 스테퍼 모터 제어 시스템 구성

## 1. 개요

Jetson Orin Nano를 상위 컨트롤러로 사용하여 4축 리니어 스테퍼 모터를 독립적으로 위치 제어하는 시스템 구성.

### 시스템 구성도

```
Jetson Orin Nano (상위 컨트롤러)
        │
       USB (시리얼 통신)
        │
BTT SKR 3 EZ (모션 컨트롤러)
        │
     SPI (온보드)
        │
┌───────┼───────┬───────┬───────┐
│       │       │       │       │
EZ5160  EZ5160  EZ5160  EZ5160
Pro     Pro     Pro     Pro
│       │       │       │
M1      M2      M3      M4
(리니어 스테퍼 x4)
```

---

## 2. 하드웨어 구성

### 2.1 리니어 스테퍼 모터

**모델: LSM4-NK235630-1610**

| 항목 | 사양 |
|------|------|
| 유효 스트로크 | 100~1500mm (선택) |
| 스크류 직경 | φ16mm |
| 리드 | 10mm |
| 스피드 | 100mm/sec |
| 부하 | 수평 40kg, 수직 30kg |
| 스크류 정밀도 | 0.03mm |
| 모터 사이즈 | 57×56mm (NEMA23) |
| 홀딩 토크 | 1.2Nm |
| **모터 전류** | **3A** |

### 2.2 모션 컨트롤러

**BIGTREETECH SKR 3 EZ**

| 항목 | 사양 |
|------|------|
| MCU | STM32H723VGT6 (32-bit ARM Cortex-M7) |
| 드라이버 슬롯 | 5개 (EZ 타입) |
| 입력 전압 | DC 12-24V |
| 통신 | USB, UART, CAN |
| 특징 | 온보드 DIAG 기능, 교체형 퓨즈 |

### 2.3 스테퍼 드라이버

**BIGTREETECH EZ5160 Pro**

| 항목 | 사양 |
|------|------|
| 칩셋 | TMC5160 |
| 최대 전류 | 3A (피크 4.4A) |
| 통신 | SPI |
| 마이크로스텝 | 최대 256 |
| 특징 | StallGuard (센서리스 홈잉), StealthChop, SpreadCycle |

**모터 전류 3A에 EZ5160 Pro 적합** ✅

### 2.4 상위 컨트롤러

**NVIDIA Jetson Orin Nano**

- Klipper 호스트 실행
- USB로 SKR 3 EZ와 통신
- Python API로 모터 제어 명령 전송

---

## 3. 핵심 기능

### 3.1 StallGuard를 이용한 끝단 감지

리미트 스위치 없이 모터 스톨(막힘)을 감지하여 끝단 도달 확인.

**원리:**
- TMC5160이 Back-EMF 패턴 분석
- 이동체가 끝단에 도달하면 SG_RESULT 값 급감
- DIAG 핀 신호 출력 → 홈잉 완료

**장점:**
- 리미트 스위치 배선 불필요
- 센서 고장 위험 없음
- 깔끔한 배선

### 3.2 4축 독립 위치 제어

Klipper의 `manual_stepper` 기능으로 각 모터 개별 제어.

---

## 4. 소프트웨어 구성

### 4.1 펌웨어

**Klipper** (SKR 3 EZ에 설치)

- 실시간 모션 제어
- TMC5160 SPI 통신 지원
- StallGuard/sensorless homing 지원

### 4.2 Klipper 설정 (printer.cfg)

```ini
# ========================================
# SKR 3 EZ + EZ5160 Pro x4 설정
# ========================================

[mcu]
serial: /dev/ttyACM0

[printer]
kinematics: none
max_velocity: 300
max_accel: 1000

# ----------------------------------------
# Motor 1
# ----------------------------------------
[manual_stepper motor1]
step_pin: PD4
dir_pin: PD3
enable_pin: !PD6
microsteps: 16
rotation_distance: 10  # 리드 10mm
velocity: 100          # mm/s
accel: 500

[tmc5160 manual_stepper motor1]
cs_pin: PD5
spi_software_miso_pin: PA6
spi_software_mosi_pin: PA7
spi_software_sclk_pin: PA5
run_current: 2.5
diag1_pin: ^!PC1
driver_SGT: 50

# ----------------------------------------
# Motor 2
# ----------------------------------------
[manual_stepper motor2]
step_pin: PA15
dir_pin: PA8
enable_pin: !PD1
microsteps: 16
rotation_distance: 10
velocity: 100
accel: 500

[tmc5160 manual_stepper motor2]
cs_pin: PD0
spi_software_miso_pin: PA6
spi_software_mosi_pin: PA7
spi_software_sclk_pin: PA5
run_current: 2.5
diag1_pin: ^!PC3
driver_SGT: 50

# ----------------------------------------
# Motor 3
# ----------------------------------------
[manual_stepper motor3]
step_pin: PE2
dir_pin: PE3
enable_pin: !PE0
microsteps: 16
rotation_distance: 10
velocity: 100
accel: 500

[tmc5160 manual_stepper motor3]
cs_pin: PE1
spi_software_miso_pin: PA6
spi_software_mosi_pin: PA7
spi_software_sclk_pin: PA5
run_current: 2.5
diag1_pin: ^!PC0
driver_SGT: 50

# ----------------------------------------
# Motor 4
# ----------------------------------------
[manual_stepper motor4]
step_pin: PD15
dir_pin: PD14
enable_pin: !PC7
microsteps: 16
rotation_distance: 10
velocity: 100
accel: 500

[tmc5160 manual_stepper motor4]
cs_pin: PC6
spi_software_miso_pin: PA6
spi_software_mosi_pin: PA7
spi_software_sclk_pin: PA5
run_current: 2.5
diag1_pin: ^!PA0
driver_SGT: 50

# ----------------------------------------
# Sensorless Homing 매크로
# ----------------------------------------
[gcode_macro HOME_MOTOR1]
gcode:
    MANUAL_STEPPER STEPPER=motor1 SET_POSITION=0
    MANUAL_STEPPER STEPPER=motor1 MOVE=-500 SPEED=50 STOP_ON_ENDSTOP=1
    MANUAL_STEPPER STEPPER=motor1 SET_POSITION=0

[gcode_macro HOME_MOTOR2]
gcode:
    MANUAL_STEPPER STEPPER=motor2 SET_POSITION=0
    MANUAL_STEPPER STEPPER=motor2 MOVE=-500 SPEED=50 STOP_ON_ENDSTOP=1
    MANUAL_STEPPER STEPPER=motor2 SET_POSITION=0

[gcode_macro HOME_MOTOR3]
gcode:
    MANUAL_STEPPER STEPPER=motor3 SET_POSITION=0
    MANUAL_STEPPER STEPPER=motor3 MOVE=-500 SPEED=50 STOP_ON_ENDSTOP=1
    MANUAL_STEPPER STEPPER=motor3 SET_POSITION=0

[gcode_macro HOME_MOTOR4]
gcode:
    MANUAL_STEPPER STEPPER=motor4 SET_POSITION=0
    MANUAL_STEPPER STEPPER=motor4 MOVE=-500 SPEED=50 STOP_ON_ENDSTOP=1
    MANUAL_STEPPER STEPPER=motor4 SET_POSITION=0

[gcode_macro HOME_ALL]
gcode:
    HOME_MOTOR1
    HOME_MOTOR2
    HOME_MOTOR3
    HOME_MOTOR4

# ----------------------------------------
# 동시 이동 매크로
# ----------------------------------------
[gcode_macro MOVE_ALL]
gcode:
    {% set m1 = params.M1|default(0)|float %}
    {% set m2 = params.M2|default(0)|float %}
    {% set m3 = params.M3|default(0)|float %}
    {% set m4 = params.M4|default(0)|float %}
    {% set speed = params.SPEED|default(100)|float %}
    
    MANUAL_STEPPER STEPPER=motor1 MOVE={m1} SPEED={speed} SYNC=0
    MANUAL_STEPPER STEPPER=motor2 MOVE={m2} SPEED={speed} SYNC=0
    MANUAL_STEPPER STEPPER=motor3 MOVE={m3} SPEED={speed} SYNC=0
    MANUAL_STEPPER STEPPER=motor4 MOVE={m4} SPEED={speed} SYNC=1
```

### 4.3 G-code 명령어

```gcode
# 개별 모터 이동
MANUAL_STEPPER STEPPER=motor1 MOVE=150        # 150mm 절대위치
MANUAL_STEPPER STEPPER=motor2 MOVE=200 SPEED=50  # 속도 지정

# 홈잉
HOME_MOTOR1
HOME_ALL

# 4축 동시 이동
MOVE_ALL M1=100 M2=150 M3=200 M4=50 SPEED=80

# 현재 위치 설정
MANUAL_STEPPER STEPPER=motor1 SET_POSITION=0
```

### 4.4 Jetson Orin Nano Python 제어

```python
#!/usr/bin/env python3
"""
Jetson Orin Nano에서 리니어 스테퍼 제어
Moonraker API 사용
"""

import requests
import time

MOONRAKER_URL = "http://localhost:7125"

def send_gcode(cmd: str):
    """G-code 명령 전송"""
    url = f"{MOONRAKER_URL}/printer/gcode/script"
    response = requests.post(url, json={"script": cmd})
    return response.json()

def move_motor(motor_id: int, position: float, speed: float = 100):
    """개별 모터 이동"""
    cmd = f"MANUAL_STEPPER STEPPER=motor{motor_id} MOVE={position} SPEED={speed}"
    return send_gcode(cmd)

def move_all(m1: float, m2: float, m3: float, m4: float, speed: float = 100):
    """4축 동시 이동"""
    cmd = f"MOVE_ALL M1={m1} M2={m2} M3={m3} M4={m4} SPEED={speed}"
    return send_gcode(cmd)

def home_motor(motor_id: int):
    """개별 모터 홈잉"""
    cmd = f"HOME_MOTOR{motor_id}"
    return send_gcode(cmd)

def home_all():
    """전체 홈잉"""
    return send_gcode("HOME_ALL")

# 사용 예시
if __name__ == "__main__":
    # 전체 홈잉
    home_all()
    time.sleep(5)
    
    # 개별 이동
    move_motor(1, 100)
    move_motor(2, 150)
    
    # 동시 이동
    move_all(200, 200, 200, 200, speed=80)
```

---

## 5. 하드웨어 연결

### 5.1 전원

```
24V PSU
   │
   ├── SKR 3 EZ (메인 전원)
   │
   └── 모터 전원 (EZ5160 Pro 통해 공급)
```

**권장 전원:** 24V, 10A 이상

### 5.2 드라이버 장착

SKR 3 EZ의 EZ 드라이버 슬롯에 EZ5160 Pro 장착:

| 슬롯 | 드라이버 | 모터 |
|------|----------|------|
| X | EZ5160 Pro | Motor 1 |
| Y | EZ5160 Pro | Motor 2 |
| Z | EZ5160 Pro | Motor 3 |
| E0 | EZ5160 Pro | Motor 4 |

### 5.3 모터 배선

4핀 스테퍼 모터 케이블 연결:
- A+, A- (코일 1)
- B+, B- (코일 2)

---

## 6. 설정 및 튜닝

### 6.1 전류 설정

```ini
run_current: 2.5  # 정격 3A의 약 80%
```

발열 상황 보고 조정. 방열판 필수.

### 6.2 StallGuard 튜닝

```ini
driver_SGT: 50  # 기본값
```

- 값이 높으면: 민감도 낮음 (늦게 감지)
- 값이 낮으면: 민감도 높음 (일찍 감지, 오감지 가능)

테스트 후 적절한 값 찾기.

### 6.3 가감속 설정

```ini
velocity: 100   # 최대 속도 mm/s
accel: 500      # 가속도 mm/s²
```

부하에 따라 조정.

---

## 7. BOM (부품 목록)

| 품목 | 수량 | 비고 |
|------|------|------|
| LSM4-NK235630-1610 | 4 | 리니어 스테퍼 모터 |
| BTT SKR 3 EZ | 1 | 모션 컨트롤러 |
| BTT EZ5160 Pro | 4 | 스테퍼 드라이버 |
| Jetson Orin Nano | 1 | 상위 컨트롤러 |
| 24V PSU (10A+) | 1 | 전원 공급 |
| USB 케이블 | 1 | Jetson-SKR 연결 |
| 모터 케이블 | 4 | 4핀 스테퍼 케이블 |

---

## 8. 참고사항

### 8.1 장점

- **센서리스 홈잉**: 리미트 스위치 없이 끝단 감지
- **간단한 배선**: USB 하나로 상위 연결
- **확장성**: 드라이버 슬롯 여유 있음
- **검증된 조합**: BTT 생태계 호환성 보장

### 8.2 주의사항

- EZ5160 Pro 방열판 필수 (3A 연속 구동 시)
- StallGuard는 일정 속도 이상에서만 정확함 (홈잉 시 50mm/s 권장)
- printer.cfg 핀 배열은 실제 보드 확인 후 수정 필요

---

## 9. 변경 이력

| 날짜 | 내용 |
|------|------|
| 2025-01-31 | 초기 문서 작성 |
