# 추가 카메라 설치 node-red, fswebcam활용

> **생성일:** 2025-01-14T06:08:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z


- 물의 상태를 보기위한 카메라 설치
- 기본 개념
- 노드 코드
```javascript
[
    {
        "id": "timer_trigger",
        "type": "inject",
        "z": "5f4ecb64ea70cbb4",
        "name": "10초 간격",
        "props": [
            {
                "p": "payload"
            }
        ],
        "repeat": "10",
        "crontab": "",
        "once": true,
        "onceDelay": "1",
        "topic": "",
        "payload": "",
        "payloadType": "date",
        "x": 100,
        "y": 2220,
        "wires": [
            [
                "capture_image"
            ]
        ]
    },
    {
        "id": "capture_image",
        "type": "exec",
        "z": "5f4ecb64ea70cbb4",
        "command": "fswebcam -d /dev/video2 -r 1280x720 --no-banner --jpeg 85 --delay 2 --skip 20 --set brightness=50% --set contrast=50% /home/pi/photos/image_water.jpg",
        "addpay": false,
        "append": "",
        "useSpawn": "false",
        "timer": "",
        "name": "사진 촬영",
        "x": 330,
        "y": 2220,
        "wires": [
            [
                "get_latest_image"
            ],
            [],
        ]
    },
    {
        "id": "get_latest_image",
        "type": "exec",
        "z": "5f4ecb64ea70cbb4",
        "command": "base64 /home/pi/photos/image_water.jpg",
        "addpay": false,
        "append": "",
        "useSpawn": "false",
        "timer": "",
        "name": "이미지 base64 변환",
        "x": 550,
        "y": 2220,
        "wires": [
            [
                "prepare_image"
            ],
            [],
        ]
    },
    {
        "id": "prepare_image",
        "type": "function",
        "z": "5f4ecb64ea70cbb4",
        "name": "이미지 준비",
        "func": "// base64 문자열 준비\nmsg.payload = 'data:image/jpeg;base64,' + msg.payload;\nreturn msg;",
        "outputs": 1,
        "noerr": 0,
        "initialize": "",
        "finalize": "",
        "libs": [],
        "x": 770,
        "y": 2220,
        "wires": [
            [
                "dashboard_image"
            ]
        ]
    },
    {
        "id": "dashboard_image",
        "type": "ui_template",
        "z": "5f4ecb64ea70cbb4",
        "group": "4bd72ec74fb763f2",
        "name": "카메라 이미지",
        "order": 7,
        "width": "6",
        "height": "6",
        "format": "<div style=\"width: 100%; height: 100%; display: flex; justify-content: center; align-items: center;\">\n    <img src=\"{{msg.payload}}\" style=\"max-width: 100%; max-height: 100%; object-fit: contain;\">\n</div>",
        "storeOutMessages": true,
        "fwdInMessages": true,
        "resendOnRefresh": true,
        "templateScope": "local",
        "className": "",
        "x": 990,
        "y": 2220,
        "wires": [
        ]
    },
    {
        "id": "49245152a4984207",
        "type": "comment",
        "z": "5f4ecb64ea70cbb4",
        "name": "용액통 모니터링",
        "info": "",
        "x": 90,
        "y": 2160,
        "wires": []
    },
    {
        "id": "4bd72ec74fb763f2",
        "type": "ui_group",
        "name": "식물공장제어",
        "tab": "81d350a77c0fc361",
        "order": 1,
        "disp": true,
        "width": "6",
        "collapse": false,
        "className": ""
    },
    {
        "id": "81d350a77c0fc361",
        "type": "ui_tab",
        "name": "Home",
        "icon": "dashboard",
        "disabled": false,
        "hidden": false
    }
]
```