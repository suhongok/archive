# ROS2 액션 타입이 필요한 이유

## 개요
ROS2에서 액션을 호출할 때 액션 서버뿐만 아니라 **액션 타입**을 명시해야 합니다. 이는 단순한 이름표가 아니라 클라이언트-서버 간의 통신을 위한 필수 요소입니다.

---

## 1. 메시지 구조 정의

액션 타입은 세 가지 메시지 구조를 정의합니다:

| 메시지 | 용도 | 예시 |
|--------|------|------|
| **Goal** | 액션 요청 데이터 | `target_pose`, `duration` |
| **Result** | 액션 완료 후 결과 | `final_status`, `distance_traveled` |
| **Feedback** | 실행 중 진행 상황 | `current_progress`, `elapsed_time` |

### 예시: Fibonacci 액션
```
Goal:
  - order: int32 (계산할 피보나치 항의 개수)

Result:
  - sequence: int32[] (피보나치 수열 결과)

Feedback:
  - sequence: int32[] (현재까지의 중간 결과)
```

타입이 없으면 어떤 데이터를 보내거나 받을지 알 수 없습니다.

---

## 2. 직렬화/역직렬화 (Serialization/Deserialization)

ROS2는 네트워크를 통해 메시지를 주고받을 때 **바이너리로 변환**합니다.

### 필요한 정보
- 각 필드의 데이터 타입 (int, string, array, nested 등)
- 필드의 순서와 크기
- 바이트 정렬 방식 (endianness)
- 배열의 길이

### 타입이 없으면?
```
송신자: "1.0, 2.0, 3.0" → 바이너리 변환
↓ (타입 정보 없음)
수신자: [?] 이게 3개의 float? int? double?
```

올바른 역직렬화가 불가능합니다.

---

## 3. 타입 안정성 (Type Safety)

### 타입 검증 메커니즘

**타입 없음:**
```
액션 클라이언트 ←→ (?) ←→ 액션 서버
              호환성 확인 불가
```

**타입 명시:**
```
액션 클라이언트 ←→ Fibonacci/action/Fibonacci ←→ 액션 서버
              ↓ 타입 검증
          같은 인터페이스 사용 강제
```

### 장점
- 타입 불일치 시 통신 거부
- 개발 초기에 오류 발견 가능
- 런타임 에러 감소

---

## 4. 미들웨어 간 통신 (DDS)

ROS2는 DDS(Data Distribution Service) 미들웨어를 사용합니다.

### DDS의 타입 검증
```
Topic/Service/Action을 고유하게 식별하는 방법:
1. 이름 (예: /my_action)
2. 타입 (예: MyPackage/action/MyAction)
```

타입 정보를 이용해:
- 호환되는 노드들만 통신 허용
- 타입이 다르면 통신 차단
- Topic 혼란 방지

### 실제 동작
```bash
# DDS는 내부적으로 다음을 확인합니다:
"이 노드가 fibonacci/action/fibonacci를 사용하려고 함"
"네트워크에 fibonacci/action/fibonacci 서버가 있나?"
"있다! 타입이 정확히 일치하나?"
"네, 일치합니다. 연결 수락"
```

---

## 5. 실제 사용 예시

### 액션 정의 (Fibonacci.action)
```yaml
int32 order
---
int32[] sequence
---
int32[] sequence
```

### 클라이언트에서의 호출
```bash
ros2 action send_goal /fibonacci fibonacci_msgs/action/Fibonacci "{order: 5}"
```

### 파이썬 코드
```python
from fibonacci_msgs.action import Fibonacci

# 타입이 명시되어 있어야 클라이언트 생성 가능
client = ActionClient(self, Fibonacci, '/fibonacci')

# Goal 메시지 생성 (타입에 따라 자동 완성)
goal_msg = Fibonacci.Goal()
goal_msg.order = 5
```

---

## 6. 타입 없이는 불가능한 이유 정리

| 항목 | 필요성 | 이유 |
|------|--------|------|
| 메시지 구조 파싱 | 필수 | Goal/Result/Feedback 정의 필요 |
| 바이너리 변환 | 필수 | 데이터 직렬화 방식 결정 |
| 타입 검증 | 필수 | 클라이언트-서버 호환성 확인 |
| 자동 코드 생성 | 필수 | stub/skeleton 코드 생성 |
| IDE 자동완성 | 권장 | 클라이언트 코드 작성 편의 |

---

## 7. 정리

**액션 타입은 단순한 이름표가 아닙니다.**

클라이언트와 서버 사이의 **통신 계약(Contract)**입니다:

```
"이 액션의 Goal은 int32 order입니다"
"Result는 int32[] sequence입니다"
"Feedback은 int32[] sequence입니다"
```

이 계약이 있어야:
✅ 안정적인 통신 가능
✅ 오류 조기 발견
✅ 예측 가능한 동작
✅ 자동 코드 생성
✅ IDE 지원

이것이 없으면 ROS2는 메시지가 무엇인지 알 수 없기 때문에 어떤 작업도 수행할 수 없습니다.
