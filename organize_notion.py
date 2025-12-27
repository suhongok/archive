#!/usr/bin/env python3
"""
Notion export 파일을 정리해서 jobs 폴더에 배치하는 스크립트
- allturn 관련: /jobs/allturn/
- 기타 내용: /jobs/
- 빈 파일: 제외
"""

import os
import re
from pathlib import Path
from shutil import copy2

EXPORT_DIR = "/home/sm/archive/notion_export"
JOBS_DIR = "/home/sm/archive/jobs"
ALLTURN_DIR = os.path.join(JOBS_DIR, "allturn")

# allturn 키워드 (대소문자 무시)
ALLTURN_KEYWORDS = [
    'allturn',
    'ollturn',
    '올턴',
    'atidrive',
    'ATIDrive',
    '메카넘',
    'mecanum'
]

def should_skip_file(filepath):
    """빈 파일이나 내용이 거의 없는 파일인지 확인"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().strip()
        
        # 제목과 메타데이터만 있는 경우 제외
        # 실제 내용이 있으려면 150바이트 이상이어야 함
        if len(content) < 150:
            return True
        
        # 메타데이터만 있는 경우
        lines = content.split('\n')
        if len(lines) <= 6:  # 제목(1) + 메타(3) + 공백(2) 정도만
            return True
            
        return False
        
    except Exception as e:
        print(f"  ⚠️  읽기 오류: {e}")
        return True

def is_allturn_content(filepath):
    """allturn 관련 파일인지 확인"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read().lower()
        
        for keyword in ALLTURN_KEYWORDS:
            if keyword.lower() in content:
                return True
        
        return False
        
    except:
        return False

def clean_content(content):
    """파일 내용 정리"""
    lines = content.split('\n')
    cleaned = []
    
    for line in lines:
        # [toggle], [file], [image] 등 Notion 블록 제거
        if line.strip().startswith('[') and line.strip().endswith(']'):
            continue
        cleaned.append(line)
    
    # 연속된 빈 줄 제거 (3줄 이상 제거)
    result = []
    empty_count = 0
    for line in cleaned:
        if line.strip():
            result.append(line)
            empty_count = 0
        else:
            empty_count += 1
            if empty_count <= 2:  # 최대 2줄의 빈 줄만 허용
                result.append(line)
    
    return '\n'.join(result).strip()

def process_files():
    """파일 분류 및 이동"""
    export_files = sorted([f for f in os.listdir(EXPORT_DIR) if f.endswith('.md')])
    
    skipped = 0
    allturn_count = 0
    other_count = 0
    
    print(f"📁 처리 시작... 총 {len(export_files)}개 파일\n")
    
    for idx, filename in enumerate(export_files, 1):
        filepath = os.path.join(EXPORT_DIR, filename)
        
        # 빈 파일 확인
        if should_skip_file(filepath):
            skipped += 1
            if idx % 50 == 0:
                print(f"  ⏭️  [{idx}/{len(export_files)}] 빈 파일 제외: {filename}")
            continue
        
        # 파일 내용 읽기
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 내용 정리
            cleaned_content = clean_content(content)
            
            # 대상 폴더 결정
            if is_allturn_content(filepath):
                target_dir = ALLTURN_DIR
                allturn_count += 1
                status = "✅ allturn"
            else:
                target_dir = JOBS_DIR
                other_count += 1
                status = "📝 jobs"
            
            # 대상 경로
            target_path = os.path.join(target_dir, filename)
            
            # 파일 저장
            os.makedirs(target_dir, exist_ok=True)
            with open(target_path, 'w', encoding='utf-8') as f:
                f.write(cleaned_content)
            
            if idx % 20 == 0:
                print(f"  {status} [{idx}/{len(export_files)}] {filename}")
            
        except Exception as e:
            print(f"  ❌ [{idx}/{len(export_files)}] {filename} - {e}")
    
    print(f"\n" + "="*60)
    print(f"✅ 완료!")
    print(f"  - 생성됨 (allturn): {allturn_count}개 → {ALLTURN_DIR}")
    print(f"  - 생성됨 (기타): {other_count}개 → {JOBS_DIR}")
    print(f"  - 제외됨 (빈 파일): {skipped}개")
    print(f"  - 총 처리: {allturn_count + other_count}개")
    print("="*60)

if __name__ == "__main__":
    process_files()
