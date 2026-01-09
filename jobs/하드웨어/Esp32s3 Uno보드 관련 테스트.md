# Esp32s3 Uno보드 관련 테스트

> **생성일:** 2025-12-18T06:31:00.000Z
> **수정일:** 2025-12-18T06:43:00.000Z

---

# 📝 ESP32-S3 Uno + Xbox 컨트롤러 개발 일지

## 1. 하드웨어 정보

- 보드: ESP32-S3 Uno 폼팩터 (WeAct Studio S3 Core 또는 호환 보드)
- 통신 방식: USB 포트 뒤에 CH340C 칩 내장 (USB-to-Serial 변환 칩 사용)
- 연결 장치: Xbox Series X/S 컨트롤러 (Bluetooth)
## 2. 트러블슈팅 로그 (Troubleshooting)

### ✅ 이슈 1: 업로드는 되는데 시리얼 모니터가 먹통임

- 증상: Serial.println("BOOT OK") 코드를 넣어도 아무것도 출력되지 않음.
- 원인: ESP32-S3의 USB 설정이 Native USB로 되어 있어, CH340 칩(UART 포트)으로 데이터가 오지 않음.
- 해결:
### ✅ 이슈 2: Bluepad32 라이브러리 추가 시 무한 재부팅

- 증상: 코드를 넣으면 부팅 중에 멈추거나 계속 리셋됨.
- 원인: 블루투스 스택의 용량이 커서 기본 파티션(Default, 약 1.2MB) 공간을 초과함.
- 해결:
---

## 3. 아두이노 IDE 최종 설정값 (황금 세팅) ⭐

이 보드를 사용할 때는 항상 아래 설정을 맞춰야 함.
- Board: ESP32S3 Dev Module
- USB CDC On Boot: Disabled (필수: CH340 사용 시)
- Upload Mode: UART0 / Hardware CDC
- Partition Scheme: Huge APP (3MB No OTA/1MB SPIFFS) (필수: 블루투스 사용 시)
- PSRAM: OPI PSRAM (보드 스펙에 따라 다를 수 있으나 S3 Uno는 보통 OPI)
---

## 4. 최종 소스코드 (Bluepad32 Xbox 연결)

- 기능: Xbox 컨트롤러 연결 시 스틱/버튼 값을 0.2초 간격으로 시리얼 모니터에 출력
- 보드레이트: 115200
C++
```c++
/*
 * ESP32-S3 + Bluepad32: Xbox Series Controller input
 * H/W: ESP32-S3 Uno (CH340C)
 * Settings: USB CDC On Boot [Disabled], Partition [Huge APP]
 */

#include <Arduino.h>
#include <Bluepad32.h>

#define FORGET_BT_KEYS_ON_BOOT 0   // 1=기존 페어링 삭제(문제 시 사용), 0=일반 모드

ControllerPtr myControllers[BP32_MAX_GAMEPADS];
uint32_t lastPrintMs = 0;

// 컨트롤러 연결 시 호출
void onConnectedController(ControllerPtr ctl) {
  for (int i = 0; i < BP32_MAX_GAMEPADS; ++i) {
    if (myControllers[i] == nullptr) {
      myControllers[i] = ctl;
      ControllerProperties p = ctl->getProperties();
      Serial.printf("[+] CONNECTED idx=%d model=%s, VID=0x%04x PID=0x%04x\n",
                    i, ctl->getModelName().c_str(), p.vendor_id, p.product_id);
      return;
    }
  }
}

// 컨트롤러 연결 해제 시 호출
void onDisconnectedController(ControllerPtr ctl) {
  for (int i = 0; i < BP32_MAX_GAMEPADS; ++i) {
    if (myControllers[i] == ctl) {
      myControllers[i] = nullptr;
      Serial.printf("[-] DISCONNECTED idx=%d\n", i);
      return;
    }
  }
}

// 데이터 출력 함수
void dumpController(ControllerPtr ctl, int idx) {
  if (!ctl || !ctl->isConnected()) return;

  int lx = ctl->axisX();    // -511 ~ +512
  int ly = ctl->axisY();
  int rx = ctl->axisRX();
  int ry = ctl->axisRY();
  int lt = ctl->brake();    // 0 ~ 1023
  int rt = ctl->throttle(); // 0 ~ 1023
  uint8_t d = ctl->dpad();  // D-Pad

  // 버튼 상태 (A, B, X, Y, LB, RB 등)
  bool a = ctl->a(); bool b = ctl->b(); bool x = ctl->x(); bool y = ctl->y();
  bool lb = ctl->l1(); bool rb = ctl->r1();

  Serial.printf("idx=%d  LX=%4d LY=%4d  RX=%4d RY=%4d  LT=%4d RT=%4d  DPAD=%02X  [A:%d B:%d X:%d Y:%d]\n",
                idx, lx, ly, rx, ry, lt, rt, d, a, b, x, y);
}

void setup() {
  Serial.begin(115200);
  delay(500);

  // 필요 시 기존 페어링 정보 삭제
  if (FORGET_BT_KEYS_ON_BOOT) {
    Serial.println("[*] Forgetting stored Bluetooth keys...");
    BP32.forgetBluetoothKeys();
  }

  // Bluepad32 초기화
  BP32.setup(&onConnectedController, &onDisconnectedController);
  
  Serial.println("== Xbox Series Controller Waiting... ==");
}

void loop() {
  // 1. 데이터 업데이트 (필수)
  BP32.update();

  // 2. 200ms 마다 상태 출력
  uint32_t now = millis();
  if (now - lastPrintMs >= 200) {
    lastPrintMs = now;
    for (int i = 0; i < BP32_MAX_GAMEPADS; ++i) {
      if (myControllers[i] && myControllers[i]->isConnected()) {
        dumpController(myControllers[i], i);
      }
    }
  }
  delay(10);
}
```

---

### 🚀 향후 계획 (Next Steps)

1. 모터 제어: 수신된 axisY(스틱 값)를 PWM 신호로 변환해 모터 돌려보기.
1. 진동 피드백: 특정 조건(충돌 등)에서 패드에 진동 주기 (ctl->setRumble(force, duration)).
1. LED 제어: 패드의 버튼을 누르면 보드의 LED 켜기.