# node-red 서비스 등록으로 자동시작

> **생성일:** 2024-11-28T01:29:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

systemd 서비스를 사용하는 방법 (권장):BashAskCopyRun# Node-RED 서비스 활성화sudo systemctl enable nodered.service# 서비스 시작sudo systemctl start nodered.service
- systemd 서비스를 사용하는 방법 (권장):
- 서비스 상태 확인:
- 서비스 비활성화가 필요한 경우:AskCopyRun
이렇게 설정하면 라즈베리파이가 부팅될 때마다 Node-RED가 자동으로 시작됩니다. 웹 브라우저에서 http://<라즈베리파이IP>:1880으로 접속하여 Node-RED 에디터에 접근할 수 있습니다.