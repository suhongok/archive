# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a personal knowledge management system ("archive") that stores professional and personal information in Markdown format. The repository is designed to work with Obsidian and integrates with Notion databases for synchronization.

### Purpose
- Personal diary and career planning
- Professional network management (people database)
- Work logs and technical documentation (Allturn company projects)
- Study notes and research

### Content Language
The repository primarily uses **Korean (한국)** for content, with some technical terms in English. File names may be in Korean.

## Directory Structure

```
/archive
├── diary/           # Personal diary, career planning, life goals
├── people/          # Personal network database (contacts, relationships)
├── jobs/            # Work logs and technical documentation (주제별 분류)
│   ├── 현재업무/       # Current Allturn projects (올턴 메카넘휠)
│   │   └── allturn/
│   ├── 이전업무/       # Previous company archives (록시스, 다오코리아)
│   ├── 하드웨어/       # Hardware development (라즈베리파이, ESP32, 센서)
│   ├── 소프트웨어/     # Software development (ROS, Node-RED, AI/ML)
│   ├── 농업_스마트팜/  # Smart farming projects
│   ├── 로봇/          # Robotics, drones, autonomous systems
│   ├── 회의_기록/      # Meeting notes
│   └── 기획_문서/      # Business planning, budgets, certifications
├── study/           # Learning notes (ROS2, AI/ML)
├── tools/           # Python utility scripts
├── .obsidian/       # Obsidian vault configuration (DO NOT EDIT)
└── README.md
```

### Key Files
- `link_generator.py` - Generates wiki-style links between related markdown files
- `notion_crawler.py` - Exports Notion database to markdown
- `organize_notion.py` - Organizes exported Notion files into appropriate folders
- `tools/reorganize_jobs.py` - Manual job folder reorganization
- `tools/reorganize_jobs_auto.py` - Automatic job folder reorganization by keywords

## Development Commands

### Python Environment

```bash
# Run link generator (creates cross-references between files)
python link_generator.py

# Sync from Notion (requires NOTION_API_TOKEN env var)
export NOTION_API_TOKEN="your_token"
python notion_crawler.py
python organize_notion.py

# Reorganize jobs folder by keywords
python tools/reorganize_jobs_auto.py
```

### Git Workflow

```bash
# Check status
git status

# Add and commit changes
git add .
git commit -m "descriptive message in Korean or English"
git push

# View recent commits
git log --oneline -10
```

## Key Concepts

### 1. People Network Management

**Location**: `/people/`

This folder maintains a personal CRM-like system tracking professional contacts.

**Structure**:
- Individual profile: `/people/[이름].md`
- Overview: `/people/목록.md`
- Guidelines: `/people/README.md`

**Profile Template Sections**:
- 👤 Basic information (name, date met, workplace)
- 🎯 Characteristics (personality, attitude)
- 💼 Professional info (company, role, expertise)
- 📞 Contact info (last contact, status)
- 💡 Collaboration potential (rating ⭐1-5, recommended frequency)
- 📝 Notes and retrospective
- 🔗 Related links

**Important**: This syncs with Notion database at https://www.notion.so/suhong86/74da43db631845648226645f8b48c6db

### 2. Work Documentation (Jobs)

**Location**: `/jobs/` (주제별 분류 체계)

총 369개 이상의 파일을 주제별로 체계적으로 관리합니다.

**폴더 구조**:
| 폴더 | 내용 | 파일 수 |
|------|------|--------|
| `현재업무/allturn/` | 올턴 메카넘휠 로봇 프로젝트 | ~50개 |
| `이전업무/` | 록시스, 다오코리아 과거 프로젝트 | ~83개 |
| `하드웨어/` | 라즈베리파이, ESP32, 센서, 모터 | ~60개 |
| `소프트웨어/` | ROS, Node-RED, AI/ML, 시스템 구축 | ~50개 |
| `농업_스마트팜/` | 임실, 남원 스마트팜, 식물재배 | ~38개 |
| `로봇/` | 로봇팔, 드론, 자율주행 | ~19개 |
| `회의_기록/` | 정기 회의록, 외부 미팅 | ~13개 |
| `기획_문서/` | 사업 기획, 예산, 인증, 업무일지 | ~56개 |

**Current Projects (Allturn)**:
- 메카넘휠 플랫폼 개발 (Mecanum wheel platform)
- ESP32-S3 USB JSON 통신 (cmd_vel standard)
- Jetson/Raspberry Pi AI 통합
- 고소작업대, 지게차 로봇 개발

**Notion Source**: https://www.notion.so/suhong86/861b3256eb86487598e09fc1af3d5fb4

### 3. Automated Link Generation

The `link_generator.py` script creates Obsidian-style `[[wiki links]]` between related files.

**How it works**:
1. Scans all markdown files in the vault
2. Extracts keywords and project categories (사이버트럭, 지게차, IoT시스템, etc.)
3. Calculates similarity scores based on:
   - Common keywords (70% weight)
   - Content similarity (30% weight)
4. Adds top 5 related files to `## 📎 연관 문서` section

**Categories (for link generation)**:
- 사이버트럭 (Cybertruck projects)
- 지게차 (Forklift projects)
- 라즈베리파이 (Raspberry Pi)
- 드론 (Drone)
- 센서 (Sensors)
- 모터제어 (Motor control)
- 네트워크 (Networking)
- IoT시스템 (IoT systems)
- 이미지인식 (Image recognition)
- 농업 (Agriculture/Smart farming)

**Job Folder Classification Keywords** (for `reorganize_jobs_auto.py`):
- **하드웨어**: 라즈베리파이, esp32, 센서, 모터, jetson, 보드
- **소프트웨어**: ros, node-red, ai, 인공지능, 이미지인식, ubuntu
- **로봇**: 로봇팔, 드론, 자율주행, 메카넘, 지게차
- **농업**: 스마트팜, 임실, 식물, 재배, 농업, 토지
- **회의**: 회의, 미팅, meeting
- **기획**: 기획, 사업, 예산, 인증, 업무일지

### 4. Notion Synchronization

**Process**:
1. `notion_crawler.py` - Fetches data from Notion API
2. `organize_notion.py` - Categorizes and cleans content
3. Files are automatically sorted:
   - Allturn-related → `/jobs/allturn/`
   - Other work → `/jobs/`
   - Empty/minimal files → skipped

**Keywords for Allturn classification**:
- allturn, ollturn, 올턴
- atidrive, ATIDrive
- 메카넘, mecanum

## Working with This Repository

### Adding New People Profiles

1. Create file: `/people/[이름].md`
2. Use standard template (see `/people/README.md`)
3. Update `/people/목록.md` with link
4. Commit with message: `"Add [이름] profile"`

### Adding Work Documentation

1. For current Allturn projects → `/jobs/현재업무/allturn/[제목].md`
2. For hardware development → `/jobs/하드웨어/[제목].md`
3. For software/AI development → `/jobs/소프트웨어/[제목].md`
4. For smart farming → `/jobs/농업_스마트팜/[제목].md`
5. For robotics/drones → `/jobs/로봇/[제목].md`
6. For meeting notes → `/jobs/회의_기록/[제목].md`
7. For business planning → `/jobs/기획_문서/[제목].md`
8. Run `link_generator.py` to create cross-references

**Quick Reference** (see `/jobs/README.md` for full details):
| 내용 | 저장 위치 |
|------|----------|
| 올턴 현재 프로젝트 | `현재업무/allturn/` |
| 라즈베리파이, 센서, 모터 | `하드웨어/` |
| ROS, Node-RED, AI | `소프트웨어/` |
| 스마트팜, 식물재배 | `농업_스마트팜/` |
| 로봇팔, 드론, 자율주행 | `로봇/` |
| 회의록, 미팅 | `회의_기록/` |
| 예산, 인증, 업무일지 | `기획_문서/` |
| 과거 프로젝트 | `이전업무/` |

### Syncing from Notion

1. Set `NOTION_API_TOKEN` environment variable
2. Run `notion_crawler.py` to export
3. Run `organize_notion.py` to categorize
4. Review and commit changes

## File Naming Conventions

- Use Korean for descriptive names: `메카넘휠_제어_로직.md`
- Include dates when relevant: `24년_3월_27일_회의_기록.md`
- Use underscores or spaces (both acceptable)
- Avoid special characters that may cause file system issues

## Important Notes

### DO NOT
- Edit files in `.obsidian/` directory (Obsidian config)
- Delete the `## 📎 연관 문서` section (managed by link_generator.py)
- Place files directly in `/jobs/` root (use appropriate subfolder)

### DO
- Use Korean naturally in content and file names
- Maintain consistent profile structure in `/people/`
- Keep Notion as source of truth for people database
- Run link generator after adding multiple new files
- Follow the template structures defined in README files

## Technical Context

### Technologies Referenced
- **ROS2** (Robot Operating System) - Future integration planned
- **ESP32-S3** - Microcontroller for robot control
- **Hailo-8** - AI accelerator for edge computing
- **Node-RED** - Visual programming for IoT
- **Raspberry Pi** - Edge computing platform
- **Obsidian** - Knowledge management interface

### Current Projects (Allturn)
- Mecanum wheel platform control systems
- USB JSON protocol (cmd_vel standard)
- AI integration for autonomous navigation
- Sales target: 300 units/year
- 100M KRW research project (completion: 2026.04)

## Maintenance

### Regular Tasks
- Monthly: Sync people profiles from Notion
- After bulk content addition: Run `link_generator.py`
- Weekly: Review and commit changes
- Quarterly: Update `/people/목록.md` network analysis
- When files need reorganization: Run `python tools/reorganize_jobs_auto.py`

### Jobs Folder Statistics
- **총 파일 수**: 369개+
- **총 폴더 수**: 11개 (서브폴더 포함)
- **가장 큰 카테고리**: 이전업무/록시스 (~78개)
- **현재 활발한 카테고리**: 현재업무/allturn (~50개)
