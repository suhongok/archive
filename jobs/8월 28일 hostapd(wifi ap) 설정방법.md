# 8월 28일 hostapd(wifi ap) 설정방법

> **생성일:** 2023-08-08T09:47:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

- 유틸설치
```shell
sudo apt-get isntall hostapd dnsmasq
```

- 설정파일 작성
```shell
#/etc/hostapd/hostapd.conf
interface=wlan0
bridge=br0
ssid=loxis_bridge30
hw_mode=g
channel=7
wmm_enabled=0
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase=YourPassword
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
```

```shell
#/etc/default/hostapd
#DAEMON_CONF= 를 변경
DAEMON_CONF="/etc/hostapd/hostapd.conf"
```

```shell
# hostapd 서비스 시작
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
sudo systemctl start hostapd

#sudo systemctl restart hostapd.service
```

- dns 설정하기
- dns & wifi ap 한번에 설정하기
- rasp ap 설치 및 사용