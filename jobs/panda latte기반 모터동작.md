# panda latte기반 모터동작

> **생성일:** 2025-01-12T02:35:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

- pwm제어
- 판다라때 ↔ 내부 atmegachip(아두이노기반) ↔ pwm 신호출력
- 
```javascript
const int speedPin = 10;       // 모터 속도 제어 핀
const int inputPin = 8;        // 입력 감지 핀
const int motorSpeed = 200;    // 모터 속도 (0-255)

void setup() {
  // 제어 핀들을 설정
  pinMode(directionPin, OUTPUT);
  pinMode(speedPin, OUTPUT);
  pinMode(inputPin, INPUT);    // 8번 핀을 입력으로 설정
  
  // 시리얼 통신 시작 (동작 확인용)
  Serial.begin(9600);
}

void loop() {
  // 8번 핀의 입력 상태 읽기
  if (digitalRead(inputPin) == HIGH) {
    // 8번 핀이 HIGH일 때 정방향 회전
    Serial.println("정방향 회전");
    digitalWrite(directionPin, HIGH);    // 방향 설정 (정방향)
    analogWrite(speedPin, motorSpeed);   // PWM으로 속도 제어
  } else {
    // 8번 핀이 LOW일 때 모터 정지
    Serial.println("모터 정지");
    analogWrite(speedPin, 0);           // 모터 정지
  }
  
  delay(100);  // 짧은 지연 시간 (안정성을 위해)
}
```