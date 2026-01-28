# USB WiFi 안테나 (TP-Link AX1800) 성능 테스트 결과

- 테스트 일시: 2026-01-28
- 플랫폼: Jetson (Linux 5.15.148-tegra, Ubuntu 22.04)

## 어댑터 정보

| 항목 | 내장 WiFi (wlP1p1s0) | TP-Link AX1800 (wlx0cef15393be0) |
|------|----------------------|----------------------------------|
| 칩셋 | Realtek rtl8822ce (PCIe) | Realtek rtl8852au (USB) |
| USB ID | - | 2357:013f |
| 드라이버 | rtl8822ce | 8852au (lwfinger/rtl8852au) |
| 대역 | 2.4 GHz (ch11) | 5 GHz |
| 링크 속도 | 156 Mb/s | 1,201 Mb/s |
| 신호 강도 | -49 dBm (61/70) | -54 dBm (56/70) |
| TX Power | 25 dBm | 12 dBm |
| SSID | 올턴가연테크 | 올턴가연테크 |
| USB 버스 | - | USB 2.0 (480Mbps) |

## Ping 테스트 (Google DNS 8.8.8.8, 20회)

| 항목 | 내장 WiFi | AX1800 |
|------|----------|--------|
| 평균 RTT | 29.2 ms | 30.2 ms |
| 최소 RTT | 27.3 ms | 28.8 ms |
| 최대 RTT | 32.2 ms | 34.0 ms |
| 지터 (mdev) | 0.95 ms | 1.04 ms |
| 패킷 손실 | 0% | 0% |

## Jitter 테스트 (50회, 100ms 간격)

| 항목 | 내장 WiFi | AX1800 |
|------|----------|--------|
| 평균 | 29.1 ms | 30.3 ms |
| 최대 | 36.9 ms | 34.4 ms |
| mdev | 1.39 ms | 1.30 ms |

## 다운로드 속도 (Cloudflare Speed Test)

| 파일 크기 | 내장 WiFi | AX1800 |
|----------|----------|--------|
| 10 MB | 9.92 MB/s (79.4 Mbps) | 10.08 MB/s (80.7 Mbps) |
| 100 MB | 11.90 MB/s (95.2 Mbps) | 11.93 MB/s (95.4 Mbps) |

## 업로드 속도 (Cloudflare Speed Test, 10MB)

| 항목 | 내장 WiFi | AX1800 |
|------|----------|--------|
| 속도 | 9.59 MB/s (76.7 Mbps) | 9.56 MB/s (76.5 Mbps) |

## HTTP 응답 테스트

| 대상 | 내장 WiFi (이전 측정) |
|------|---------------------|
| Google | DNS 7.6ms, Total 0.35s |
| Naver | Total 0.22s, 968 KB/s |

## 분석

1. **ISP 대역폭이 병목**: 두 어댑터 모두 ~95 Mbps로 거의 동일. ISP 상한에 걸려 WiFi 자체 성능 차이가 외부 테스트에서 드러나지 않음
2. **링크 속도 차이**: AX1800은 1,201 Mb/s, 내장은 156 Mb/s (7.7배 차이). LAN 내부 전송에서 차이 예상
3. **USB 2.0 병목**: AX1800이 USB 2.0 버스(480Mbps)에 연결됨. USB 3.0 포트 연결 시 성능 향상 가능
4. **신호 강도**: 내장 WiFi가 5dBm 더 강함 (-49 vs -54). 5GHz는 2.4GHz 대비 감쇠가 크기 때문
5. **안정성**: 두 어댑터 모두 패킷 손실 0%, 지터 유사. 안정적 통신 확인

## 드라이버 설치 참고

- 소스: https://github.com/lwfinger/rtl8852au
- 빌드: `make -j$(nproc)` 후 `sudo insmod 8852au.ko`
- 커널: 5.15.148-tegra (aarch64)
