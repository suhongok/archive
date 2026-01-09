# 라즈베리파이5 우분투 및 ROS설치

> **생성일:** 2024-05-07T07:50:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

### 설치시도#2

1. 라즈베리파이5에 sd카드32g 넣어서 컴퓨터 모니터와 연결하여 전원켬. 
1. 전원켜니 우분투 설치 인터페이스가 뜸. 64bit용 우분투 데스크탑 설치
1. 아이디 비번등 기본 설정후 ssh 설정
1. Ubuntu (Debian packages) — ROS 2 Documentation: Iron documentation 여기 참고하여 ROS2설치
### 설치시도#3

1. ubuntu server 20.04.5LTS(64-bit)버전을 라즈베리파이4에 설치 → 라즈베리파이5에서 인식안됨.
1. 라즈베리파이마다 지원하는 운영체제가 다르다. 현재ROS2를 지원하는 기기는 rasp4가 적합하다.
### 설치시도#4

1. 라즈베리파이 5에 설치 시도.
1. yahboom사이트에서 img파일 받아서 sd카드(32GB)에 넣음 라즈베리파이5에서 인식안됨.
1. 1.System_File - Google Drive

### 설치시도#5 24.5.15

1. Raspberry Pi for Robotics with ROS2 : Headless Development Setup (youtube.com)
1. 라즈베리파이4에 우분투 22.04 desktop버전 설치 → 성공(화면보임, SSH접속성공)
1. 카메라 리스트 업→lsusb카메라 인식 성공
1. cheese 설치해서 카메라 테스트 하니 인식 안됨.
1. vlc 설치 후 카메라 인식 시도 → vlc에서 기존 카메라는 인식을 못하나 웹캠은 인식이 됨. 
### 설치시도#6 

1. 라즈베리파이4 4GB기반으로 우분투 데스크탑 22.04버전 설치
1. Install ROS2 Humble on Raspberry Pi 4 - The Robotics Back-End (roboticsbackend.com) 참고 ROS2 설치
1. 설치성공 ROS2 
1. 코딩은 visual studio code ssh 활용 접속
### ROS2 + Ubuntu22.04 LTS(장기 지원버전) Desktop 버전 설치, JetsonNano

- [JN 10] JetsonNano 우분투 22.04 업그레이드 개요 (youtube.com)
- jetson nano에 우분투 20.04 LTS를 USB에 이미지를 구운후 테스트 했으나 동작 안됨. kernel error가 뜨는데, 원인을 모르겠음, 인터넷 상에는 성공사례가 있으나 나는 안됨. 보드 문제인가??
- 2번째 시도로 jetson nano 보드에 ros2를 설치하기 위해서 jetpack 4.6.1를 설치 시도 한다 이것은 ubuntu18.04버전이다. 그리고 ros2 dashing과 호환된다.MakingRobot :: Jetson nano 보드에 ROS 2 설치 (tistory.com)
- Jet pack용량이 13 기가 정도인데 그래서 그런지 유에스비에 굽는데 5분 정도 밖에 걸리지 않는다.

- 설치 시도 했으나 문제가 있어서 부팅이 안 됨 fail to start load kernel 문제가 발생해서 balena ether 대신 Rufus 통해서 설치 진행 중
또다시 커널 에러가 떠서 일단 쳇 나노 활용해서 프로그램 설치 하는 건 보류한다. 그대신 라즈베리파이 바이브 활용해서 다시 시도.


설치가 안 된 것은 제 슨 나노 키트를 위한 보드 이기 때문이다 자체 16 기가 이 MC 가 내장 된 형태임 잭슨 나노 보드 때문에 다른 게 설치가 안 됐던 거임. 


## 라즈베리파이5 + ubuntu desktop 22.04LTS에 ros2설치

- 설치시도#6  ← 참고
- 현재 깔린 우분투 버전을 확인해보니. $uname -r 우분투 24.04버전이라는 것을 알게 되었고, 거기에 맞는 ros2버전은 jazzy이며 이게 이미 설치 되어 있었다.
- ros2실행환경을 활성화 및 작동 테스트
## 라즈베리파이5 & 우분투 20.04 설치시도.

- 라즈베리파이5에 설치된 우분투에서 문제가 생김. 재설치 진행. (원격 화면 접속이 안됨.)
- balanaEther 를 활용해서 ubuntu20.04 서버 iso 설치
- 설치가 안되는 것으로 보아 라즈베리파이5 보드가 손상된 것으로 보임. 이유는 i2c연결 문제 때문? 원인은 . 잘모르겠음.

## 📎 연관 문서


- [[이미지 데이터 라벨링, 모델훈련, mediapipe, tensorflow]] - 2개 공통 주제
- [[라즈베리파이 비디오 스트리밍 웹, flask]] - 2개 공통 주제
- [[라즈베리파이 http 스트리밍 usb cam, 재부팅시 재실]] - 2개 공통 주제
- [[7월 24일 cm4확장보드에 cm4연결후 테스트]] - 2개 공통 주제
- [[라즈베리파이에 ROS2설치 및 pwm제어]] - 2개 공통 주제