#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jobs 폴더를 방안 B(주제 기반)로 재구성하는 스크립트
"""

import os
import shutil
from pathlib import Path
import re

# 경로 설정
JOBS_DIR = Path("/home/sm/archive/jobs")

# 새로운 폴더 구조
NEW_STRUCTURE = {
    "현재업무": ["allturn"],  # allturn은 이미 존재하므로 이동
    "이전업무": ["록시스", "다오코리아"],  # 이미 존재
    "하드웨어": [],
    "소프트웨어": [],
    "농업_스마트팜": [],
    "로봇": [],
    "회의_기록": [],
    "기획_문서": [],
}

# 분류 키워드 (우선순위 순서)
CLASSIFICATION_RULES = {
    "회의_기록": [
        r"회의", r"미팅", r"meeting", r"브레인스토밍"
    ],
    "하드웨어": [
        r"라즈베리파이", r"raspberry", r"rpi", r"esp32", r"arduino", r"아두이노",
        r"센서", r"sensor", r"모터", r"motor", r"dc모터", r"서보",
        r"초음파", r"dht", r"온습도", r"릴레이", r"relay",
        r"cm4", r"jetson", r"제트슨", r"agx", r"orin",
        r"라우터", r"router", r"usb", r"ethernet", r"485",
        r"보드", r"board", r"하드웨어", r"gpio", r"핀",
        r"ToF", r"카메라", r"전원", r"배터리", r"충전",
        r"임베디드", r"embedded", r"펌웨어"
    ],
    "소프트웨어": [
        r"ros2?", r"node-red", r"노드레드", r"소프트웨어", r"software",
        r"ubuntu", r"우분투", r"linux", r"os", r"python", r"파이썬",
        r"flask", r"웹서버", r"api", r"데이터베이스", r"db", r"sql",
        r"스트리밍", r"streaming", r"vnc", r"ssh", r"원격",
        r"이미지.*인식", r"이미지.*검출", r"mediapipe", r"tensorflow",
        r"ai", r"인공지능", r"머신러닝", r"모델", r"훈련",
        r"gui", r"인터페이스", r"대시보드", r"dashboard",
        r"vpn", r"네트워크", r"통신", r"프로토콜", r"mqtt",
        r"json", r"데이터", r"알고리즘"
    ],
    "로봇": [
        r"로봇팔", r"로봇", r"robot", r"드론", r"drone",
        r"자율주행", r"autonomous", r"메카넘", r"mecanum",
        r"지게차", r"forklift", r"고소작업",
        r"adeept", r"ar4", r"servo", r"액추에이터",
        r"제어.*로봇", r"로봇.*제어", r"크레인"
    ],
    "농업_스마트팜": [
        r"스마트팜", r"smartfarm", r"임실", r"농업", r"농작물",
        r"식물", r"재배", r"비닐하우스", r"하우스", r"greenhouse",
        r"토지", r"땅", r"답사", r"방교리", r"감곡면",
        r"블루베리", r"딸기", r"토마토", r"상추", r"과수",
        r"육모", r"파종", r"수확", r"양액", r"관수", r"관개",
        r"ph센서", r"ec센서", r"비료", r"방제", r"살충",
        r"온풍기", r"분무기", r"펌프"
    ],
    "기획_문서": [
        r"기획", r"계획", r"사업", r"project", r"제안서", r"보고서",
        r"예산", r"구매", r"발주", r"견적", r"투자", r"가치산정",
        r"인증", r"특허", r"등록", r"신청", r"정책", r"지원",
        r"업무일지", r"업무", r"일지", r"todo", r"할일",
        r"조사", r"분석", r"시장", r"전망", r"현황"
    ]
}

def create_folder_structure():
    """새로운 폴더 구조 생성"""
    print("📁 폴더 구조 생성 중...")

    for main_folder, subfolders in NEW_STRUCTURE.items():
        main_path = JOBS_DIR / main_folder
        main_path.mkdir(exist_ok=True)
        print(f"  ✓ {main_folder}/")

        for subfolder in subfolders:
            sub_path = main_path / subfolder
            if not sub_path.exists():
                sub_path.mkdir(exist_ok=True)
                print(f"    ✓ {main_folder}/{subfolder}/")

def classify_file(filename):
    """파일명 기반으로 분류 결정"""
    filename_lower = filename.lower()

    # 각 카테고리별로 키워드 매칭
    for category, keywords in CLASSIFICATION_RULES.items():
        for keyword_pattern in keywords:
            if re.search(keyword_pattern, filename_lower):
                return category

    # 매칭되지 않으면 기획_문서로 (기본값)
    return "기획_문서"

def move_existing_folders():
    """기존 폴더들을 새로운 구조로 이동"""
    print("\n📦 기존 폴더 이동 중...")

    # allturn -> 현재업무/allturn
    allturn_src = JOBS_DIR / "allturn"
    allturn_dst = JOBS_DIR / "현재업무" / "allturn"
    if allturn_src.exists() and not allturn_dst.exists():
        shutil.move(str(allturn_src), str(allturn_dst))
        print(f"  ✓ allturn → 현재업무/allturn")

    # 록시스 -> 이전업무/록시스
    roxis_src = JOBS_DIR / "록시스"
    roxis_dst = JOBS_DIR / "이전업무" / "록시스"
    if roxis_src.exists() and not roxis_dst.exists():
        shutil.move(str(roxis_src), str(roxis_dst))
        print(f"  ✓ 록시스 → 이전업무/록시스")

    # 다오코리아 -> 이전업무/다오코리아
    dao_src = JOBS_DIR / "다오코리아"
    dao_dst = JOBS_DIR / "이전업무" / "다오코리아"
    if dao_src.exists() and not dao_dst.exists():
        shutil.move(str(dao_src), str(dao_dst))
        print(f"  ✓ 다오코리아 → 이전업무/다오코리아")

def reorganize_files(dry_run=False):
    """루트에 있는 파일들을 분류하여 이동"""
    print("\n📄 파일 분류 및 이동 중...")

    # jobs 루트의 .md 파일만 처리
    md_files = list(JOBS_DIR.glob("*.md"))

    if not md_files:
        print("  ℹ️  이동할 파일이 없습니다.")
        return

    # 분류 통계
    stats = {category: [] for category in CLASSIFICATION_RULES.keys()}

    for file_path in md_files:
        filename = file_path.name
        category = classify_file(filename)

        # 대상 경로
        target_dir = JOBS_DIR / category
        target_path = target_dir / filename

        stats[category].append(filename)

        if dry_run:
            print(f"  [{category}] {filename}")
        else:
            # 파일 이동
            try:
                shutil.move(str(file_path), str(target_path))
                if len(stats[category]) % 20 == 0:
                    print(f"  ✓ {category}: {len(stats[category])}개 파일 이동됨")
            except Exception as e:
                print(f"  ✗ {filename} 이동 실패: {e}")

    # 통계 출력
    print("\n📊 분류 결과:")
    total = 0
    for category in sorted(stats.keys()):
        count = len(stats[category])
        total += count
        if count > 0:
            print(f"  {category}: {count}개")
    print(f"\n  총 {total}개 파일 처리 완료")

def main():
    print("=" * 60)
    print("🗂️  jobs 폴더 재구성 시작 (방안 B: 주제 기반 분류)")
    print("=" * 60)

    # 1단계: 폴더 구조 생성
    create_folder_structure()

    # 2단계: 기존 폴더 이동
    move_existing_folders()

    # 3단계: Dry run (확인용)
    print("\n" + "=" * 60)
    print("🔍 파일 분류 미리보기 (실제 이동 전)")
    print("=" * 60)
    reorganize_files(dry_run=True)

    # 사용자 확인
    print("\n" + "=" * 60)
    response = input("\n위 분류대로 파일을 이동하시겠습니까? (y/n): ")

    if response.lower() == 'y':
        # 4단계: 실제 파일 이동
        print("\n" + "=" * 60)
        print("🚀 파일 이동 실행 중...")
        print("=" * 60)
        reorganize_files(dry_run=False)
        print("\n✅ 완료!")
    else:
        print("\n❌ 취소되었습니다.")

if __name__ == "__main__":
    main()
