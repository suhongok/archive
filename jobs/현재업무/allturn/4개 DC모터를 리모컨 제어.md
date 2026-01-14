# 4개 DC모터를 리모컨 제어

> **생성일:** 2025-10-13T01:46:00.000Z
> **수정일:** 2025-10-20T04:55:00.000Z

### 개념: 4개의 DC모터를 릴레이로 제어

### 기능: 

전진(4개 바퀴동작: 전진,전진,전진,전진), 후진(후진,후진,후진,후진), 방향전환_제자리(전진, 후진, 전진, 후진), 방향전환_한쪽(전진,전진, 정지,정지), 속도 증감(60,75,100).
### 구현: 

리모컨 신호 전송→리모컨 수신릴레이신호 전송(8개 핀)→아두이노→모터 드라이버→DC모터
### 세부 기능:

방향:
1. 전진: 4개의 바퀴 모두 시계방향회전
1. 후진: 4개의 바퀴 모두 반시계방향회전
1. 제자리회전: 좌측 또는 우측 바퀴는 시계방향회전 동시에, 우측또는 좌측 바퀴가 반시계방향회전
1. 한쪽회전: 좌측 또는 우측 바퀴가 시계방향회전 동시에, 반대편은 정지
1. 슬로우 스타터 스탑 기능: 서서히 가속, 서서히 감속
릴레이 버튼 총 6개 입력받음.
1. 전진
1. 후진
1. 제자리회전(좌,우)
1. 한쪽회전(좌,우)
1. 속도변경(상,하)
### 하드웨어

1. 아두이노 우노 사용
1. 모터 드라이버: HC-160A S2
1. DC모터 24V 1A 모터 4개
1. 단점: 한쪽의 모터만 사용가능함.
# ⚙️ 아두이노 기반 2채널 DC모터 제어 시스템 (릴레이 입력 + PWM 제어)

## 📘 프로젝트 개요

- 목표:
- 하드웨어 환경:

---

## 🧩 주요 기능 요약


---

## 🔌 하드웨어 연결 요약

### 🔹 입력 핀


> ✅ 모든 입력핀은 pinMode(pin, INPUT) + 외부 10 kΩ 풀업 저항 사용
> 내부 INPUT_PULLUP 비활성화 상태
---

### 🔹 출력 핀 및 드라이버 연결


> ⚠️ 각 드라이버의 5 V 입력 및 GND는 Arduino와
> ⚠️ 24 V 전원은 각 드라이버에 별도 공급 (병렬 연결 가능) - 24v배터리 사용
---

## 🧠 개발 및 디버깅 히스토리


---

## 📊 테스트 및 보조 코드

1. 릴레이 입력 테스트 코드 → 각 버튼 입력 상태를 시리얼 출력
1. 전압 모니터링 코드 → A0/A1 실시간 전압 출력 (분압 보정 지원)
1. 모터 채널 자가진단 코드 → 각 채널의 PWM / DIR 조합을 자동 시퀀스로 검증
> 모든 테스트에서
> 드라이버 #2 (ab 채널) 미동작 시 5 V 입력 공급 및 배선 위치 재확인
---

## ✅ 현재 구성 상태

- 좌측 / 우측 모터 모두 정상 동작
- 입력 3.9 V 신호 안정화 완료
- 가속/감속 부드럽게 동작
- 코드 최종 버전에서 자동 감속 + 정지 기능 확립
---

## 🪜 다음 단계

1. Node-RED 대시보드 연동 (속도 조절 및 상태 시각화)
1. 감속곡선 세분화 – RAMP_DOWN_STEP = 2 로 더 부드럽게
1. 드라이버 입력 5 V 및 GND 라인 확실한 공통 결선 정리
1. 모터 제어 상태 (전류 / 전압 / PWM Duty) 로그 기록 기능 추가
---

## 📎 프로그램 코드 첨부 (별도)

> 아래에 아두이노 최종 코드를 붙여넣으세요.
```plain text
// Arduino DC motor control (좌/우 독립형)
/*
  2채널(좌/우) DC모터 제어 - 단일 PWM + 방향 A/B 드라이버용 (개선버전)
  - 감속 시 DIR 유지, PWM이 0이 되면 DIR=0으로 정지
  - 버튼을 떼면 자동 감속 및 정지
*/

#include <Arduino.h>

// ===== 설정 =====
#define ACTIVE_LOW_INPUT 0
const uint8_t SPEEDS[] = {50, 70, 90};
const uint8_t N_SPEEDS = sizeof(SPEEDS)/sizeof(SPEEDS[0]);

const uint8_t RAMP_UP_STEP = 4;      // 가속 시 변화량
const uint8_t RAMP_DOWN_STEP = 4;    // 감속 시 변화량
const uint16_t RAMP_INTERVAL_MS = 20;

// ===== 핀맵 (UNO 예시) =====
const uint8_t PIN_PWM_L  = 3;
const uint8_t PIN_DIRA_L = 4;
const uint8_t PIN_DIRB_L = 2;
const uint8_t PIN_PWM_R  = 5;
const uint8_t PIN_DIRA_R = 6;
const uint8_t PIN_DIRB_R = 7;

// 릴레이 입력 6 + 속도 상/하 2 = 8개
const uint8_t PIN_IN_FW      = 8;
const uint8_t PIN_IN_BW      = 9;
const uint8_t PIN_IN_SPOT_L  = 10;
const uint8_t PIN_IN_SPOT_R  = 11;
const uint8_t PIN_IN_PIVOT_L = 12;
const uint8_t PIN_IN_PIVOT_R = 13;
const uint8_t PIN_IN_SPD_UP  = A0;
const uint8_t PIN_IN_SPD_DN  = A1;

// 회전 방향 반전 설정
bool INVERT_LEFT  = false;
bool INVERT_RIGHT = false;

// ===== 내부 상태 =====
enum Motion { STOP=0, FWD, BWD, SPOT_L, SPOT_R, PIVOT_L, PIVOT_R };
struct Channel { int8_t dir; uint8_t cur; uint8_t tgt; };

uint8_t speed_idx=0;
Motion motion=STOP;
Channel L{0,0,0}, R{0,0,0};

struct Button { uint8_t pin; bool last; uint32_t t; } btns[8];

// ===== 함수 =====
bool rawRead(uint8_t pin){
#if ACTIVE_LOW_INPUT
  return digitalRead(pin)==LOW;   // 액티브-LOW: 눌리면 GND
#else
  return digitalRead(pin)==HIGH;
#endif
}

bool edgePressed(Button &b, uint16_t debounce=30){
  bool now = rawRead(b.pin);
  uint32_t tnow = millis();
  if(now!=b.last && (tnow-b.t)>debounce){
    b.last = now;
    b.t = tnow;
    if(now) return true;
  }
  return false;
}

uint8_t pct2pwm(uint8_t p){ if(p>100) p=100; return (uint8_t)round(255.0*(p/100.0)); }

uint8_t ramp(uint8_t cur, uint8_t tgt){
  if(cur == tgt) return cur;
  if(cur < tgt){
    uint16_t inc = cur + RAMP_UP_STEP;
    return (inc > tgt) ? tgt : (uint8_t)inc;
  }else{
    uint16_t dec = (cur > RAMP_DOWN_STEP) ? cur - RAMP_DOWN_STEP : 0;
    return (dec < tgt) ? tgt : (uint8_t)dec;
  }
}

// 단일 PWM + DIR_A/B 출력
void applyAB(uint8_t pwmPin, uint8_t aPin, uint8_t bPin, int8_t dir, uint8_t pwm, bool invert){
  int8_t d = invert ? -dir : dir;
  if      (d > 0){ digitalWrite(aPin, HIGH); digitalWrite(bPin, LOW); }
  else if (d < 0){ digitalWrite(aPin, LOW);  digitalWrite(bPin, HIGH); }
  else           { digitalWrite(aPin, HIGH); digitalWrite(bPin, HIGH); } // 프리런 모드
  analogWrite(pwmPin, pwm);
}

// 동작 설정
void computeTargets(Motion m, uint8_t sp){
  uint8_t pwm = pct2pwm(sp);
  switch(m){
    case FWD:     L.dir=+1; L.tgt=pwm; R.dir=+1; R.tgt=pwm; break;
    case BWD:     L.dir=-1; L.tgt=pwm; R.dir=-1; R.tgt=pwm; break;
    case SPOT_L:  L.dir=-1; L.tgt=pwm; R.dir=+1; R.tgt=pwm; break;
    case SPOT_R:  L.dir=+1; L.tgt=pwm; R.dir=-1; R.tgt=pwm; break;
    case PIVOT_L: L.dir=0;  L.tgt=0;   R.dir=+1; R.tgt=pwm; break;
    case PIVOT_R: L.dir=+1; L.tgt=pwm; R.dir=0;  R.tgt=0;   break;
    case STOP:    L.tgt=0;  R.tgt=0;   break;
  }
}

// ===== setup =====
void setupInputs(){
  uint8_t pins[8]={PIN_IN_FW,PIN_IN_BW,PIN_IN_SPOT_L,PIN_IN_SPOT_R,
                   PIN_IN_PIVOT_L,PIN_IN_PIVOT_R,PIN_IN_SPD_UP,PIN_IN_SPD_DN};
  for(int i=0;i<8;i++){
    pinMode(pins[i], INPUT);
    btns[i] = {pins[i], rawRead(pins[i]), millis()};
  }
}
void setupOutputs(){
  pinMode(PIN_PWM_L,OUTPUT); pinMode(PIN_DIRA_L,OUTPUT); pinMode(PIN_DIRB_L,OUTPUT);
  pinMode(PIN_PWM_R,OUTPUT); pinMode(PIN_DIRA_R,OUTPUT); pinMode(PIN_DIRB_R,OUTPUT);
  analogWrite(PIN_PWM_L,0); analogWrite(PIN_PWM_R,0);
  digitalWrite(PIN_DIRA_L,HIGH); digitalWrite(PIN_DIRB_L,HIGH);
  digitalWrite(PIN_DIRA_R,HIGH); digitalWrite(PIN_DIRB_R,HIGH);
}
void setup(){
  Serial.begin(115200);
  setupInputs(); setupOutputs();
  Serial.println(F("== Smooth Decel / Auto Stop version =="));
}

// ===== loop =====
uint32_t tRamp=0, tPrint=0;

void loop(){
  // --- 버튼 입력 ---
  if (edgePressed(btns[0])) motion=FWD;
  if (edgePressed(btns[1])) motion=BWD;
  if (edgePressed(btns[2])) motion=SPOT_L;
  if (edgePressed(btns[3])) motion=SPOT_R;
  if (edgePressed(btns[4])) motion=PIVOT_L;
  if (edgePressed(btns[5])) motion=PIVOT_R;

  // 속도 상하
  if (edgePressed(btns[6]) && (speed_idx+1<N_SPEEDS)){
    speed_idx++; Serial.print(F("[Speed] ")); Serial.println(SPEEDS[speed_idx]);
  }
  if (edgePressed(btns[7]) && speed_idx>0){
    speed_idx--; Serial.print(F("[Speed] ")); Serial.println(SPEEDS[speed_idx]);
  }

  // 모든 버튼이 OFF면 STOP 명령
  bool any = rawRead(PIN_IN_FW)||rawRead(PIN_IN_BW)||rawRead(PIN_IN_SPOT_L)||
             rawRead(PIN_IN_SPOT_R)||rawRead(PIN_IN_PIVOT_L)||rawRead(PIN_IN_PIVOT_R);
  if(!any && motion != STOP) motion=STOP;

  // 목표 갱신
  computeTargets(motion, SPEEDS[speed_idx]);

  // 램핑
  uint32_t now=millis();
  if(now - tRamp >= RAMP_INTERVAL_MS){
    tRamp = now;

    // PWM ramp 계산
    uint8_t prevL = L.cur, prevR = R.cur;
    L.cur = ramp(L.cur, L.tgt);
    R.cur = ramp(R.cur, R.tgt);

    // 감속 중일 때는 DIR 유지, 완전 정지 시 DIR=0
    if (motion==STOP) {
      if (L.cur == 0) L.dir = 0;
      if (R.cur == 0) R.dir = 0;
    }

    // 적용
    applyAB(PIN_PWM_L, PIN_DIRA_L, PIN_DIRB_L, L.dir, L.cur, INVERT_LEFT);
    applyAB(PIN_PWM_R, PIN_DIRA_R, PIN_DIRB_R, R.dir, R.cur, INVERT_RIGHT);
  }

  // 상태 출력
  if(now - tPrint > 300){
    tPrint = now;
    const char* mstr[]={"STOP","FWD","BWD","SPOT_L","SPOT_R","PIVOT_L","PIVOT_R"};
    Serial.print(F("[Motion] ")); Serial.print(mstr[motion]);
    Serial.print(F(" | Speed%=")); Serial.print(SPEEDS[speed_idx]);
    Serial.print(F(" | L(dir,pwm)=(")); Serial.print(L.dir); Serial.print(','); Serial.print(L.cur);
    Serial.print(F(") R(dir,pwm)=(")); Serial.print(R.dir); Serial.print(','); Serial.print(R.cur);
    Serial.println(F(")"));
  }
}
```

---

### 배선 정리

## 📎 연관 문서


- [[메카넘휠 브랜딩_v1.0]] - 2개 공통 주제
- [[ESP32 485통신]] - 2개 공통 주제
- [[node-red 인터록 구현(개폐기용)]] - 2개 공통 주제
- [[node-red 모터 제어 리미트 릴레이]] - 2개 공통 주제
- [[라즈베리파이_Hailo8_카메라인식]] - 3개 공통 주제