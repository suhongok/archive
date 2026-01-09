# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

**문서/아카이브 저장소** - 올턴(Allturn)의 사업 기록, 기술 사양, 업무일지를 보관합니다. 2023년 설립된 메카넘휠 기반 이동로봇 및 고소작업대 개발 회사입니다.

**소스 코드 없음** - 빌드, 테스트, 실행 명령이 없는 순수 문서 저장소입니다.

## Repository Structure

```
/                           # 루트: 마크다운 문서들
├── mecanum 고소작업대 개발기획/  # 개발기획서 (docx, pdf)
└── .claude/                # Claude 설정
```

## Key Documents

### 핵심 비즈니스
| 문서 | 내용 |
|------|------|
| `올턴_회사_분석.md` | 비즈니스 모델, 조직, 기술 전략 |
| `올턴_투자제안서_2026.md` | 2026년 투자 제안 |
| `올턴_기업가치_산정.md` | 기업가치 산정 |
| `기술_개발_항목.md` | 진행 중인 기술 과제 (4개) |

### 기술 사양
| 문서 | 내용 |
|------|------|
| `ESP32_USB_JSON_통신.md` | **Allturn USB NDJSON Control Protocol v1** - 핵심 통신 프로토콜 |
| `메카넘 플렛폼 제어 로직 다이어그램 1.06v.md` | 제어 로직 |
| `라즈베리파이_Hailo8_카메라인식.md` | Hailo-8 AI 가속기 프로젝트 (완료) |

### AI/엣지 컴퓨팅 실험
- `halio-8기반 영상처리 llm on 라즈베리파이 테스트.md`
- `jetson nano 구매 및 ai 기능 추가.md`
- `jetson orin nano llm사용시도..md`

### 업무일지
- `업무일지_12월.md`, `업무일지_11월_[날짜]회의.md`
- `한국건설기계연구원_미팅_브레인스토밍.md` - 2026년 1월 연구과제 미팅

## Company Context

- **설립**: 2023년
- **주요 프로젝트**: 험지전용 메카넘휠 R&D (1억원, 2026년 4월 완료 예정)
- **기술 단계**: Phase 2 (디지털 제어) → Phase 3 (AI 통합) 전환 중

## Communication Protocol

**Allturn USB NDJSON Control Protocol v1** - 메카넘휠 제어용:

```json
{"cmd": "vel", "linear_x": 0.5, "linear_y": 0.0, "angular_z": 0.3}
```

명령: `vel`, `stop`, `status`, `calibrate`

메카넘휠 공식:
```
FL = linear_x + linear_y + angular_z
FR = linear_x - linear_y - angular_z
RL = linear_x - linear_y + angular_z
RR = linear_x + linear_y - angular_z
```

## Hardware Stack

- **MCU**: ESP32-S3 (Native USB, NDJSON)
- **AI**: Raspberry Pi 5 + Hailo-8 (26 TOPS) / Jetson Nano (실험)
- **통신**: USB, RS-485

## Notes for Claude

- 모든 문서는 **한국어** - 번역 작업 시 기술 용어 원문 유지
- 문서 작업 중심: 정리, 분석, 번역, 신규 문서 작성
- `업무일지_*.md` 파일로 회의 기록 추적 가능
- 투자/기업가치 문서는 민감 정보 포함
