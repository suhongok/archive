# ESP32 메카넘 로봇 - 사람 추종 및 제어 고도화

> **생성일:** 2025-11-20T08:36:00.000Z
> **수정일:** 2025-11-23T08:46:00.000Z

## 1. 주요 개발 내용

### ✅ 사람 추종 (Person Follower) 모드 구현

- 원리: 비전 센서(K230) 데이터를 기반으로 P(비례) 제어 적용.
- 안전 로직:
### ✅ 라이브러리 구조 리팩토링

- 기존: PersonVision (센서 파싱) + PersonFollower (추종 계산) 분리 구조.
- 변경: PersonVision 라이브러리에 추종 계산 로직(calculateFollow)을 통합.
### ✅ 게임패드(Bluepad32) 매핑 고도화

- 모드 전환:
- 디지털 주행 (버튼 주행):
---

## 2. 트러블 슈팅 및 튜닝 (Troubleshooting)

### 🛠️ 문제 1: 추종 시 동작이 끊김 (Stuttering)

- 증상: 로봇이 따라오다가 움찔거리며 멈추는 현상 반복.
- 원인: 안전을 위한 Deadman Timeout(입력 끊김 감지)이 100ms로 너무 짧아, 비전 데이터 처리 지연 시 정지 명령이 들어감.
- 해결: DEADMAN_MS를 500ms로 늘려 부드러운 주행 확보.
### 🛠️ 문제 2: 반대로 회전하는 현상

- 증상: 사람이 왼쪽으로 가면 로봇이 오른쪽으로 회전하여 시야에서 놓침.
- 원인: 카메라 좌표계와 로봇의 회전 방향(Kinematics) 부호 불일치.
- 해결: 회전 제어 게인(kp_turn) 계산식에 -1.0을 곱하여 방향 반전.
### 🛠️ 문제 3: 반응 속도 저하

- 증상: 사람이 빨리 움직이면 놓치거나 따라가는 속도가 너무 느림.
- 해결: 제어 게인(Gain) 및 속도 제한 대폭 상향.
### 🛠️ 문제 4: 안전 필터 충돌

- 증상: 추종 모드에서 전진 명령을 내리면 로봇이 멈춤.
- 원인: 기존 안전 필터(front_blocked)가 전방의 사람을 '장애물'로 인식하여 전진을 차단함.
- 해결: FOLLOW 모드일 때는 일반 장애물 차단 로직을 끄고, Hard Stop(충돌 직전)만 체크하도록 예외 처리.
---

## 3. 최종 파라미터 설정 (v1.14)


Sheets로 내보내기
---

## 4. 코드 스니펫 (핵심 로직)

C++
// PersonVision.cpp 내 추종 계산 로직
PersonVision::FollowResult PersonVision::calculateFollow(float area, int x1, int x2) {
    FollowResult res = {0, 0};
    int cx = (x1 + x2) / 2;

    // 1. 회전 제어 (Center Tracking) - 방향 반전 적용
    int err_x = _cfg.center_x - cx;
    if (abs(err_x) > _cfg.center_deadzone) {
        res.z_pct = (int)(err_x * _cfg.kp_turn * -1.0f); 
    }

    // 2. 거리 제어 (Area Tracking)
    float err_area = _cfg.target_area - area;
    if (abs(err_area) > _cfg.area_deadzone) {
        res.x_pct = (int)(err_area * _cfg.kp_dist);
    }
    
    // ... (속도 제한 로직) ...
    return res;
}
1. 차후 요청사항
### 사람 인식 following 업그레이드 - 타겟 팔로잉