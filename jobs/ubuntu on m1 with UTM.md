# ubuntu on m1 with UTM

> **생성일:** 2024-06-16T07:10:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

https://velog.io/@zihooy/M1-Mac-UTM-Linux-Ubuntu
### 설치 개요

- ros2개발을 위해 우분투가 필요하게 되었고, 맥북에 설치 시도를 하게 되었다.
- 우분투 20.04 다운로드
- UTM 설치
- UTM 실행해서 우분투 설치
- 우분투 실행
### 설치시 오류 해결(부팅오류)

- 초기 부팅시오류가 났으나 아래 글 참조하여 해결
- https://howudong.tistory.com/435
### 우분투 서버 설치

- ubuntu server22.04버전으로 설치하니 설치됨. 앞서 검은화면도 해결방법이 있었음 utm공식 싸이트 문서확인. 위 글대로 옵션 변환 안하고, 해도 가능.
- https://king-ja.tistory.com/93 참고하면 될듯. 처음에 데스크탑으로 설치 하지 말고 우분투 서버를 설치해서 업데이트 해야함.
- 우분투 설치 완료후 재부팅 하고 나서 화면 뜸. 드디어 됬다.
- 

## UTM활용해서  오늘 추가 설치 24.10.07

- https://sincerity.page/random/Random-How_to_install_Ubuntu20.04_in_M1/ 참고, 
- ID / PASSWD utuntu/2222

- 설치 잘됨.
- Ros2 시험 동작  source /opt/ros/foxy/setup.bash