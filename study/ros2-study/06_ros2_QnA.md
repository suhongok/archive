# ROS2 Q&A 정리

## 1. 실행 노드와 퍼블리셔
- 별도의 “실행 노드”가 퍼블리셔 노드를 돌려 주는 구조가 아니다. 퍼블리셔 기능을 가진 노드는 `ros2 run <패키지> <실행파일>` 또는 launch 파일로 직접 실행된다.
- Executor(`rclpy.spin()`, `spin_once()`)는 해당 프로세스 안에서 콜백을 돌려 주는 루프일 뿐, 다른 노드를 대신 띄우지 않는다.

## 2. 노드와 프로세스 관계
- 기본적으로 노드 하나가 OS 프로세스 하나로 실행된다.
- 하나의 프로세스에 여러 노드를 넣을 수도 있지만, 일반적 모델은 노드=프로세스 1:1이다.

## 3. 패키지에 여러 노드를 넣는 이유
- 관련 기능을 묶어 빌드·배포·버전 관리를 단순화한다.
- 공통 메시지, 파라미터, launch, 유틸 모듈을 공유해 중복을 줄인다.
- `package.xml` 한 곳에서 모든 노드의 의존 패키지를 선언할 수 있어 유지보수가 쉽다.

## 4. `ros2 run` vs `ros2 launch`
- `run`: 단일 실행파일(노드)을 그대로 띄움. 파라미터나 remap은 `--ros-args`로 직접 넘겨야 한다.
- `launch`: launch 파일에 정의한 여러 노드/파라미터/조건을 한 번에 실행. 시스템 전체 시나리오 재현에 사용.

## 5. 실행 시 변수(파라미터) 전달
- `ros2 run pkg node --ros-args -p my_param:=10 -r /old:=/new --log-level debug`처럼 명령줄 옵션으로 전달.
- launch 파일에서는 `DeclareLaunchArgument` 및 `ros2 launch pkg file arg:=value` 형태로 제어.

## 6. `colcon build`와 혼합 언어
- 파이썬 패키지(`ament_python`)와 C++ 패키지(`ament_cmake` 등)가 섞여 있어도 `colcon build` 한 번으로 모두 처리된다.
- 한 패키지 안에 파이썬·C++ 노드를 같이 둘 수도 있으나, 유지보수 편의를 위해 언어별 패키지를 나누는 경우가 많다.

## 7. 파이썬에서 C++로 단계적 전환
- ROS 인터페이스(토픽, 서비스)가 동일하므로, 초기에는 파이썬으로 빠르게 개발하고 점차 C++ 노드를 추가해도 된다.
- 워크스페이스 안에 두 언어 패키지를 함께 두고 launch에서 혼합 구성이 가능하다.

## 8. `--symlink-install`의 의미
- 설치 경로에 실제 복사본 대신 소스를 가리키는 심볼릭 링크를 만든다.
- 파이썬 노드는 소스 수정 직후 별도 빌드 없이 즉시 반영된다(C++ 바이너리는 재빌드 필요).
- 같은 터미널에서 이미 `source install/setup.bash`를 했으면 파일 수정 후 다시 소싱할 필요는 없다.

## 9. `setup.bash`와 `local_setup.bash`
- `setup.bash`: 현재 워크스페이스와 그의 상·하위 워크스페이스를 모두 순서대로 소싱.
- `local_setup.bash`: “현재 워크스페이스만” 환경에 추가. 이미 다른 ROS 환경을 소싱한 터미널에서 덧씌울 때 사용.
- 일반적으로는 `setup.bash`만 실행하면 내부에서 `local_setup.bash`를 호출하므로 둘을 연속으로 실행할 필요는 없다.

## 10. rqt로 `/cmd_vel` 발행
- `rqt_robot_steering` 플러그인 또는 `rqt_publisher` 플러그인을 열어 토픽을 `/cmd_vel`로 지정하면 GUI에서 `geometry_msgs/Twist` 메시지를 발행할 수 있다.

## 11. 모바일에서 rqt 실행?
- rqt는 Qt 기반 데스크톱 앱이라 Android/iOS용 빌드는 제공되지 않는다.
- 필요 시 VNC 등의 원격 접속이나 웹 기반 대시보드(rosbridge+웹클라이언트 등)로 대체한다.

## 12. rosbridge란?
- ROS 토픽·서비스·파라미터를 JSON 메시지로 노출하는 브리지 패키지(`rosbridge_suite`).
- 웹소켓/TCP를 통해 브라우저, 모바일 앱, Node.js/Python 등 비ROS 환경에서 ROS 기능을 사용할 수 있게 해 준다.
