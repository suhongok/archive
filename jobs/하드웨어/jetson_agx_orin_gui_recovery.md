# Jetson AGX Orin GUI 환경 손상 복구 시도

**날짜:** 2026-01-06
**장치:** Jetson AGX Orin (JetPack, SSD 설치)
**증상:** 부팅 및 BIOS는 정상, GUI 환경만 안 뜸

---

## 문제 상황

- 부팅은 정상적으로 됨
- BIOS 화면은 정상 출력
- Linux 부팅 후 GUI 로그인 화면이 안 뜸 (검은 화면)
- 원격 GUI 접속(xrdp) 설정 후 문제 발생

---

## 진단 과정

### 1. 네트워크 접속 시도
```bash
# MAC 주소로 IP 찾기 시도
nmap -sn 172.30.1.0/24 && arp -a | grep -i "48:b0:2d"
```
- 결과: MAC 주소가 ARP 테이블에 없음 → 네트워크 연결 안 됨

### 2. 시리얼 콘솔로 접속
```bash
screen /dev/tty.usbmodem* 115200
```
- 시리얼 콘솔로 접속 성공

### 3. Display Manager 상태 확인
```bash
sudo systemctl status gdm3
```
- gdm3는 active (running) 상태

### 4. Xorg 에러 로그 확인
```bash
cat /var/log/Xorg.0.log | grep "(EE)"
```
**핵심 에러:**
```
(EE) NVIDIA(0): Failed to allocate NVIDIA Error Handler
(EE) systemd-logind: failed to take device /dev/dri/card1: Device or resource busy
(EE) modeset(G0): drmSetMaster failed: Device or resource busy
```

### 5. 원인 발견: xrdp 서비스
```bash
systemctl list-units --type=service | grep -iE "(vnc|rdp|nomachine|xrdp)"
```
- **xrdp.service**, **xrdp-sesman.service** 실행 중
- xrdp가 GPU/DRM 장치를 선점하여 로컬 디스플레이 충돌 발생

---

## 시도한 해결 방법

### 1. xrdp 비활성화
```bash
sudo systemctl stop xrdp xrdp-sesman
sudo systemctl disable xrdp xrdp-sesman
sudo reboot
```
- 결과: 여전히 검은 화면

### 2. Wayland 비활성화
```bash
# /etc/gdm3/custom.conf 수정
WaylandEnable=false
```
- 결과: 변화 없음

### 3. xorg.conf 설정 시도
```bash
sudo nano /etc/X11/xorg.conf
```
```
Section "Device"
    Identifier "Tegra"
    Driver "nvidia"
    Option "UseDisplayDevice" "DFP-0"
EndSection

Section "Screen"
    Identifier "Default Screen"
    Device "Tegra"
    DefaultDepth 24
EndSection
```
- 결과: 파란 화면으로 변경 (X서버 동작 확인)

### 4. lightdm으로 변경
```bash
sudo apt install lightdm
sudo dpkg-reconfigure lightdm
```
- 결과: 검은 화면

### 5. unminimize 실행
시스템이 minimized 상태였음:
```
"This system has been minimized by removing packages and content..."
```
```bash
sudo unminimize
sudo apt install --reinstall ubuntu-desktop gnome-shell gdm3
```
- 결과: 변화 없음

### 6. nvargus-daemon 비활성화
```bash
sudo systemctl stop nvargus-daemon
sudo systemctl disable nvargus-daemon
```
- 결과: 텍스트 프롬프트만 보이는 검은 화면

### 7. nvidia-xconfig 재생성
```bash
sudo nvidia-xconfig
```
- 결과: xorg.conf 생성됨, 하지만 GUI 여전히 안 뜸

### 8. xrdp 관련 설정 파일 제거
```bash
sudo rm -f /etc/X11/xorg.conf
sudo rm -rf /etc/X11/xrdp
echo "allowed_users=console" | sudo tee /etc/X11/Xwrapper.config
```
- 결과: 변화 없음

---

## 최종 상태

### /dev/dri/ 상태
```bash
ls -la /dev/dri/
```
```
card0
renderD128
```
- **card1 (tegra display)이 생성되지 않음!**

### 핵심 문제
- `/dev/dri/card1` 장치가 생성되지 않음
- tegra display 드라이버(13800000.display)가 DRM card1을 생성하지 못함
- L4T/JetPack 레벨의 드라이버 문제로 추정

---

## 결론 및 권장 사항

### 근본 원인
1. xrdp 설정 과정에서 드라이버/설정 손상 가능성
2. card1 (tegra display) 장치가 생성되지 않는 것이 핵심 문제
3. `NVIDIA Error Handler` 할당 실패 → GPU 초기화 불완전

### 권장 해결 방법
**SDK Manager를 통한 JetPack 재플래싱**

```bash
# Recovery Mode 진입:
# 1. Jetson 전원 끄기
# 2. Recovery 버튼 누른 채로 전원 켜기
# 3. 2초 후 Recovery 버튼 놓기
# 4. USB-C로 호스트 PC와 연결

# 호스트 PC에서 확인:
lsusb | grep -i nvidia

# SDK Manager 실행 후 재플래싱
# - Jetson OS 선택 (Desktop 버전, Headless 아님)
# - Storage: SSD (NVMe) 선택
```

---

## 참고: xrdp와 로컬 GUI 동시 사용 설정 (추후)

재플래싱 후 xrdp를 다시 설정할 때는 로컬 디스플레이와 충돌하지 않도록 설정 필요:

1. xrdp가 별도의 가상 디스플레이 사용하도록 설정
2. 또는 xrdp 대신 VNC (x11vnc) 사용 고려

---

## 배운 점

1. 원격 GUI 접속(xrdp) 설정 시 로컬 디스플레이와 충돌 가능
2. `Device or resource busy` 에러 → 다른 프로세스가 GPU/DRM 선점
3. Jetson에서는 card0(integrated), card1(tegra display) 구조
4. card1이 생성되지 않으면 로컬 디스플레이 출력 불가
5. L4T 드라이버 문제는 재플래싱이 가장 확실한 해결책
