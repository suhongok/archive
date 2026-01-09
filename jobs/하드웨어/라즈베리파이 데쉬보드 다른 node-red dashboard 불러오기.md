# 라즈베리파이 데쉬보드 다른 node-red dashboard 불러오기

> **생성일:** 2024-02-08T05:50:00.000Z
> **수정일:** 2025-09-13T15:38:00.000Z

임실에는 2개의 node-red 서버가 있다. 메인 node-redd 및 서브모터제어용 node-red이다.
메인 node-red에 접속해서 모터제어용 node-red를 제어하면 편하다.

- 위와 같이 구성하기 위해서 dashboard상에 template node를 추가하고 아래와 같이 내용을 넣었다.


```bash
<iframe style="width:600px; height:200px;" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
    src="http://loxisjeonju.iptime.org:60101/ui/"></iframe>

<iframe style="width:600px; height:400px;" frameborder="0" scrolling="no" marginheight="0" marginwidth="0"
    src="http://loxisjeonju.iptime.org:60103/?action=stream"></iframe>
```

- 서브 모터용 카메라 스트리밍 내용은 https://www.notion.so/suhong86/http-usb-cam-6be3bd8fa173428195413ab5fb0ce5f6?pvs=4 여기에 있다.
- 메인카메라도 http 형식으로 불러와서 재생하니 쉬움