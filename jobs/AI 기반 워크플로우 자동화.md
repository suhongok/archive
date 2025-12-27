# AI 기반 워크플로우 자동화

> **생성일:** 2025-04-22T00:47:00.000Z
> **수정일:** 2025-04-22T02:20:00.000Z

```markdown

# ✅ n8n + OpenAI + Google Calendar 연동 정리

## 🎯 목표
자연어로 AI에게 "내일 오전 10시에 친구 만나기로 등록해줘"라고 말하면  
👉 Google Calendar에 자동으로 일정 등록되는 시스템 구현

---

## 🧱 구성 요소

- **OpenAI 노드**: 자연어 이해 및 날짜/제목 정보 추출
- **Memory 노드**: 컨텍스트 유지
- **Google Calendar 노드**: 일정 등록 또는 조회 수행
- **AI Agent 노드**: 모든 흐름을 통합해주는 인터페이스 역할
- **n8n (Cloud)**: 전체 워크플로우 자동화 관리 플랫폼

---

## ⚙️ 구현 순서

### 1. OpenAI API 연결
- [OpenAI API Key 발급](https://platform.openai.com/account/api-keys)
- n8n에서 OpenAI 노드 추가 → Credential 등록

### 2. Google Calendar 연결
- n8n에서 Credential 메뉴 → `Google Calendar OAuth2` 생성
- Google 계정 로그인 → 권한 허용 (`calendar.events` 등)
- 인증 완료 시 Credential 연결됨

### 3. Google Calendar 노드 설정
- Resource: `Event`
- Operation: `Create`
- Calendar: `catleminok@gmail.com`
- Start / End Time: 인공지능 자동 설정하게 하기
- Summary: 친구 만남 (또는 AI 생성 제목)

---

## 🧪 테스트 예시

**입력:**  
```
내일 오전 10시에 친구 만나기로 등록해줘
```

**결과:**  
- Google Calendar에 '친구 만남'이라는 제목으로  
- 2025년 4월 23일 오전 10시 일정이 자동 등록됨 ✅

---

## 🚧 주요 오류 & 해결법

- **Unable to sign without access token**  
  인증 토큰 만료 → Credential 삭제 후 재인증 필요

- **Calendar parameter’s value is invalid**  
  Calendar ID 누락 → 이메일 직접 입력 (`catleminok@gmail.com`)

- **OpenAI 호출 실패**  
  무료 크레딧 소진 또는 결제 수단 미등록 → [Billing 확인](https://platform.openai.com/account/billing)

---

## 💡 향후 확장 아이디어

- 일정 중복 감지 후 대안 제시
- 음성 명령 연동 (Google Assistant, 카카오 등)
- 슬랙/카카오톡 메시지로 일정 알림 자동 전송
- Google Sheet 또는 Notion에 일정 로그 저장

```

- 실행 링크https://suhong86.app.n8n.cloud/workflow/JJyIypREUhly2Kyp
- 실행화면