# ROS2 spin() vs spin_once() 함수 비교

## 📊 기본 비교

| 구분 | `spin()` | `spin_once()` |
|------|----------|--------------|
| **동작 방식** | 무한 루프 | 한 번만 실행 |
| **블로킹** | 완전 블로킹 | 논블로킹 |
| **제어 반환** | 종료 신호까지 반환 안 함 | 즉시 반환 |
| **타임아웃** | 없음 | `timeout_sec` 설정 가능 |
| **사용 위치** | 간단한 서버/리스너 | 복잡한 로직, 병렬 작업 |

## 🔄 spin() 함수

### 특징
- **완전 블로킹**: 함수 호출 후 제어가 반환되지 않음
- **무한 루프**: ROS2 종료 신호(`rclpy.ok()` == False)까지 계속 실행
- **콜백 처리만**: 콜백 함수만 처리하고 다른 작업 불가

### 사용 예시
```python
rclpy.spin(node)  # 여기서 멈춤, 제어 반환 안 됨
# 이 아래 코드는 ROS2 종료까지 실행되지 않음
```

### 적합한 상황
- 서비스 서버만 대기
- 구독(subscription)만 처리
- 간단한 리스너 노드

---

## 🔄 spin_once() 함수

### 특징
- **논블로킹**: 한 번 처리 후 즉시 제어 반환
- **타임아웃 설정 가능**: `timeout_sec` 파라미터로 대기 시간 제어
- **반복 호출**: 보통 while 루프 안에서 반복 호출

### 사용 예시
```python
while rclpy.ok():
    rclpy.spin_once(node, timeout_sec=0.1)
    # 이 아래 코드가 계속 실행됨
    print("다른 작업 수행 중...")
```

### 적합한 상황
- 비동기 서비스 요청 대기
- 대기 중 다른 작업 필요
- 응답 상태 주기적 확인
- 여러 이벤트 동시 처리

---

## 💡 현재 코드에서의 활용

### empty_service_client.py에서 spin_once() 사용

```python
while rclpy.ok():
    rclpy.spin_once(empty_client, timeout_sec=0.1)  # ← 0.1초마다 콜백 처리
    
    if empty_client.future.done():                   # ← 응답 확인 가능
        try:
            response = empty_client.future.result()  # ← 결과 가져오기
            empty_client.get_logger().info('service call completed')
        except Exception as e:
            empty_client.get_logger().info('service call failed %r' % (e,))
        break
    
    # 서버 응답 대기 중에도 다른 작업 수행 가능
    empty_client.get_logger().info('additional work...!')
```

### spin_once()를 사용하는 이유

| 필요 조건 | 해결 방법 |
|----------|---------|
| 서비스 응답 기다리기 | `spin_once()` 루프로 계속 확인 |
| 응답 완료 감지 | `future.done()` 메서드 체크 |
| 응답 중 다른 작업 | while 루프 내에서 추가 작업 수행 |
| 빠른 반응성 | `timeout_sec=0.1` (0.1초)로 설정 |

---

## ⚖️ 선택 기준

### spin() 사용
```python
# 서비스 서버 예시
def main():
    rclpy.init()
    node = MyServiceServer()
    rclpy.spin(node)  # 서비스만 처리하면 됨
    rclpy.shutdown()
```

### spin_once() 사용
```python
# 클라이언트 또는 복잡한 로직 예시
def main():
    rclpy.init()
    node = MyClient()
    node.send_request()
    
    while rclpy.ok():
        rclpy.spin_once(node, timeout_sec=0.1)  # 비동기 처리
        if node.future.done():
            # 응답 처리
            break
    
    rclpy.shutdown()
```

---

## 📌 핵심 정리

- **spin()**: "항상 콜백 처리만 하기" → 서버 노드에 적합
- **spin_once()**: "주기적으로 콜백 처리 + 다른 작업" → 클라이언트 노드에 적합
