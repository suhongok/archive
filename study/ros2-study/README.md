# ROS2 학습 자료

ROS2 개발 과정에서 학습한 내용을 정리한 저장소입니다.

## 📚 목차

### 1. Empty Service Client 분석
- ROS2 서비스 클라이언트의 기본 구조
- 비동기 서비스 호출 패턴
- [📄 자세히 보기](01_empty_service_client_분석.md)

### 2. spin() vs spin_once() 비교
- 두 함수의 차이와 사용 시기
- 블로킹과 논블로킹의 이해
- [📄 자세히 보기](02_spin_vs_spin_once.md)

### 3. 비동기 서비스 완료 확인 방법
- `future.done()` 폴링 방식
- `add_done_callback()` 콜백 방식
- `spin_until_future_complete()` 대기 방식
- [📄 자세히 보기](03_비동기_서비스_완료_확인.md)

### 4. 콜백 방식 동작 원리
- 콜백 실행 타이밍
- 비동기 작업의 생명주기
- [📄 자세히 보기](04_콜백_방식_동작_원리.md)

### 5. CMake 캐시 메커니즘
- 빌드 캐시의 역할과 문제점
- 캐시 초기화 방법
- [📄 자세히 보기](05_CMake_캐시_메커니즘.md)

---

## 🛠️ 주요 학습 키워드

- **ROS2 기초**: Node, Service, Client, Server
- **비동기 프로그래밍**: Future, Callback, Promise
- **이벤트 루프**: spin(), spin_once(), spin_until_future_complete()
- **빌드 시스템**: CMake, colcon, 캐시 관리

---

## 📖 사용 방법

각 마크다운 파일을 순서대로 읽으며 학습하세요. 코드 예시와 표, 다이어그램을 포함하고 있습니다.

---

## 💡 학습 환경

- **OS**: Ubuntu 20.04 / 22.04
- **ROS2**: Humble
- **Python**: 3.10+

---

## 📝 작성자

SM

## 📅 마지막 수정

2025년 12월 27일
