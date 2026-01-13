# Jetson AGX Orin GUI 환경 문제 및 VNC 접속

## 환경
- 장비: Jetson AGX Orin
- JetPack 설치 완료
- NVIDIA Driver: 540.4.0
- CUDA: 12.6
- OS: Ubuntu (GNOME Desktop)

## 문제 상황
- JetPack 설치 후 모니터 연결했으나 화면이 안 뜸
- SSH로만 접속 가능한 상태

## 진단 과정

### 1. GDM 상태 확인
```bash
sudo systemctl status gdm3
```
- 결과: active (running) - 정상 실행 중

### 2. 디스플레이 연결 확인
```bash
cat /var/log/Xorg.0.log | tail -50
```
- 결과: 모니터(VIE F3275T) DisplayPort로 감지됨

### 3. NVIDIA 드라이버 확인
```bash
nvidia-smi
```
- 결과: Orin (nvgpu) 정상 인식

### 4. Wayland 설정 확인
```bash
cat /etc/gdm3/custom.conf
```
- `WaylandEnable=false` 이미 설정됨

### 5. X 세션 프로세스 확인
```bash
ps aux | grep -E "Xorg|gnome"
```
- 결과: Xorg, gnome-shell 모두 실행 중

### 6. xrandr로 모니터 상태 확인
```bash
sudo DISPLAY=:0 XAUTHORITY=/run/user/128/gdm/Xauthority xrandr
```
- 결과: DP-0 connected, 1920x1080 출력 중

## 결론
- 그래픽 드라이버, X 서버, GNOME 모두 정상
- 모니터에 직접 화면이 안 나오는 것은 하드웨어 문제(케이블, 모니터 입력 소스 설정) 가능성

---

## VNC 서버 설치 및 접속

### 1. x11vnc 설치
```bash
sudo apt update
sudo apt install x11vnc -y
```

### 2. VNC 비밀번호 설정
```bash
x11vnc -storepasswd
```

### 3. GDM 로그인 화면용 VNC 서버 실행
```bash
sudo x11vnc -display :0 -auth /run/user/128/gdm/Xauthority -forever -noxdamage -repeat -rfbauth ~/.vnc/passwd -rfbport 5900 -shared
```

### 4. 사용자 로그인 후 VNC 서버 실행
로그인 하면 세션이 바뀌므로 다시 실행 필요:
```bash
x11vnc -find -forever -noxdamage -repeat -rfbauth ~/.vnc/passwd -rfbport 5900 -shared
```

### 5. VNC 클라이언트로 접속
- 주소: `Jetson_IP:5900`
- IP 확인: `hostname -I`

## 결과
- VNC로 접속 시 GUI 화면 정상 출력
- 그래픽 드라이버 및 소프트웨어 문제 없음 확인

---

## 추가 참고

### Wayland 비활성화 방법 (필요시)
```bash
sudo nano /etc/gdm3/custom.conf
```
`[daemon]` 섹션에 추가:
```
WaylandEnable=false
```

### VNC 자동 시작 설정 (선택)
```bash
mkdir -p ~/.config/autostart
cat > ~/.config/autostart/x11vnc.desktop << EOF
[Desktop Entry]
Type=Application
Name=x11vnc
Exec=x11vnc -find -forever -noxdamage -repeat -rfbauth /home/사용자명/.vnc/passwd -rfbport 5900 -shared
NoDisplay=true
EOF
```

---

작성일: 2026-01-07
