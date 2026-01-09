#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
jobs 폴더를 방안 B(주제 기반)로 재구성하는 스크립트 (자동 실행)
"""

import os
import shutil
from pathlib import Path
import re

# 경로 설정
JOBS_DIR = Path("/home/sm/archive/jobs")

# 새로운 폴더 구조
NEW_STRUCTURE = {
    "현재업무": ["allturn"],
    "이전업무": ["록시스", "다오코리아"],
    "하드웨어": [],
    "소프트웨어": [],
    "농업_스마트팜": [],
    "로봇": [],
    "회의_기록": [],
    "기획_문서": [],
}

# 분류 키워드
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
        for subfolder in subfolders:
            sub_path = main_path / subfolder
            if not sub_path.exists():
                sub_path.mkdir(exist_ok=True)

def classify_file(filename):
    """파일명 기반으로 분류 결정"""
    filename_lower = filename.lower()
    for category, keywords in CLASSIFICATION_RULES.items():
        for keyword_pattern in keywords:
            if re.search(keyword_pattern, filename_lower):
                return category
    return "기획_문서"

def move_existing_folders():
    """기존 폴더들을 새로운 구조로 이동"""
    print("\n📦 기존 폴더 이동 중...")

    moves = [
        ("allturn", "현재업무/allturn"),
        ("록시스", "이전업무/록시스"),
        ("다오코리아", "이전업무/다오코리아")
    ]

    for src_name, dst_path in moves:
        src = JOBS_DIR / src_name
        dst = JOBS_DIR / dst_path
        if src.exists() and not dst.exists():
            shutil.move(str(src), str(dst))
            print(f"  ✓ {src_name} → {dst_path}")

def reorganize_files():
    """루트에 있는 파일들을 분류하여 이동"""
    print("\n📄 파일 이동 중...")

    md_files = list(JOBS_DIR.glob("*.md"))
    stats = {category: 0 for category in CLASSIFICATION_RULES.keys()}

    for file_path in md_files:
        filename = file_path.name
        category = classify_file(filename)
        target_dir = JOBS_DIR / category
        target_path = target_dir / filename

        try:
            shutil.move(str(file_path), str(target_path))
            stats[category] += 1
            if stats[category] % 20 == 0:
                print(f"  ✓ {category}: {stats[category]}개 이동됨")
        except Exception as e:
            print(f"  ✗ {filename} 이동 실패: {e}")

    print("\n📊 최종 결과:")
    total = 0
    for category in sorted(stats.keys()):
        count = stats[category]
        total += count
        if count > 0:
            print(f"  {category}: {count}개")
    print(f"\n  총 {total}개 파일 이동 완료")
    return total

def main():
    print("=" * 60)
    print("🗂️  jobs 폴더 재구성 시작 (방안 B: 주제 기반 분류)")
    print("=" * 60)

    create_folder_structure()
    move_existing_folders()
    total = reorganize_files()

    print("\n" + "=" * 60)
    print(f"✅ 완료! {total}개 파일이 성공적으로 재구성되었습니다.")
    print("=" * 60)

if __name__ == "__main__":
    main()
