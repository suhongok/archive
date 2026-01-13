# ubuntu node-red 설치 및 외부 vpn서버에서 접속가능하게 하기.

> **생성일:** 2024-06-04T08:00:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

How to Install Node-RED on Ubuntu 20.04 | ArubaCloud.com
- 위 사이트 참고 

- wireguard client가 작동중이라 공개 주소를 resolving 못해서 초기에 설치가 안됨.
- 
### 포트 포워딩을 통해 공개 VPN서버 주소를 통해서 연결된 라즈베리파이 node-red로 접속하기.

- 기본정보: 우분투 서버 158.247.210.80
1. 포트포워딩 활성화
1. iptable 설정
1.