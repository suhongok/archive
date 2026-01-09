# 라즈베리파이에 ROS2설치 및 pwm제어

> **생성일:** 2024-03-21T09:59:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

*ROS2는 ROS1에 비해서 실시간 작동이 강화된 버전이다.
### 진행단계

- 라즈베리파이에 우분투 설치 설치 파일링크:Thank you for downloading Ubuntu Server for Raspberry Pi | Ubuntu
- 설치후 , 화면설정필요함.
- The Ultimate Guide to Set Up Ubuntu Server On Raspberry Pi – RaspberryTips 이거 보고 설치했고 여러번 시도 끝에 결국 성공 설치직후 ssh 접속가능
- ROS2설치01장 ROS2 설치 | ROS2 하루에 입문하기 (gitbook.io)
## 라즈베리파이 ros2설치 시도 #2 ubuntu 22.04 client

- ubuntu 22.04 client 부분은 설치 실패, sd카드로 설치 시도했으나 계속 실패.
## 라즈베리파이5 + raspberry os로 설치 시도(중단)

- 결과: ros2소스를 다운받아 컴파일 하던중 오류가 나서 진행이 불가함. docker를 라즈베리파이 os에 설치하여 docker를 실행하라는 권고에따라 도커를 설치 이미지를 다운받아 설치하고 실행하니 ros2를 실행됨. 
## 라즈베리파이5 + 라즈베리파이 os + 도커 + ros2_humble환경 

- 명령어
- 컨테이너 실행후 컨테이너 접속해서 turtlesim 설치하기
## 방법 1: Docker 컨테이너를 이미지로 커밋하기

## 도커로 설치된 ros2를 활용하여 gpio실행하기

## docker 내부에서 테스트

## 도커내부에서 gpio핀으로 pwm모터 제어하기

## 라즈베리파이 os재 설치후 gpiod재설치하기.

## pwm제어 배선 및 테스트