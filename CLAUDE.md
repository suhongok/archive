# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

개인 지식관리 시스템("archive")으로, Obsidian 기반 마크다운 저장소입니다.
**Robofarm** 창업을 중심으로 농업용 자율이동 로봇 개발 및 사업화를 진행하고 있습니다.

### Purpose
- **Robofarm 창업**: 노지(露地) 자율이동형 농업 로봇 개발 및 사업화
- 기술 문서 및 개발 로그 관리
- 인맥 네트워크 관리 (Notion 연동)
- 개인 일기 및 커리어 기획

### Content Language
한국어가 기본이며, 기술 용어는 영어를 병행합니다.

---

## Robofarm 프로젝트 개요

### 회사명: Robofarm

### 핵심 제품: 노지 자율이동형 농업 로봇

4륜(또는 6륜) 기반의 노지 밭(경작지) 자율이동 로봇 플랫폼.
지형 인식, 자기 위치 추정, 경로 계획을 통해 다양한 농작업을 수행한다.

**핵심 특징**:
- **자율이동**: GPS/RTK + LiDAR + 비전 센서 융합으로 노지 환경 자율주행
- **지형인식**: 경작지의 지형을 읽고 맵핑
- **모듈형 설계**: 이동체(플랫폼) 위에 작업 모듈을 교체 장착
  - 잡초 제거 모듈
  - 운반 모듈
  - 파종/이식 모듈
  - (추후 확장 가능)

**개발 우선순위**:
1. **이동체(플랫폼) 개발** ← 현재 집중
2. 자율주행 소프트웨어 (SLAM, Navigation)
3. 작업 모듈 추가 개발

### 기술 스택

| 영역 | 기술 |
|------|------|
| OS | Ubuntu 22.04 LTS |
| 미들웨어 | ROS2 Humble |
| SLAM | SLAM Toolbox |
| Navigation | Nav2 |
| MCU | ESP32-S3 (모터 제어) |
| 컴퓨팅 | Jetson / Intel NUC |
| 센서 | RPLidar, Orbbec Depth Camera, GPS/RTK |
| 구동 | BLDC 모터 + 드라이버 (4WD/6WD) |
| CAD | FreeCAD (.FCStd) |
| AI | Hailo-8 엣지 AI 가속기 |

---

## Directory Structure

```
/archive
├── diary/                  # 개인 일기, 커리어 기획
├── people/                 # 인맥 네트워크 DB (Notion 연동)
├── jobs/                   # 업무 문서 (주제별 분류)
│   ├── 현재업무/
│   │   ├── startup/        # ⭐ Robofarm 창업 기획 (사업계획서, 지원사업, 로드맵)
│   │   ├── farm_nav/       # ⭐ 이동체 플랫폼 CAD 설계 (FreeCAD)
│   │   ├── farm_weed_delete/ # 잡초 제거 모듈 (차후 개발)
│   │   ├── smart_farm/     # 스마트팜 제안서/아키텍처
│   │   └── allturn/        # [이전] 올턴 프로젝트 아카이브
│   ├── 이전업무/            # 과거 회사 (록시스, 다오코리아)
│   ├── 하드웨어/            # 라즈베리파이, ESP32, 센서, 모터
│   ├── 소프트웨어/          # ROS, Node-RED, AI/ML
│   ├── 농업_스마트팜/       # 농업/스마트팜 연구
│   ├── 로봇/               # 로봇팔, 드론, 자율주행
│   ├── 회의_기록/           # 회의록
│   └── 기획_문서/           # 사업 기획, 예산, 인증
├── study/                  # 학습 노트 (ROS2, AI/ML)
├── tools/                  # Python 유틸리티 스크립트
├── .obsidian/              # Obsidian vault 설정 (DO NOT EDIT)
└── README.md
```

### 핵심 프로젝트 폴더

| 폴더 | 내용 | 중요도 |
|------|------|--------|
| `현재업무/startup/` | Robofarm 창업 기획, 사업계획서, 지원사업 전략, 개발 로드맵 | ⭐⭐⭐ |
| `현재업무/farm_nav/` | 이동체 플랫폼 CAD 설계 (FreeCAD), 부품, 조립도, 계약서 | ⭐⭐⭐ |
| `현재업무/farm_weed_delete/` | 잡초 제거 모듈 (레이저 제초 등) | ⭐⭐ |
| `현재업무/smart_farm/` | 스마트팜 시스템 설계 | ⭐ |
| `현재업무/allturn/` | 올턴 재직 시절 프로젝트 아카이브 (메카넘휠, OdinLift 등) | 참조용 |

### 핵심 파일

**Startup 기획**:
- `startup/plan/2026_창업지원사업_신청전략.md` - 예비창업패키지 + 청년전용 창업자금 전략
- `startup/plan/개발_로드맵_2026.md` - HW/SW 개발 + 사업 연계 타임라인
- `startup/source/청년창업지원사업_조사보고서.md` - 지원사업 상세 조사

**이동체 설계 (farm_nav)**:
- `farm_nav/cads/` - FreeCAD 설계 파일 (프레임, 모터, 휠 등)
- `farm_nav/parts/` - 개별 부품 설계
- `farm_nav/sub_assembly/` - 서브 어셈블리
- `farm_nav/contracts/` - 계약/견적 관련

**유틸리티 스크립트**:
- `link_generator.py` - Obsidian 위키 링크 자동 생성
- `notion_crawler.py` - Notion DB → 마크다운 동기화
- `organize_notion.py` - Notion 파일 분류
- `tools/reorganize_jobs_auto.py` - 업무 폴더 자동 재분류

---

## Development Commands

### Python 유틸리티

```bash
# 연관 문서 링크 생성
python link_generator.py

# Notion 동기화
export NOTION_API_TOKEN="your_token"
python notion_crawler.py
python organize_notion.py

# 업무 폴더 자동 재분류
python tools/reorganize_jobs_auto.py
```

### Git Workflow

```bash
git status
git add .
git commit -m "descriptive message"
git push
git log --oneline -10
```

---

## Key Concepts

### 1. Robofarm 개발 로드맵 (2026)

**Phase 0 (1~2월)**: 하드웨어 제작 — CAD 완료, 부품 발주, 프레임 조립, 모터 연동
**Phase 1 (1~2월)**: 소프트웨어 기반 — SLAM/Nav2 연동, 기본 자율주행 (HW와 병렬)
**Phase 2 (2~3월)**: 실외 검증 — 농지 실외 테스트, 시연 영상, 사업계획서 제출
**Phase 3 (3~4월)**: PT 대비 — MVP 데모, 발표 평가
**Phase 4 (5~12월)**: 본격 개발 — HW 고도화, AI, 현장 실증, 제품화

**사업 일정**:
- 예비창업패키지: 2월 공고 → 3월 접수 → 4월 PT → 5월 협약
- 청년전용 창업자금: 수시 접수 (선착순, 2026년 내 필수)

### 2. People Network Management

**Location**: `/people/`

Notion DB(https://www.notion.so/suhong86/74da43db631845648226645f8b48c6db)와 연동되는 인맥 관리 시스템.

**Profile Template**:
- 기본 정보, 특성, 직업 정보, 연락처
- 협업 가능성 (⭐1-5), 메모, 연관 링크

### 3. Automated Link Generation

`link_generator.py`가 마크다운 파일 간 `[[wiki links]]`를 자동 생성합니다.

**카테고리**: 농업, 자율주행, 센서, 모터제어, 라즈베리파이, 드론, IoT시스템, 이미지인식 등

**분류 키워드** (for `reorganize_jobs_auto.py`):
- **하드웨어**: 라즈베리파이, esp32, 센서, 모터, jetson, 보드
- **소프트웨어**: ros, node-red, ai, 인공지능, 이미지인식, ubuntu
- **로봇**: 로봇팔, 드론, 자율주행, 메카넘, 지게차
- **농업**: 스마트팜, 임실, 식물, 재배, 농업, 토지
- **회의**: 회의, 미팅, meeting
- **기획**: 기획, 사업, 예산, 인증, 업무일지

### 4. Notion Synchronization

1. `notion_crawler.py` → Notion API에서 데이터 가져오기
2. `organize_notion.py` → 자동 분류
3. 인맥 DB: https://www.notion.so/suhong86/74da43db631845648226645f8b48c6db
4. 업무 DB: https://www.notion.so/suhong86/861b3256eb86487598e09fc1af3d5fb4

---

## Working with This Repository

### 문서 저장 위치

| 내용 | 저장 위치 |
|------|----------|
| Robofarm 창업 기획/전략 | `현재업무/startup/` |
| 이동체 CAD 설계 | `현재업무/farm_nav/` |
| 잡초 제거 모듈 | `현재업무/farm_weed_delete/` |
| 스마트팜 | `현재업무/smart_farm/` |
| 올턴 아카이브 (참조용) | `현재업무/allturn/` |
| 라즈베리파이, 센서, 모터 | `하드웨어/` |
| ROS, Node-RED, AI | `소프트웨어/` |
| 스마트팜, 식물재배 | `농업_스마트팜/` |
| 로봇팔, 드론, 자율주행 | `로봇/` |
| 회의록, 미팅 | `회의_기록/` |
| 예산, 인증, 업무일지 | `기획_문서/` |
| 과거 프로젝트 | `이전업무/` |

### File Naming Conventions

- 한국어 파일명 사용: `노지_이동체_설계_v2.md`
- 날짜 포함 (필요시): `2026-02-15_실외테스트_결과.md`
- 언더스코어 또는 공백 모두 가능
- 파일시스템 문제를 유발하는 특수문자 회피

---

## Important Notes

### DO NOT
- `.obsidian/` 디렉토리 편집 금지
- `## 📎 연관 문서` 섹션 삭제 금지 (link_generator.py가 관리)
- `/jobs/` 루트에 직접 파일 배치 금지 (서브폴더 사용)

### DO
- 한국어를 자연스럽게 사용
- Robofarm 관련 신규 문서는 `startup/` 또는 적절한 서브폴더에 저장
- 새 파일 대량 추가 후 `link_generator.py` 실행
- `/people/` 프로필은 Notion을 source of truth로 유지

---

## Technical Context

### Robofarm 이동체 하드웨어 구성

| 구성요소 | 사양 |
|----------|------|
| 프레임 | 알루미늄 프로파일 |
| 구동 | BLDC 모터 + 드라이버 (4WD or 6WD), 농지용 대형 바퀴 |
| 전원 | 리튬 배터리 (24V/48V) + BMS |
| 메인 컴퓨터 | Jetson / Intel NUC |
| 2D LiDAR | RPLidar A2/A3 |
| Depth Camera | Orbbec Astra/Femto |
| 위치 | GPS/RTK 모듈 |
| MCU | ESP32-S3 (모터 제어, micro-ROS 연동) |

### ROS2 시스템 구조

```
TF 트리: map → odom → base_link → sensors
토픽: /cmd_vel (이동 명령), /odom (위치), /scan (LiDAR), /camera/* (비전)
```

### 과거 프로젝트 참조 (Allturn)
- 메카넘휠 플랫폼: ESP32-S3 USB JSON 통신 (cmd_vel 표준)
- OdinLift/OdinTruck: SLAM, 자율주행 경험
- 이 경험을 Robofarm 이동체 개발에 활용

---

## Maintenance

### Regular Tasks
- Monthly: Notion 인맥 프로필 동기화
- 대량 문서 추가 후: `link_generator.py` 실행
- Weekly: 변경사항 리뷰 및 커밋
- 폴더 재분류 필요시: `python tools/reorganize_jobs_auto.py`

### Jobs Folder Statistics
- **총 파일 수**: 500개+
- **핵심 프로젝트**: `현재업무/startup/`, `현재업무/farm_nav/`
- **CAD 파일**: 110개+ (FreeCAD)
