# 라즈베리파이 http 스트리밍 usb cam, 재부팅시 재실

> **생성일:** 2024-02-05T01:21:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

- 참고 사이트: Stream Video Raspberry Pi + USB Webcam (youtube.com)
- 
- 기본 라이브러리 및 코드 컴파일, 설치 
```bash
$sudo apt-get update
$sudo apt-get install libjpeg9-dev
$sudo apt-get install imagemagick
$sudo apt-get install libv4l-dev
$sudo apt-get install cmake
$wget https://github.com/jacksonliam/mjpg-streamer/archive/master.zip
$unzip master.zip
$cd mjpg-streamer
$cd mjpg-streamer-experimental
$make clean all
$sudo make install
```

- 현재 실행중인 v4l2 카메라 확인
```bash
$v4l2-ctl --list-devices
```

- 실행 현재 /dev/video2에 접속되어 있음 8084포트로 /dev/video2 출력
```bash
$cd mjpg-streamer-master
$cd mjpg-streamer-experimental
$./mjpg_streamer -i "/usr/local/lib/mjpg-streamer/input_uvc.so -y -d /dev/video2 -n -f 6 -r 640x480" -o "/usr/local/lib/mjpg-streamer/output_http.so -p 8084 -w /usr/local/share/mjpg-streamer/www"
```

- 접속후 확인 rasp4 ip : 192.168.0.28:8084
```bash
http://192.168.0.28:8084/?action=stream
```

- usb카메라만 되는듯하다. 라즈베리파이에 mipi로 접속한 카메라에서는 동작안됨.
- usb cam 빼니 기존 arducam 잘됨.
- 설치 후 서버실행 카메라는 /dev/video0, /dev/video2, /dev/video4 
- 서버 실행포트 각 8084,8085,8086으로 실행
- 
### 임실 라즈베리파이모터 카메라 http 스트리밍

### 3대 카메라 동시에 http 실행하기

- 1대 테스트
- export STREAMER_PATH=$HOME/video/mjpg-streamer-master/mjpg-streamer-experimental
export LD_LIBRARY_PATH=$STREAMER_PATH
$STREAMER_PATH/mjpg_streamer -i "input_uvc.so -d /dev/video0 -n -r 640x480 -f 5 -timeout 60" -o "output_http.so -n -w $STREAMER_PATH/www -p 8084"
### 서비스 등록(재시작시 자동실행가능)

- usb video cam video0, video2, video4 활용
- 포트: 8084, 8085, 8086활용
- 파일 이동
```bash
sudo mv -r /home/loxis/video /mjpg_streamer/mjpg_streamer_experimental  
```

- 서비스 등록(1개만 등록하는 방법 나머지 2개는 추가 세팅해야함)
```javascript
sudo nano /etc/systemd/system/video-stream.service

Description=video0 streaming using http 8084port

Type=simple
ExecStart=/bin/bash -c 'cd /home/loxis/video/ && ./mjpg_streamer -i "/usr/local/lib/mjpg-streamer/input_uvc.so -y -d /dev/video0 -n -f 6 -r 640x480" -o "/usr/local/lib/mjpg-streamer/output_http.so -p 8084 -w /usr/local/share/mjpg-streamer/www"'

WantedBy=multi-user.target
```

- 서비스 실행
```javascript
sudo systemctl enable video-stream 

#동작 확인
192.168.10.120
sudo systemctl status video-stream

192.168.10.140에서
sudo systemctl status video-stream
sudo systemctl status video-stream1
sudo systemctl status video-stream2

```

- 2024-04-12 카메라 스트리밍 문제