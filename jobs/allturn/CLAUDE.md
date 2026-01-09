# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **documentation and business archive repository** for Allturn (올턴), a Korean company founded in 2023 that develops mecanum wheel-based mobile robots and elevated work platforms. All documentation is in Korean.

**This repository contains NO source code** - it is purely for documentation, business planning, technical specifications, and work logs.

## Repository Structure

The repository is flat with markdown documents at the root level, plus one subdirectory:

- **Root level**: Technical specifications, work logs, business documents, branding materials
- **mecanum 고소작업대 개발기획/**: Development planning documents for mecanum-based elevated work platforms (includes PDFs and Word documents)

## Key Documents

### Core Business Documents
- **README.md** - Overview of work logs, company status, and technical development roadmap
- **올턴_회사_분석.md** - Company business model, organization, technology strategy, project status
- **올턴_투자제안서_2026.md** - Investment proposal for 2026
- **올턴_기업가치_산정.md** - Company valuation document
- **올턴미래사업계획서.md** - Future business plan
- **기술_개발_항목.md** - Technical development items (3 major projects)

### Technical Specifications
- **ESP32_USB_JSON_통신.md** - Allturn USB NDJSON Control Protocol v1 specification for ESP32-S3
- **ESP32 485통신.md** - ESP32 RS-485 communication implementation
- **라즈베리파이_Hailo8_카메라인식.md** - Raspberry Pi 5 + Hailo-8 AI accelerator + camera recognition (completed project)
- **메카넘 플렛폼 제어 로직 다이어그램 1.06v.md** - Mecanum platform control logic diagram

### Work Logs (업무일지)
- **업무일지_12월.md** - December work logs with sales targets and meetings
- **업무일지_11월_[날짜]회의.md** - November meeting notes

### Product Development
- **dc 모터 메카넘휠 - ps4 컨트롤러 제어.md** - DC motor mecanum wheel PS4 controller control
- **ESP32 메카넘 로봇 - 사람 추종 및 제어 고도화.md** - ESP32 mecanum robot person following
- **메카넘휠 지게차 사람인지 경보장치 & following .md** - Person detection warning device for mecanum wheel forklift

### Branding and Products
- **ATIDrive 브랜딩 .md** - ATIDrive brand materials
- **메카넘휠 브랜딩.md** - Mecanum wheel branding
- **ATlift(Mecanum Forklift feat. ATIDRIVE).md** - ATlift product documentation

## Company Context

- **Founded**: 2023
- **CEO**: 이대표 (automotive background)
- **Business**: Mecanum wheel-based mobile robot development and sales
- **Teams**: Laser sales team + Development team
- **Major Project**: 100M KRW research project for rough-terrain mecanum wheel design (completion: April 2026)
- **Sales Target**: 300 units annually (distributor basis)

## Technology Roadmap

```
Phase 1: Electrical control
    ↓
Phase 2: Digital control system (current)
    ↓
Phase 3: AI-integrated control (in progress)
    ↓
Phase 4: Fully autonomous driving
```

## Current Development Priorities (2025-2026)

1. **ESP32-S3 Native USB JSON Communication** - cmd_vel standard protocol for mecanum wheel robot control
2. **Mecanum Wheel Control System Enhancement** - Transitioning from Phase 2 to Phase 3 (AI integration)
3. **Cybertruck AI Feature Integration** - Planning stage for mecanum wheel-based platform

## Hardware Stack

- **Microcontroller**: ESP32-S3 (Native USB, JSON protocol)
- **AI Edge Device**: Raspberry Pi 5 + Hailo-8 AI accelerator (26 TOPS)
- **Camera**: Raspberry Pi Camera V3 (12MP, 4K 30fps)
- **Motor Control**: DC motors, stepper motors for mecanum wheels
- **Communication**: USB (NDJSON), RS-485

## Communication Protocol

The company uses **Allturn USB NDJSON Control Protocol v1** for mecanum wheel control:

```json
{
  "cmd": "vel",
  "linear_x": 0.5,
  "linear_y": 0.0,
  "angular_z": 0.3,
  "timestamp": 1703338020
}
```

Supported commands: `vel`, `stop`, `status`, `calibrate`

## External Resources

- **Notion Workspace**: https://www.notion.so/suhong86/861b3256eb86487598e09fc1af3d5fb4?v=bc276a9a05624c4b9b4d94d1c9c58ac6
- Latest Notion entries include company development methods, meeting notes, and protocol specifications

## Notes for Claude

- All documents are in **Korean** - translations may be needed for non-Korean speakers
- This is an **archive/documentation repository** - there is no code to build, test, or run
- When asked to work with this codebase, focus on document organization, content analysis, translation, or documentation creation
- The company is in active development with regular meetings recorded in 업무일지 files
- Business documents contain sensitive information about company valuation and investment proposals
