# Ros2 study

> **생성일:** 2024-05-29T06:19:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

로스트는 워크스페이스를 쉘을 이용하여 만든다. 매번 로스2 실행시 셀 스크립트 명령어를 실행 해야 한다. 그렇지 않으면 로스2를 쓸수가 없다. 
로스2 작동 시에 매번 슈에 대해서 소스를 실행 해줘야 되는 것을 기억
터틀심을 이용한 테스트하자

털 심의 노드 구성

섭스 클라이브 와 퍼블리셔 서비스 서버 서비스 클라이언트 액션서버로 구성된다.
### 노드(Node)란?

- 각 노드는 topic을 통해 서로 메시지를 주고 받고 서비스를 통해 요청과 반응을 한다.
- 완벽한 로봇시스템은 많은 노드가 함께 일하는것이 콘서트하는 것과 비슷하다.

- 노드가 시작되면 그것은 같은 ROS도메인에 광고를 한다. 노드는 주기적으로 자기의 존재를 광고한다. 노드는 꺼질때 주변에 알린다. 각각의 터미널에서 노드를 실행함.
Topics — ROS 2 Documentation: Rolling documentation
### 토픽(Topics)이란?

- 3가지 기본적인 인터페이스 스타일중 하나이다. 토픽은 연속적인 데이터 스트림을 위한 것입니다. 센서나, 로봇 상태등. 
### 발행(Publish)/구독(Subscribe)란?

- 발행 구독이란 데이터를 생성하는 자와 소비하는 자의 관계이다. 그들은 토픽을 통해서 서로 접촉한다. 예를 들면, 그들이 발행자를 만들면, 그것에게 토픽의 이름을 지어줘야 한다. 게다가 구독자도 같은 토픽명을 가져야한다. 특정 토픽에 대해 여려개의 발행자가 있을수 있으며, 여러개의 구독자가 있을수 있다. 어떤 발행자가 토픽에 대한 데이터를 발행하면 그 토픽을 구독하는 모든 구독자에게 전달된다. 이것을 또한 버스라 한다. 이러한 특징이 ROS2를 강력하면서도 유연한 시스템이 되는 이유이다. 만약에 당신이 데이터를 저장하고자 한다면 ‘ros2 bag record’라는 명령어를 써보라. 이 명령어는 당신이 이야기하는 어떤 것이라도 듣는 새로운 구독자를 생성한다. 
### 익명인(Anonymous)

- ROS2를 소개할때 언급되는 또다른 것은 익명인이다.이것은 어떤 구독자가 데이터를 받았을때, 일반적으로 그는 원래 어떤 발행인이 보낸것인지 모른다. 이러한 형태의 장점은 발행인과 구독인이 서로 즉시 바뀔수 있다는 것과 그것은 시스템 전체에 영향을 주게 된다.
### 타입이 지정된(Strongly-typed)

- 구독자와 발행자는 타입이 지정되어 있다. 코드는 매번 ROS에서 발행된 메시지가 타입에 맞는지 확인한다. 
Services — ROS 2 Documentation: Rolling documentation
→ 이어서 작성하기
### ROS1 vs ROS2 차이

- ROS2 - Real time, Safey, Certification, Security 스크래치로부터 시작됨.
- rcl이라는 기본 c기반 펀더멘털로 이루어짐에 따라 파이썬이나 cpp둘다 호환이 가능하다.
### 튜토리얼 작성

Configuring environment — ROS 2 Documentation: Rolling documentation
- https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Introducing-Turtlesim/Introducing-Turtlesim.html
- ros2 시작시 배쉬셀에 환경 변수를 반영해야 한다.
```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
```

- 우분투에서 거북이 조종창 열고 제어하기.

- 현재 실행중인 ROS2 요소 확인하기
```bash
ros2 node list
ros2 topic list
ros2 service list
ros2 action list
```

- rqt 를 사용하여 현재 ros2의 노드및 topic 흐름을 알 수 있다.

- rqt에서 Plugnin에서 “/spawn” 선택하면, 거북이를 하나 더 불러올 수 있다. 그런데 여기서 ‘turtl2’가 아닌 ‘’turtle2’ 등으로 쓰면, 문법상 에러가 발생하여 turtlesim 및 rqt도 같이 강제 중지된다.


- 여기서 turtle2를 제어하려면 위 turtle1에서 옵션을 더 추가해야한다. cmd_vel 값이 turtle1/cmd_vel으로 가는것이 아닌 turtle2/cmd_vel 값으로 전달되게 해야한다. 아래 그림에서 보면 왼쪽창의 빨간색 거북이가 오른쪽 커맨드 창의 움직임의 조종을 받은것을 알 수 있다.
```bash
ros2 run turtlesim turtle_teleop_key --ros-args --remap turtle1/cmd_vel:=turtle2/cmd_vel
```


- Ctrl + C 키로 모든 창 종료 가능하다.
### Remapping

- 노드 명이나, 토픽 이름을 변경할 수 있게된다. 아래의 예시를 통해 우리가 앞서 실행한 turtle_node를 my_turtle로 바꾸어 실행할 수 있게 된다.
```bash
#명령어 세부 명령 패키지이름 실행파일 --실행노드옵션 --리맵핑 __노드명을my_turtle로 치환
ros2 run turtlesim turtlesim_node --ros-args --remap __node:=my_turtle
```

- 왼쪽 첫번째 커맨드에서 turtlesim_node를 노드명을 my_turtle로 지정해서 실행하였고, 노드 리스트를 출력해보면 /my_turtle을 확인할 수 있다.

### 노드 정보 획득

- 노드의 현재 정보를 획득해서 노드에 대해 상세히 알 수 있다.
```bash
#명령어 세부명령어 info 노드명
ros2 node info /my_turtle
```


- 여기서 거북이 위치 이동을 위하여 teleop_turtle노드를 켜서 실행하고 노드 정보를 보자. 실행해서 화면을 보면 위의 노드 정보와 아래의 노드 정보가 다른것을 알 수 있다. 위에는 Action Server가 있으나 아래에는 Action Client가 있다.
```bash
#거북이 조종용 노드 실행
ros2 run turtlesim turtle_teleop_key
#실행중 노드 리스트 확인
ros2 node list
#조종용 노드 실행후 노드 정보확인
ros2 node info /teleop_turtle
```


### Topic을 통한 정보전달.

- publisher는 topic을 생성하고 subscriber는 topic정보를 가져온다. publisher는 여러개의 topic정보를 생성할 수있다. 마찬가지로 subscriber는 여러개의 topic정보를 수신할 수 있으며 표현하자면 n:n 통신이 가능한 것이다.
- rqt_graph를 통해서 서로 노드간에 어떻게 topic을 주고 받는지 알 수 있다. topic에도 계층이 있다. 아래 그림을 보면, turtlesim노드는 cmd_vel값을 teleop_turtle로부터 받는다. 그리고 그 움직임에 대한 결과물을 rotate_absolute를 통해서 전달하게 된다.

- https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Topics/Understanding-ROS2-Topics.html#ros2-topic-list 
- hide박스를 체크 해제 하면 우리가 볼수 없는 부분도 볼 수 있다.

- 실제 토픽이 발행되는 것을 커맨드 창에서 확인 가능하다. 아래 왼쪽 커맨드 창에서 커맨드를 입력하면, 오른쪽 창에 커맨드가 발행되는 것을 볼 수 있다. 
```bash
#ros2 topic echo <토픽 종류>
:ros2 topic echo /turtle1/cmd_vel
```


- 아래와 같은 명령어를 통해서 topic을 수신하는 곳과 발신하는 곳의 갯수를 알 수 있다.
```bash
#ros2 topic info <토픽명>
:ros2 topic info /turtle1/cmd_vel
```


- topic을 주고받는 것은 메시지를 주고 받는것과 같은데, 이 메시지는 포멧이 있다. 그것을 인터페이스라고 한다. 우리는 아래와 같은 명령어에서 인터페이스를 확인할 수 있다. 3개 직교좌표계 값과 3개의 회전좌표계값으로 이루어져 있다.
```bash
#ros2 interface show <메시지>
:ros2 interface show geometry_msgs/msg/Twist
```


- 특정 토픽에 대한 명령어 발행하기도 가능하다. 아래의 커맨드 처럼 입력하면, 거북이가 회전하는것을 알 수 있다. 이때, x: 를 띄어서 2.0을 입력해야 한다. 두번째 명령어같이 —rate 1 옵션을 주면, 계속회전한다. 마지막 그림에서, rqt_graph를 보면 커맨드 창에서 실행한 topic pub으로부터 계속해서 명령어를 받기 때문에 /turtle1/cmd_vel로 메시지가 전달되는 것을 그래프로 표현되어 있다.
```bash
#ros2 topic pub <topic_name> <msg_type> '<args>'
:ros2 topic pub --once /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
#1Hz명령어 발생
:ros2 topic pub --rate 1 /turtle1/cmd_vel geometry_msgs/msg/Twist "{linear: {x: 2.0, y: 0.0, z: 0.0}, angular: {x: 0.0, y: 0.0, z: 1.8}}"
```


- 토픽에 대해서받는것을 아래와 같이 추가할 수 있다.
```bash
#현재 커맨드창에 /turtle1/pose관련 메시지를 출력한다.
:ros2 topic echo /turtle1/pose
```

### 서비스의 이해

https://docs.ros.org/en/humble/Tutorials/Beginner-CLI-Tools/Understanding-ROS2-Services/Understanding-ROS2-Services.html
- 서비스는 publish - subscriber 모델과 달리 service는 응답을 하게 되는데, 특히 client가 요청 메시지를 보내면 server가 응답하는 방식을 사용한다. 서비스는 노드의 service server로 리퀘스트를 전달해주고 응답을 받으면 또다른 노드의 service Client로 전달해주는 형식이다.
- 서비스 리스트 확인하기, 아래의 명령어들을 치면 앞서 topic에서와 같이 거북이가 나타나고 서비스 리스트를 볼 수 있게된다.
- service가 topic과 다른 점은 요청하는 부분과 대응하는 두 부분으로 나뉘어 있다는 것이다. 아래 명령어로 ‘spawn’이란 명령어를 찾아보면, request할때 필요한 값이 위치및 각도, 이름(없으면 정해줌)등이고 생성되면 답변으로 이름을 줍니다.
- 서비스 요청하기.
- Ros2서비스가 서로 요청과 반응을 실시간으로 지켜볼수 있게 하는명령어가 service ehco이다. 아래와 같은 명령어를 치면된다. 하지만 우선 이전에 실행해야될 파일이 있고 설정해야 하는것이 있다.