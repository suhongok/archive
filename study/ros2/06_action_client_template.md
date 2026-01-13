# ROS2 액션 클라이언트 템플릿

이 문서는 `play_motion_client.py`를 템플릿화한 ROS2 액션 클라이언트의 일반적인 패턴입니다.

---

## 개요

ROS2 액션 클라이언트를 구현할 때의 표준 패턴을 제시합니다. 이 템플릿을 기반으로 다양한 액션 클라이언트를 빠르게 작성할 수 있습니다.

---

## 1. 기본 구조

```python
import rclpy
from rclpy.node import Node
from rclpy.action import ActionClient
from [ACTION_PACKAGE].action import [ACTION_TYPE]

class [CustomName]Client(Node):
    def __init__(self):
        super().__init__('[custom_name]_client')
        self.action_client = ActionClient(
            self,
            [ACTION_TYPE],  # 액션 메시지 타입
            '/[action_server_name]',  # 액션 서버 이름
        )
        self.get_logger().info('[CustomName] Client has been started')

    # ... 메서드들 ...

def main(args=None):
    rclpy.init(args=args)
    client = [CustomName]Client()

    try:
        # 클라이언트 로직
        rclpy.spin(client)
    except KeyboardInterrupt:
        client.get_logger().info('Keyboard interrupt received, shutting down...')
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

---

## 2. 핵심 메서드 패턴

### 2.1 목표 전송 메서드 (send_goal)

```python
def send_goal(self, param1, param2):
    """
    액션 서버에 목표를 전송합니다.

    Args:
        param1: Goal 메시지의 첫 번째 필드
        param2: Goal 메시지의 두 번째 필드
    """
    self.get_logger().info('Waiting for action server...')
    self.action_client.wait_for_server()

    # Goal 메시지 생성 (액션 타입에 따라 필드가 다름)
    goal_msg = [ACTION_TYPE].Goal()
    goal_msg.field1 = param1  # 실제 필드명으로 변경
    goal_msg.field2 = param2  # 실제 필드명으로 변경

    self.get_logger().info(f'Sending goal: {param1}, {param2}')

    # 비동기로 goal 전송 (callback과 함께)
    self.send_goal_future = self.action_client.send_goal_async(
        goal_msg,
        feedback_callback=self.feedback_callback  # 선택사항
    )
    self.send_goal_future.add_done_callback(self.goal_response_callback)
```

**주요 특징:**
- `wait_for_server()`: 서버 준비 대기
- Goal 메시지 생성 및 필드 설정
- `send_goal_async()`: 비동기 전송 (블로킹 없음)
- `add_done_callback()`: 응답 처리 콜백 등록

---

### 2.2 목표 응답 콜백 (goal_response_callback)

```python
def goal_response_callback(self, future):
    """
    액션 서버가 목표를 수락/거부했을 때 호출됩니다.
    """
    goal_handle = future.result()

    if not goal_handle.accepted:
        self.get_logger().error('Goal rejected by server')
        return

    self.get_logger().info('Goal accepted by server')

    # 결과를 비동기로 가져오기
    self.get_result_future = goal_handle.get_result_async()
    self.get_result_future.add_done_callback(self.get_result_callback)
```

**주요 특징:**
- Goal이 수락되었는지 확인
- 수락된 경우, 비동기로 결과 대기
- 거부된 경우, 에러 로깅 및 반환

---

### 2.3 결과 콜백 (get_result_callback)

```python
def get_result_callback(self, future):
    """
    액션이 완료되고 결과를 받았을 때 호출됩니다.
    """
    result = future.result().result

    # 결과 처리 (액션 타입에 따라 다름)
    if hasattr(result, 'success') and result.success:
        self.get_logger().info('Action completed successfully!')
    else:
        self.get_logger().error(f'Action failed: {result}')

    # 추가 작업 수행
    self.get_logger().info('Action completed')
```

**주요 특징:**
- `future.result().result`: 실제 Result 객체 추출
- 결과 필드 확인 및 처리
- 성공/실패 분기 처리

---

### 2.4 피드백 콜백 (feedback_callback)

```python
def feedback_callback(self, feedback_msg):
    """
    액션 실행 중에 주기적으로 호출됩니다.
    """
    feedback = feedback_msg.feedback

    # 피드백 처리 (액션 타입에 따라 다름)
    self.get_logger().info(
        f'Progress: {feedback.field1}, '
        f'Status: {feedback.field2}'
    )
```

**주요 특징:**
- `feedback_msg.feedback`: 실제 Feedback 객체 추출
- 진행 상황 표시
- 선택사항 (필요한 경우에만 구현)

---

## 3. PlayMotion2 실제 예시

```python
from play_motion2_msgs.action import PlayMotion2

class PlayMotionClient(Node):
    def __init__(self):
        super().__init__('play_motion_client')
        self.action_client = ActionClient(
            self,
            PlayMotion2,  # 액션 타입
            '/play_motion2',  # 서버 이름
        )

    def send_goal(self, motion_name, skip_planning=False):
        self.action_client.wait_for_server()

        goal_msg = PlayMotion2.Goal()
        goal_msg.motion_name = motion_name  # 실제 필드명
        goal_msg.skip_planning = skip_planning  # 실제 필드명

        self.send_goal_future = self.action_client.send_goal_async(
            goal_msg,
            feedback_callback=self.feedback_callback
        )
        self.send_goal_future.add_done_callback(self.goal_response_callback)

    def goal_response_callback(self, future):
        goal_handle = future.result()
        if not goal_handle.accepted:
            self.get_logger().error('Goal rejected')
            return

        self.get_logger().info('Goal accepted')
        self.get_result_future = goal_handle.get_result_async()
        self.get_result_future.add_done_callback(self.get_result_callback)

    def get_result_callback(self, future):
        result = future.result().result
        if result.success:
            self.get_logger().info('Motion completed successfully!')
        else:
            self.get_logger().error(f'Motion failed: {result.error}')

    def feedback_callback(self, feedback_msg):
        feedback = feedback_msg.feedback
        self.get_logger().info(
            f'Current time - sec: {feedback.current_time.sec}, '
            f'nanosec: {feedback.current_time.nanosec}'
        )
```

---

## 4. 명령줄 인자 처리 패턴

```python
import sys

def main(args=None):
    rclpy.init(args=args)
    client = [CustomName]Client()

    # 기본값 설정
    param1 = 'default_value'
    param2 = False

    # 명령줄 인자 처리
    if len(sys.argv) > 1:
        param1 = sys.argv[1]
    if len(sys.argv) > 2:
        param2 = sys.argv[2].lower() == 'true'

    try:
        client.send_goal(param1, param2)
        rclpy.spin(client)
    except KeyboardInterrupt:
        client.get_logger().info('Keyboard interrupt received, shutting down...')
    finally:
        rclpy.shutdown()

if __name__ == '__main__':
    main()
```

**사용 예:**
```bash
# 기본값으로 실행
ros2 run package_name node_name

# 인자 지정
ros2 run package_name node_name home false
ros2 run package_name node_name walk true
```

---

## 5. 비동기 흐름도

```
┌─────────────┐
│  send_goal  │ ─────> goal_msg 생성 및 전송
└─────────────┘
        │
        ▼
┌──────────────────────────┐
│ goal_response_callback   │ ─────> Goal 수락 확인
│                          │ ─────> get_result 비동기 요청
└──────────────────────────┘
        │
        ├─> (수락됨)
        │       ▼
        │   ┌──────────────────┐
        │   │ 액션 실행 중...   │
        │   │ feedback_callback │ 호출됨
        │   └──────────────────┘
        │       │
        │       ▼
        │   ┌──────────────────────┐
        │   │ get_result_callback  │ ─────> 최종 결과 처리
        │   └──────────────────────┘
        │
        └─> (거부됨)
                ▼
            에러 로깅 후 반환
```

---

## 6. 체크리스트

새로운 액션 클라이언트를 만들 때 다음을 확인하세요:

- [ ] ActionClient 초기화 (올바른 액션 타입, 서버 이름)
- [ ] send_goal() 메서드에서 Goal 필드 올바르게 설정
- [ ] goal_response_callback() 구현
- [ ] get_result_callback() 구현 (결과 처리 로직)
- [ ] feedback_callback() 구현 (필요한 경우)
- [ ] main() 함수에서 예외 처리 (try-except-finally)
- [ ] 명령줄 인자 처리 (필요한 경우)
- [ ] setup.py에 entry_point 등록
- [ ] 테스트 (액션 서버 실행 후 클라이언트 테스트)

---

## 7. 일반적인 실수

| 실수 | 문제 | 해결책 |
|------|------|--------|
| `wait_for_server()` 없음 | 서버 준비 전에 goal 전송 | 반드시 `wait_for_server()` 호출 |
| Goal 필드명 오류 | 타입 에러 또는 필드 없음 | 액션 메시지 정의 확인 |
| `feedback_callback` 미등록 | 피드백을 받지 못함 | `send_goal_async()` 호출 시 콜백 등록 |
| 동기 호출 | 블로킹으로 인한 UI 멈춤 | `send_goal_async()` 사용 (비동기) |
| 콜백에서 rclpy.spin() | 무한 루프 | main에서만 spin() 호출 |

---

## 8. 주요 개념 정리

### 비동기 호출
- `send_goal_async()`: Goal 전송 (블로킹 없음)
- `get_result_async()`: 결과 기다림 (블로킹 없음)
- 콜백으로 완료 시점 감지

### 콜백 체인
```
send_goal_async()
  └─> goal_response_callback()
        └─> get_result_async()
              └─> get_result_callback()
```

### Goal 수락/거부
- 수락: 액션 서버가 목표 실행 시작
- 거부: 액션 서버가 현재 다른 목표 처리 중 등

---

## 참고

이 템플릿은 `play_motion_client.py`의 패턴을 일반화한 것입니다.
실제 구현 시 다음을 참고하세요:
- 액션 메시지 정의 파일 (`.action`)
- 액션 서버 문서
- ROS2 공식 문서: https://docs.ros.org/en/humble/Tutorials/Intermediate/Writing-an-Action-Server-Client.html
