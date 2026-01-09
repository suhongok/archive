# 라즈베리파이 활용하여 DOF 로봇팔 제어 시도

> **생성일:** 2024-05-29T05:04:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

젯슨나노 보드에 OS설치 문제로 인하여 라즈베리파이5로 설치시도.
### 라즈베리파이5기반에 주어진 OS 세팅후 아래 동작 시키기.

### 라즈베리파이5 + 카메라 세팅 fswebcam

- http://www.yahboom.net/study/Dofbot-Pi
- 카메라 라즈베리파이5에 연결하고 실행 테스트
### 라즈베리파이5 - DOF 제어보드 I2C연결

- I2C통신기본https://lg960214.tistory.com/69
- 9번이 I2C연결핀인데, 원래는 18번에 연결해야하는데 9 번에 연결해도 될지 의문임
- I2C 선을 연결해서 로봇팔 DOFBOT제어 가능한지 테스트하기.
## 라즈베리파이5를 활용하여 환경 구성하기

라즈베리파이5 + ubuntu desktop 22.04LTS에 ros2설치 
- jupyterlab 설치 on unbuntu 24.04 https://www.howtoforge.com/how-to-install-jupyterlab-on-ubuntu-24-04/
## 라즈베리파이 ↔ 제어보드 컨트롤 라인 연결

http://www.yahboom.net/study/Dofbot-Pi
- GPIO test 하기, I2C선 연결 완료
-

## 📎 연관 문서


- [[7월 25일 라즈베리파이 습도, 온센서]] - 2개 공통 주제
- [[8월 11일 ToF 카메라 영상취득]] - 2개 공통 주제
- [[7월 28일 라즈베리파이 초음파센서 제어]] - 2개 공통 주제
- [[8월 1일 학생관리]] - 2개 공통 주제
- [[라즈베리파이 dht11 nodered 셋업]] - 2개 공통 주제