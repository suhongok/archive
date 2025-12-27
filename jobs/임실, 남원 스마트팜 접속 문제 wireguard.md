# 임실, 남원 스마트팜 접속 문제 wireguard

> **생성일:** 2024-06-03T01:00:00.000Z
> **수정일:** 2025-09-15T00:55:00.000Z

- 6월1일 토요일 임실 스마트팜이 연결이 안되었다고 연락옴, 원격제어 불가능.
- 6월 3일 출근해서 사무실에서 확인해 보니, 사무실 인터넷이 중지되었음.
- 사무실 공유기 리셋후 인터넷 복구됨. 그러나 스마트팜 접속이 안됨.

- Wireguard서버가 도작 중지된 것으로 보임.
- 문재가 반복될 가능성이 있음에 사설 서 버를 활용해 vpn구축 시도
- https://vultr.com - 사설 서버 
- Linux : Ubuntu 20.04 : WireGuard VPN 설정 방법, 예제, 명령어 (tistory.com) - wireguard on ubuntu 22.04LTS
### wireguard setup on Ubuntu 22.04LTS on Vultr.com private server

- 서버측 설정
```bash
sudo apt get update
sudo apt install wireguard
sudo apt isntall wireguard-go
wg genkey | sudo tee /etc/wireguard/privatekey | wg pubkey | sudo tee /etc/wireguard/publickey
sudo nano wg0 #파일 작성 하고 위에서 생성된 private 키 입력하기
ip -o -4 route show to default | awk '{print $5}'
sudo chmod 600 /etc/wireguard/{privatekey,wg0.conf}
sudo wg-quick up wg0
```


-PrKey OA0NS9h29cdvyAOYXwYz7mraaWh7JsSbvtHwibS6E2U=
-Pukey QEfXXZyJbJIekmcelnS3V039F3JJwc/t/Of87aMUQCA=
-notebook public key +PtV2pnuIEN08lHfb4eaJ7bV1RAmtmxHQMj8RlZq5TA=
Server Endpoint : 158.247.210.80:51820
- 윈도우에서 wireguard client 실행후, 
- 아래 그림과 같이 진행.

빈 터널 추가 하기, 위에 publickey에 서버 키를 넣고 서버 아이피를 넣는다
- 아래 명령어를 서버에서 실행
```bash
sudo wg set wg0 peer CLIENT_PUBLIC_KEY allowed-ips 10.0.0.2
```

- wireguard 접속 성공 

- 추후 라즈베리파이에서 접속 시도 할것. 
- 
### 사무실 라즈베리파이에서 접속시도

- 설치
- 접속파일 작성
- wireguard 서버에서 접속허용. 
- 클라이언트에서 wireguard 실행
- 클라이언트에서 접속 확인
- 결과화면

- 외부망에서 서브넷으로 패킷은 보내지나, portforwarding이 안됨..
- 내부망 컴퓨터(10.0.0.2)→ wg서버(10.0.0.1)→nr서버(10.0.0.4)로 접속은 가능.
- ubuntu port forwarding에 관해서 좀더 연구할 필요가 있음.
### 공용 ip 로 내부에 접속한 wireguard client (node-red, rasp5)에 접속 성공

1. 포트포워딩 활성화
1. 방화벽 오픈 1880 포트
1. iptable 활용하여 규칙확인
1. iptable 포트포워딩 설정
1. iptables 규칙 저장
1. 최종 확인(동작성공)