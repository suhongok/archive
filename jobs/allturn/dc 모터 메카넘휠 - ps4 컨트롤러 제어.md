# dc 모터 메카넘휠 - ps4 컨트롤러 제어

> **생성일:** 2025-12-09T06:07:00.000Z
> **수정일:** 2025-12-19T03:06:00.000Z

오늘 진행한 프로젝트 내용을 노션(Notion)에 바로 복사해서 붙여넣을 수 있도록 깔끔하게 정리해 드립니다.
---

# 🚗 ESP32 메카넘 휠 로봇 개발 일지 (PS4 컨트롤러)

날짜: 2024년 12월 09일
주요 하드웨어: ESP32, DC 모터 드라이버(4채널), 메카넘 휠, PS4 호환 컨트롤러
라이브러리: Bluepad32
## 1. 하드웨어 핀 맵 (Pinout)

ESP32와 모터 드라이버 연결 구성입니다.

> Note: 25번 핀은 DAC 핀이지만 디지털 PWM 출력으로 사용함.
---

## 2. 주요 구현 기능 (Key Features)

오늘 개발 및 테스트를 완료한 기능 목록입니다.
### ✅ 1. 전방향 이동 (Omnidirectional Movement)

- 메카넘 키네마틱스 적용: 벡터 합산을 통해 전진, 후진, 좌우 평행이동, 대각선 이동 구현.
- 부드러운 주행 (Ramping): lerp 함수를 사용하여 급출발/급정지를 방지하고 움직임을 부드럽게 처리.
### ✅ 2. PS4 컨트롤러 연동

- Bluepad32 라이브러리: 별도의 동글 없이 ESP32 블루투스로 직접 페어링.
- 자동 재연결: forgetBluetoothKeys() 및 페어링 로직 최적화.
### ✅ 3. 사용자 편의 기능 (Advanced Control)

- 버튼 회전: 스틱 조작 없이 버튼만으로 정확한 제자리 회전 가능.
- 크루즈 컨트롤 (Cruise Control):
- 속도 미세 조정 (Trim):
---

## 3. 조작 매뉴얼 (User Manual)


---

## 4. 핵심 코드 로직 (Snippet)

크루즈 컨트롤의 안정성을 높여준 1초 잠금(Lock Delay) 로직입니다.
C++
// 크루즈 켜기 (세모 버튼)
if (btnTriangle && !lastTriangleState) {
    if (!isCruiseMode) {
        isCruiseMode = true;
        cruiseTwist = currentTwist; // 현재 속도 저장
        cruiseStartTime = millis(); // 시작 시간 기록 (잠금 시작)
        ctl->setColorLED(255, 0, 255); // 보라색 LED
    }
    // ... (OFF 로직)
}

// 해제 조건 검사
bool isLocked = (millis() - cruiseStartTime < 1000); // 1초 지났는지 확인

if (isCruiseMode && !isLocked) {
    // 1초가 지난 후에만 스틱 입력으로 크루즈 해제 가능
    if (isStickMoved || btnSquare || btnCircle) {
        isCruiseMode = false;
        // ...
    }
}
---

---

### 코드

```c++
#include <Arduino.h>
#include <Bluepad32.h>

// ================= 핀 정의 =================
const int PIN_ENABLE = 15;

// FL
const int FL_FWD = 16; const int FL_BWD = 17;
// FR
const int FR_FWD = 18; const int FR_BWD = 19;
// RL
const int RL_FWD = 21; const int RL_BWD = 22;
// RR
const int RR_FWD = 23; const int RR_BWD = 25;

// ================= PWM 설정 =================
const int PWM_FREQ = 30000;
const int PWM_RES = 8;
const int MAX_PWM = 255;

const int CH_FL_F = 0; const int CH_FL_B = 1;
const int CH_FR_F = 2; const int CH_FR_B = 3;
const int CH_RL_F = 4; const int CH_RL_B = 5;
const int CH_RR_F = 6; const int CH_RR_B = 7;

// ================= 제어 변수 =================
struct Twist {
  float linear_x;
  float linear_y;
  float angular_z;
};

Twist targetTwist = {0, 0, 0};
Twist currentTwist = {0, 0, 0};
Twist cruiseTwist = {0, 0, 0};

bool isCruiseMode = false;
bool lastTriangleState = false;

// 크루즈 잠금 및 속도 조절 변수
unsigned long cruiseStartTime = 0;
const int CRUISE_LOCK_DURATION = 1000; // 1초 잠금

const int DEADZONE = 40;
const float ACCEL_STEP = 0.05;

ControllerPtr myControllers[BP32_MAX_GAMEPADS];

// 함수 선언
void processControllers();
void driveMecanum(float x, float y, float z);
void setSingleMotor(int ch_fwd, int ch_bwd, int speed);
void setupMotorPin(int pin, int channel);
float lerp(float start, float end, float amt);

void setup() {
  Serial.begin(115200);
  Serial.println("PS4 Mecanum: Cruise Speed Control (L1/L2)");

  pinMode(PIN_ENABLE, OUTPUT);
  digitalWrite(PIN_ENABLE, HIGH);

  setupMotorPin(FL_FWD, CH_FL_F); setupMotorPin(FL_BWD, CH_FL_B);
  setupMotorPin(FR_FWD, CH_FR_F); setupMotorPin(FR_BWD, CH_FR_B);
  setupMotorPin(RL_FWD, CH_RL_F); setupMotorPin(RL_BWD, CH_RL_B);
  setupMotorPin(RR_FWD, CH_RR_F); setupMotorPin(RR_BWD, CH_RR_B);

  BP32.setup(&onConnectedController, &onDisconnectedController);
  BP32.forgetBluetoothKeys(); 
}

void loop() {
  bool dataUpdated = BP32.update();
  
  if (dataUpdated) {
    processControllers();
  }

  // 부드러운 가속 (Ramping)
  currentTwist.linear_x = lerp(currentTwist.linear_x, targetTwist.linear_x, ACCEL_STEP);
  currentTwist.linear_y = lerp(currentTwist.linear_y, targetTwist.linear_y, ACCEL_STEP);
  currentTwist.angular_z = lerp(currentTwist.angular_z, targetTwist.angular_z, ACCEL_STEP);

  driveMecanum(currentTwist.linear_x, currentTwist.linear_y, currentTwist.angular_z);
  delay(10);
}

// ================= 컨트롤러 로직 =================
void processControllers() {
  bool controllerFound = false;

  for (auto ctl : myControllers) {
    if (ctl && ctl->isConnected() && ctl->hasData()) {
      controllerFound = true;
      
      // 1. 입력 값 읽기
      int lx = ctl->axisX();
      int ly = ctl->axisY();
      int rx = ctl->axisRX();
      
      bool btnSquare = ctl->x();  
      bool btnCircle = ctl->b();  
      bool btnTriangle = ctl->y();
      
      // L1 버튼 (감속용)
      bool btnL1 = ctl->l1();
      // L2 트리거 (가속용) - Bluepad32에서 brake()는 L2 아날로그 값(0~1023)
      bool btnL2 = (ctl->brake() > 50); 

      bool isStickMoved = (abs(lx) > DEADZONE || abs(ly) > DEADZONE || abs(rx) > DEADZONE);

      // --- [크루즈 ON/OFF 로직] ---

      if (btnTriangle && !lastTriangleState) {
        if (!isCruiseMode) {
          isCruiseMode = true;
          cruiseTwist = currentTwist; 
          cruiseStartTime = millis(); 
          ctl->setColorLED(255, 0, 255); // 보라색
          Serial.println("Cruise ON");
        } else {
          isCruiseMode = false;
          ctl->setColorLED(0, 255, 0); // 초록색
          Serial.println("Cruise OFF");
        }
      }
      lastTriangleState = btnTriangle;

      // --- [크루즈 해제 및 속도 조절] ---
      
      bool isLocked = (millis() - cruiseStartTime < CRUISE_LOCK_DURATION);

      if (isCruiseMode) {
        // [속도 조절] L1: 감속, L2: 가속
        // 현재 벡터에 비율을 곱해서 속도 조절
        if (btnL1) {
          // 감속: 매 루프마다 2%씩 감소
          cruiseTwist.linear_x *= 0.98;
          cruiseTwist.linear_y *= 0.98;
          cruiseTwist.angular_z *= 0.98;
        } 
        else if (btnL2) {
          // 가속: 매 루프마다 2%씩 증가
          cruiseTwist.linear_x *= 1.02;
          cruiseTwist.linear_y *= 1.02;
          cruiseTwist.angular_z *= 1.02;
        }

        // 속도가 너무 커지지 않게 제한 (최대 2.0배수 정도까지만 허용하고 나중에 잘림)
        float mag = sqrt(sq(cruiseTwist.linear_x) + sq(cruiseTwist.linear_y));
        if (mag > 2.5) { 
           cruiseTwist.linear_x *= 0.95;
           cruiseTwist.linear_y *= 0.95;
        }

        // [해제 조건] 잠금 시간 지난 후 스틱/회전버튼 개입 시
        if (!isLocked) {
          if (isStickMoved || btnSquare || btnCircle) {
            isCruiseMode = false;
            ctl->setColorLED(0, 255, 0); 
            Serial.println("Cruise Cancelled");
          }
        }
        
        targetTwist = cruiseTwist;
      } 
      else {
        // [일반 모드]
        if (!isStickMoved) { lx = 0; ly = 0; rx = 0; }

        float lin_x = -ly / 512.0f; 
        float lin_y = lx / 512.0f;  
        float ang_z = rx / 512.0f;  

        if (btnSquare) ang_z = -0.8f;      
        else if (btnCircle) ang_z = 0.8f; 

        targetTwist.linear_x = lin_x;
        targetTwist.linear_y = lin_y;
        targetTwist.angular_z = ang_z;

        float throttle = ctl->throttle(); 
        float speedScale = 0.5f + (throttle / 2048.0f); 

        targetTwist.linear_x *= speedScale;
        targetTwist.linear_y *= speedScale;
        targetTwist.angular_z *= speedScale;
      }
      
      return; 
    }
  }

  if (!controllerFound) {
    targetTwist = {0, 0, 0};
    isCruiseMode = false;
  }
}

void driveMecanum(float x, float y, float z) {
  float fl = x + y + z;
  float fr = x - y - z;
  float rl = x - y + z;
  float rr = x + y - z;

  float maxVal = max(abs(fl), max(abs(fr), max(abs(rl), abs(rr))));
  if (maxVal > 1.0) {
    fl /= maxVal; fr /= maxVal; rl /= maxVal; rr /= maxVal;
  }

  setSingleMotor(CH_FL_F, CH_FL_B, fl * MAX_PWM);
  setSingleMotor(CH_FR_F, CH_FR_B, fr * MAX_PWM);
  setSingleMotor(CH_RL_F, CH_RL_B, rl * MAX_PWM);
  setSingleMotor(CH_RR_F, CH_RR_B, rr * MAX_PWM);
}

float lerp(float start, float end, float amt) {
  return start + (end - start) * amt;
}

void setupMotorPin(int pin, int channel) {
  ledcSetup(channel, PWM_FREQ, PWM_RES);
  ledcAttachPin(pin, channel);
}

void setSingleMotor(int ch_fwd, int ch_bwd, int speed) {
  if (speed > 0) {
    ledcWrite(ch_fwd, speed);
    ledcWrite(ch_bwd, 0);
  } else if (speed < 0) {
    ledcWrite(ch_fwd, 0);
    ledcWrite(ch_bwd, abs(speed));
  } else {
    ledcWrite(ch_fwd, 0);
    ledcWrite(ch_bwd, 0);
  }
}

void onConnectedController(ControllerPtr ctl) {
  for (int i = 0; i < BP32_MAX_GAMEPADS; i++) {
    if (myControllers[i] == nullptr) {
      myControllers[i] = ctl;
      ctl->setColorLED(0, 255, 0); 
      return;
    }
  }
}

void onDisconnectedController(ControllerPtr ctl) {
  for (int i = 0; i < BP32_MAX_GAMEPADS; i++) {
    if (myControllers[i] == ctl) {
      myControllers[i] = nullptr;
      return;
    }
  }
}
```