# ROS2 _ Python 코딩

> **생성일:** 2024-05-27T08:59:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

### 라즈베리파이4 기반 ROS 코딩

- 환경 우분투데스크탑 22.04, ROS2, Visual studio code, ssh접속 코딩
### 파이썬 코딩 첫걸음

- Write a Minimal ROS2 Python Node - The Robotics Back-End (roboticsbackend.com)
```python
import rclpy
from rclpy.node import Node

def main(args=None):
    rclpy.init(args=args)
    node = Node('my_node_name')
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```

- 파이썬 라이브러리 rclpy.node에서 node 임폴트, rclpy를 먼저 임폴트후 rclpy.node에서 Node를 가져온다. 
- ROS2에서 실행하기 위해서는 패키지형태로 코딩해야하는데, 패키지를 구성후 colony를 활용하여 빌드 한다.
- 로컬 라즈베리파이에 ROS python 라이브러리를 설치한다.

### 첫ROS node 생성및 테스트

Write a Minimal ROS2 Python Node - The Robotics Back-End (roboticsbackend.com)
- ros2 소스 폴더 생성
- ros2 패키지 생성
- 코딩
- 파이썬 파일 실행파일로 변환
- 파이썬 파일 실행
- 파일을 수정했을때는 파일을 닫아야 저장이된다.
- setup.py에서 노드 및 프로그램 소스 및 엔트리 포인트를 지정해줘야 인스톨됨.

```bash
. ~/ros2_ws/install/setup.bash 
```

아래 명령어로 실행한 환경변수를 설정해줌. 설정을 해줘야 실행이 됨.
### 콜백 함수를 활용한 주기적으로 노드 함수 실행

```python
import rclpy
from rclpy.node import Node

class MyNode(Node):
    def __init__(self):
        super().__init__('my_node_name')
        self.create_timer(0.2, self.timer_callback)

    def timer_callback(self):
        self.get_logger().info("Hello ROS2")

def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
```