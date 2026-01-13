# halio-8기반 영상처리 llm on 라즈베리파이 테스트

> **생성일:** 2025-11-29T01:41:00.000Z
> **수정일:** 2025-12-19T03:08:00.000Z

아래는 오늘 진행한 전체 작업 흐름을 Notion에 바로 붙여 넣을 수 있게 깔끔하게 구조화한 회고/정리본이야.
불필요한 말 없이 핵심 기술 흐름 + 문제 해결 과정 + 현재 상태 + 다음 단계까지 단번에 잡히도록 구성했어.
---

# 📌 **[2025-11-29 작업 요약]

라즈베리파이5 + Hailo-8 + USB 카메라 + LLM(음성명령) 통합 테스트 기록**
---

## ✅ 1.

## Hailo-8 초기 문제 해결 (드라이버 버전 불일치)

### ● 문제

- HailoRT 라이브러리 버전: 4.23.0
- Hailo PCIe 드라이버 버전: 4.20.0
- IDENTIFY 명령 오류 / FW 로딩 실패 / /dev/hailo0 액세스 실패
### ● 해결

1. Hailo 모든 패키지 제거
1. 4.20.0 버전 드라이버 + 라이브러리로 다시 설치
1. FW 파일 위치 체크 후 /usr/lib/firmware/hailo/ 경로 정리
1. 재부팅 후 정상 동작 확인
### ✔ 결과

```plain text
Firmware Version: 4.20.0
Device: HAILO8
/dev/hailo0 정상 동작
```

---

## ✅ 2.USB 카메라 + OpenCV 프레임 캡처 테스트

- /dev/videoX 번호 확인
- OpenCV로 테스트 시 GStreamer 오류 → V4L2 직접 사용으로 해결
- 저해상도(720p 이하)일 때 자원 사용량 약간 감소 관찰
- usb카메라 사용시 검출 영역 오류 보임 → csi카메라가 더 넓은 면적 커버하면서도 정확함. 자원 사용량은 전체의 30퍼센트 수준
### 

---

## ✅ 3.Hailo YOLO 모델 로딩 문제 해결

### ● 문제

- Model Zoo의 *.hef 파일 중 대부분이 Hailo-15용이라 Hailo-8에서 호환 불가
### ● 해결

- 기본 제공되는 Hailo-8용 모델 활용:
```plain text
/usr/share/hailo-models/yolov8s_h8.hef
```

### ✔ 결과

YOLO8s-H8 모델 로딩 및 vstreams 초기화 성공
---

## ✅ 5.

## 음성인식(Whisper) + JSON 변환 파이프라인 구축

### ● Whisper (faster-whisper) 설치

- ARM64 환경에서 tiny 모델 CPU로 테스트
- 3초 녹음 → whisper → 명령 텍스트화 정상 작동
- 웹켐 마이크 정상 작동 인식됨. 
### ● 스피커 출력 준비

- USB 사운드카드 + 스피커 연결 성공
- arecord / aplay 정상 동작 확인
---

## ✅ 6.LLM 기반 명령 처리(Qwen) 테스트

### ● 1) 음성 → 텍스트 → Qwen-planner(JSON)

- OpenAI local API or remote API 기반 구조 설계
- 0.5B 모델 정확도는 낮고 편차 큼
- 규칙 기반 파서가 훨씬 정확하고 빠름
### ✔ 결론

- LLM은 자유문장 처리 or 복합 명령에서 보조역할
- 기본 이동/회전/높이 조절 등은 규칙 기반 파싱이 압도적으로 안정적
- 차후 원격서버 LLM으로 전환해서 테스트할것
---

## ✅ 7.전체 아키텍처 현재 상태

### ● 입력

- USB 웹캠 (↓ 정확도 / ↑부하)
- Whisper STT (좋음)
- Hailo YOLO 사람감지 (작동)
### ● 처리

- Rule-based Command Parser: 안정적
- Qwen-planner: 구조는 완성, 0.5B는 출력 다양성 낮음
### ● 출력

- JSON 명령으로 메카넘 제어 준비됨
---

## 🔍

## 현재까지 정리된 통찰

1. Hailo-8 통합 성공 → 추후 CSI 카메라로 바꾸면 크게 안정됨
1. USB 카메라는 테스트용 이상으로는 비효율적
1. Whisper STT는 생각보다 훌륭한 품질
1. Qwen 0.5B는 빠르지만 궁극적으로 rule-based 파싱 필요
1. 전체 파이프라인이 완전하게 연결됨:
---

# 🧭 다음 단계 제안 (우선순위)

### 1️⃣ CSI 카메라 기반 Hailo YOLO 파이프라인 구성

- rpicam → hailo postprocess plugin
- 실시간 30fps 가능
- CPU 부하 50% 이하로 증대 안정성 UP
### 2️⃣ 사람 검출 안정화

- bounding box smoothing
- center tracking
- distance 추정 (bbox height 이용)
### 3️⃣ 음성명령 → JSON → 모터제어 통합 루프

- voice_to_json_test + mecanum485 제어 코드 합치기
### 4️⃣ remote LLM 연결

- Mac M2 Max에서 튜닝된 Qwen 실행
- Pi → HTTPS 요청으로 JSON 가져오기
---

필요하면 오늘 작성한 전체 스크립트 정리본 + 설치 커맨드 전체 모음집도 만들어줄게.
Notion 섹션별로 자동 목차도 넣어 정리해줄 수 있어.