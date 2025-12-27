# robotis 제어 테스트

> **생성일:** 2024-10-02T07:14:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

https://emanual.robotis.com/docs/en/platform/openmanipulator_x/quick_start_guide/
## 동작테스트

- 맥북(usb) - CR1.0(3 wire cable)- ROBOT ARM
- Cr 1.0 과 USB연결이 안되므로 고객센터에 문의 하기 리커버리 모드 진입. → 리커버리 모드 인식이 되지 않음
- DFU모드로 진입해서 부트로더 설치 시도 안됨. → 드라이버 설치가 안되서 Zadig활용하여 드라이버 설치, 드라이버 설치후 CR1.0보드와 윈도우 포트 연결됨. 부트로더 재설치 후 맥북에서도 허브통해서 됨
## Open manipulator를 openCR1.0통해서 제어하기

- 세팅: Mac→opencr1.0→open manipulator
- 프로그램 환경: Arduino ide
- 참고 링크: https://emanual.robotis.com/docs/en/platform/openmanipulator_x/quick_start_guide/#install-ros-on-pc
- 다운로드 확인 
## Dynamic cell control with wizard2.0(모터 동작 테스트)

## Control with Processing 4.3

## ROS활용한 컨트롤

- ros2 fossy 기반 설치, 우분투 20.04환경에서 실행 해야함. 그리고 아키텍쳐는 X86이어야 하는데, 이게 문제임.
- ros2환경 설정 on mac