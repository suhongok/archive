# Transbot SE

> **생성일:** 2024-02-20T09:38:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

하드웨어
트랜스봇 SE 로봇 자동차 (yahboom.net)
보드 링크 현재 구매한 버전은 sub 버전 emmc16G
Jetson nano 4GB(B01/SUB) (yahboom.net)
- usb에 robot se 버전 설치해서 usb로 부팅하는것 테스트
- 192.168.0.68 jetson/yahboom으로 ssh접속가능 접속했는데 파일이 없음. 비어있음 usb에 robot se 이미지 파일 넣은후에 부팅할것
- 


### 제어 성공

- 연결하기: 트렌스봇을 켠후 오래 기다리면 oled에 화면이 뜬다.
- 화면에 192.168.1.11이 뜬것 확인하면 스마트폰을 transbot wifi에 연결한다. 비번 12345678
- 그후 yahboom앱을 실행해서, ip connect를 하여 192.168.1.11에 연결한다.
- 펌웨어에 접근하기 아이디 비번
- 

야붐로봇을 함수제어해서 물건 집게 하기 + node-red 제어 연결시도
### 야붐로봇 제어

- 로봇 로컬 네트워크에 접속시킴. ssh jetson / yahboom 접속
- jupiterlab 접속 : pi:8888 / passwd yahboom
- vnc 접속 / pswd: yahboom으로 접속해서 원격접속 가능.
ROS활용하여 새로운 동작 정