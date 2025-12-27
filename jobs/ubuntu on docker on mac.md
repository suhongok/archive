# ubuntu on docker on mac

> **생성일:** 2024-06-20T01:43:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

# 맥북에서 docker 실행하여 우분투 설치후 ros 실행하기. 

# 맥북 m1아키텍쳐에서 도커 설치후 우분투 설치

# 도커 실행 및 우분투 실행

### 초기 실행

```bash
%docker --version #도커 버전 확인
%docker pull ubuntu #도커 허브에서 우분투 이미지 다운로드
docker run -d -it --name my_ubuntu -p 5901:5901 ubuntu #다운로드한 우분투 실행 이름을 my_buntu로 하고 포트를 5901번 사용하도록 함.
docker exec -it my_ubuntu /bin/bash #인터렉티브하게 화면 열음
root@ apt-get update
root@ apt-get install -y sudo vim curl #필요한 기본 편집기 설치
```

### 그래픽 환경 조성(feat. claude 3.5)

```bash
#필요한 패키지 설치
apt-get update
apt-get install -y xfce4 xfce4-goodies tightvncserver #설치시 시간이 10분정도 걸림.

```

- 위 단계 이후에 vncserver실행시 “The USER enviroment variable is not set. 에러 뜸. 사용자 환경 조성이 필요함.
```bash
#사용자 환경조성 root사용자로 진행
export USER=root #user환경변수 설정
export HOME=/root #홈 디렉토리 설정
vncserver #vncserver 실행및 비번 설정 22222222
```

```bash
vncserver -kill :1 #vncserver 종료
#vnc server 설정파일 생성

```

- 도커에서 현재 실행중인 컨테이너 id확인
```bash
a@aui-MacBookAir ~ % docker ps
CONTAINER ID   IMAGE     COMMAND       CREATED       STATUS       PORTS                    NAMES
2476599b1c00   ubuntu    "/bin/bash"   2 weeks ago   Up 2 weeks   0.0.0.0:5901->5901/tcp   my_ubuntu
```

- 도커 ip 확인
```bash
a@aui-MacBookAir ~ % docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' my_ubuntu           
172.17.0.2
```