# ROS2 Empty Service Client 코드 분석

## 📋 프로그램 목적
ROS2 환경에서 'spin' 또는 'circle' 서비스를 호출하여 로봇이 회전하거나 원형 이동을 하도록 명령하는 클라이언트 프로그램입니다.

## 🏗️ 클래스 구조

### EmptyServiceClient 클래스
- **상속**: Node를 상속받아 ROS2 노드 구현
- **용도**: 서비스 클라이언트로 작동

### __init__ 메서드
```python
def __init__(self):
    super().__init__('empty_service_client')
    self.client = self.create_client(Empty, 'spin')  # 또는 'circle'
    
    # 클라이언트의 타입 및 이름과 일치하는 서비스를 사용할 수 있는지 1초에 한 번 확인
    while not self.client.wait_for_service(timeout_sec=1.0):
        self.get_logger().info('service not available, waiting again...')
    
    # 서비스 요청을 위한 요청 객체 생성
    self.req = Empty.Request()
```

**역할:**
- 서비스 클라이언트 생성 ('spin' 또는 'circle')
- 서비스 서버가 준비될 때까지 1초마다 대기
- Empty.Request() 객체 생성

### send_request 메서드
```python
def send_request(self):
    self.future = self.client.call_async(self.req)
```

**특징:**
- `call_async()`: 비동기 방식으로 서비스 요청 전송
- `self.future`: 응답 대기 객체 저장

## 🔄 main 함수의 동작 흐름

1. **ROS2 초기화**
   ```python
   rclpy.init(args=args)
   ```

2. **클라이언트 노드 생성 및 요청 전송**
   ```python
   empty_client = EmptyServiceClient()
   empty_client.send_request()
   ```

3. **응답 대기 루프**
   ```python
   while rclpy.ok():
       rclpy.spin_once(empty_client, timeout_sec=0.1)
       if empty_client.future.done():
           # 응답 처리
           break
       # 추가 작업 수행
       empty_client.get_logger().info('additional work...!')
   ```

4. **정리 및 종료**
   ```python
   empty_client.destroy_node()
   rclpy.shutdown()
   ```

## ✨ 주요 특징

| 특징 | 설명 |
|------|------|
| **비동기 방식** | `call_async()`로 논블로킹 호출 |
| **에러 핸들링** | try-except로 서비스 실패 처리 |
| **동시 작업** | 응답 대기 중 추가 작업 수행 가능 |
| **서비스 선택** | 'spin' 또는 'circle' 서비스 지원 |

## 📌 핵심 개념

- **future 객체**: 비동기 작업의 결과를 나중에 얻기 위한 객체
- **spin_once()**: 한 번의 콜백 처리 (타임아웃으로 제어 가능)
- **future.done()**: 서비스 완료 여부 확인
- **future.result()**: 서비스의 응답 결과 얻기
