# OpenMPTCProuter 설치

> **생성일:** 2023-12-29T02:01:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

### 설치가능?

OpenMPTCProuter use MultiPath TCP (MPTCP) to aggregate multiple Internet connections (4G,ADSL,VDSL,fiber,Starlink,...) and OpenWrt. Connections must have a latency < 500ms for now.
If MPTCP is not supported, OpenMPTCProuter can also use Multi-link VPN (MLVPN) or Glorytun UDP with multipath support.
The image can be installed on x86, x86_64 with UEFI, Raspberry PI 2B/3B/3B+/4B, Linksys WRT3200ACM/WRT32X, Teltonika RUTX12 and Banana PI BPI-R2.
A VPS with Debian 9/10/11 or Ubuntu 18.04/20.04 LTS is also required.
- openwrt에서 multipathVPN활용하기