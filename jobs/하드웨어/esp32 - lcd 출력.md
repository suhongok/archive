# esp32 - lcd 출력

> **생성일:** 2025-10-24T05:02:00.000Z
> **수정일:** 2025-10-24T05:10:00.000Z

---

# 📘 ESP32 + I²C LCD 실습 정리

## 1️⃣ 준비 부품


---

## 2️⃣ 배선도


> ⚠️ 5 V로 연결 시 SDA/SCL 라인이 5 V로 풀업될 수 있으므로
> 가능하면 3.3 V 사용 또는 레벨시프터 추가 권장.
---

## 3️⃣ 주요 확인 사항

- 가변저항 조정: 글자가 안 보이면 파란 가변저항을 돌려 콘트라스트 조정
- I²C 주소 확인: 0x27 또는 0x3F → I²C 스캐너로 검색
- LCD 크기 맞추기:
```plain text
LiquidCrystal_I2C lcd(0x27, 16, 2);  // 또는 (20, 4)
```

---

## 4️⃣ 설치 라이브러리

Arduino IDE → [스케치] → [라이브러리 포함하기] → [라이브러리 관리]
검색창에 입력:
```plain text
LiquidCrystal_I2C
```

📦 설치 대상: LiquidCrystal I2C by Frank de Brabander
---

## 5️⃣ 테스트 코드 (Hello LCD)

```plain text
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);

void setup() {
  Wire.begin(21, 22);
  lcd.init();
  lcd.backlight();
  lcd.setCursor(0,0);
  lcd.print("Hello, ESP32!");
  lcd.setCursor(0,1);
  lcd.print("I2C LCD Ready");
}

void loop() {}
```

---

## 6️⃣ 시리얼 입력 → LCD 출력

> PC 시리얼 모니터에 입력한 문자를 LCD로 표시
```plain text
#include <Wire.h>
#include <LiquidCrystal_I2C.h>

LiquidCrystal_I2C lcd(0x27, 16, 2);
String inputString = "";

void setup() {
  Serial.begin(115200);
  Wire.begin(21, 22);
  lcd.init();
  lcd.backlight();

  lcd.setCursor(0,0);
  lcd.print("Serial to LCD");
  lcd.setCursor(0,1);
  lcd.print("Ready...");
}

void loop() {
  while (Serial.available()) {
    char c = Serial.read();

    if (c == '\n' || c == '\r') {
      if (inputString.length() > 0) {
        lcd.clear();
        lcd.setCursor(0,0);
        if (inputString.length() <= 16)
          lcd.print(inputString);
        else {
          lcd.print(inputString.substring(0,16));
          lcd.setCursor(0,1);
          lcd.print(inputString.substring(16, min((int)inputString.length(), 32)));
        }
        Serial.println("LCD Updated: " + inputString);
        inputString = "";
      }
    } else {
      inputString += c;
    }
  }
}
```

✅ 실행 절차
1. 시리얼 모니터 열기 (115200 baud)
1. 입력창에 “Hello ESP32!” 입력 후 Enter
1. LCD 화면에 그대로 표시됨
---

## 7️⃣ 확인된 동작 요약


---