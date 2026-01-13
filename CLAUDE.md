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
├── jobs/            # Work logs and technical documentation
│   └── allturn/     # Company-specific projects (메카넘휠, robotics)
├── study/           # Learning notes (ROS2, AI/ML)
├── .obsidian/       # Obsidian vault configuration (DO NOT EDIT)
└── .venv/           # Python virtual environment
```

### Key Files
- `link_generator.py` - Generates wiki-style links between related markdown files
- `notion_crawler.py` - Exports Notion database to markdown
- `organize_notion.py` - Organizes exported Notion files into appropriate folders

## Development Commands

### Python Environment

```bash
# Activate virtual environment
source .venv/bin/activate

# Run link generator (creates cross-references between files)
python link_generator.py

# Sync from Notion (requires NOTION_API_TOKEN env var)
export NOTION_API_TOKEN="your_token"
python notion_crawler.py
python organize_notion.py
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

**Location**: `/jobs/` and `/jobs/allturn/`

Tracks professional work at Allturn company (메카넘휠/mecanum wheel robotics).

**Key Topics**:
- Mecanum wheel control systems (메카넘휠 제어)
- ESP32-S3 USB JSON protocol for robot control
- Raspberry Pi + Hailo-8 AI accelerator projects
- ROS2 integration plans
- Company business strategy and sales targets

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

**Categories**:
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

1. For Allturn projects → `/jobs/allturn/[제목].md`
2. For general work → `/jobs/[제목].md`
3. Include clear titles and metadata
4. Run `link_generator.py` to create cross-references

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
- Modify `.venv/` (Python virtual environment)
- Delete the `## 📎 연관 문서` section (managed by link_generator.py)

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
