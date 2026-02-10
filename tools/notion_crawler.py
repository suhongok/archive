#!/usr/bin/env python3
"""
Notion 데이터베이스를 마크다운 파일로 변환하는 크롤러
"""

import requests
import json
import os
from datetime import datetime
from pathlib import Path

# 설정
DB_ID = "861b3256eb86487598e09fc1af3d5fb4"
API_TOKEN = os.getenv("NOTION_API_TOKEN", "")  # 환경 변수에서 토큰 읽기
OUTPUT_DIR = "/home/sm/archive/notion_export"

# API 헤더
HEADERS = {
    "Authorization": f"Bearer {API_TOKEN}",
    "Notion-Version": "2022-06-28",
    "Content-Type": "application/json"
}

def create_output_dir():
    """출력 디렉토리 생성"""
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"📁 출력 디렉토리: {OUTPUT_DIR}")

def get_all_pages(db_id):
    """데이터베이스의 모든 페이지 조회 (페이지네이션 처리)"""
    all_pages = []
    cursor = None
    page_num = 1
    
    while True:
        url = f"https://api.notion.com/v1/databases/{db_id}/query"
        payload = {}
        
        if cursor:
            payload["start_cursor"] = cursor
        
        response = requests.post(url, headers=HEADERS, json=payload)
        
        if response.status_code != 200:
            print(f"❌ 조회 실패: {response.status_code}")
            print(response.text)
            break
        
        data = response.json()
        all_pages.extend(data.get("results", []))
        
        print(f"✓ 페이지 {page_num}: {len(data.get('results', []))}개 항목 조회")
        
        # 다음 페이지가 있는지 확인
        if not data.get("has_more"):
            break
        
        cursor = data.get("next_cursor")
        page_num += 1
    
    return all_pages

def get_page_content(page_id):
    """페이지의 블록(콘텐츠) 조회"""
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=HEADERS)
    
    if response.status_code != 200:
        return []
    
    return response.json().get("results", [])

def extract_text(text_obj):
    """텍스트 객체에서 일반 텍스트 추출"""
    if isinstance(text_obj, dict):
        return text_obj.get("plain_text", "")
    elif isinstance(text_obj, list):
        return "".join(extract_text(t) for t in text_obj)
    return str(text_obj)

def block_to_markdown(block):
    """블록을 마크다운으로 변환"""
    block_type = block.get("type")
    block_data = block.get(block_type, {})
    
    # 리스 블록
    if block_type == "paragraph":
        text_content = extract_text(block_data.get("rich_text", []))
        return f"{text_content}\n" if text_content else ""
    
    elif block_type == "heading_1":
        text_content = extract_text(block_data.get("rich_text", []))
        return f"# {text_content}\n\n"
    
    elif block_type == "heading_2":
        text_content = extract_text(block_data.get("rich_text", []))
        return f"## {text_content}\n\n"
    
    elif block_type == "heading_3":
        text_content = extract_text(block_data.get("rich_text", []))
        return f"### {text_content}\n\n"
    
    elif block_type == "bulleted_list_item":
        text_content = extract_text(block_data.get("rich_text", []))
        return f"- {text_content}\n"
    
    elif block_type == "numbered_list_item":
        text_content = extract_text(block_data.get("rich_text", []))
        return f"1. {text_content}\n"
    
    elif block_type == "code":
        text_content = extract_text(block_data.get("rich_text", []))
        language = block_data.get("language", "")
        return f"```{language}\n{text_content}\n```\n\n"
    
    elif block_type == "quote":
        text_content = extract_text(block_data.get("rich_text", []))
        return f"> {text_content}\n"
    
    elif block_type == "divider":
        return "---\n\n"
    
    elif block_type == "table":
        # 간단한 테이블 처리
        return "[테이블 블록]\n\n"
    
    elif block_type == "image":
        # 이미지 블록
        return "[이미지 블록]\n\n"
    
    else:
        return f"[{block_type}]\n"

def pages_to_markdown(pages):
    """페이지들을 마크다운 파일로 변환"""
    print(f"\n📝 {len(pages)}개 페이지를 마크다운으로 변환 중...\n")
    
    for idx, page in enumerate(pages, 1):
        page_id = page.get("id")
        properties = page.get("properties", {})
        
        # 제목 추출
        title_prop = properties.get("제목", {})
        title = extract_text(title_prop.get("title", []))
        
        if not title:
            title = f"Untitled_{page_id[:8]}"
        
        # 파일명 생성 (한글 지원)
        filename = f"{title}.md"
        filepath = os.path.join(OUTPUT_DIR, filename)
        
        # 페이지 콘텐츠 조회
        blocks = get_page_content(page_id)
        
        # 마크다운 생성
        markdown_content = f"# {title}\n\n"
        
        # 메타데이터 추가
        markdown_content += f"> **생성일:** {properties.get('생성 일시', {}).get('created_time', 'N/A')}\n"
        markdown_content += f"> **수정일:** {properties.get('최종 편집 일시', {}).get('last_edited_time', 'N/A')}\n\n"
        
        # 블록 변환
        for block in blocks:
            markdown_content += block_to_markdown(block)
        
        # 파일 저장
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(markdown_content)
            print(f"✅ [{idx}/{len(pages)}] {filename}")
        except Exception as e:
            print(f"❌ [{idx}/{len(pages)}] {filename} - 오류: {e}")
    
    print(f"\n✅ 완료! {OUTPUT_DIR} 에 {len(pages)}개 파일이 저장되었습니다.")

def main():
    print("🚀 Notion 크롤러 시작\n")
    
    # 출력 디렉토리 생성
    create_output_dir()
    
    # 모든 페이지 조회
    print("\n📥 데이터베이스에서 페이지 조회 중...")
    pages = get_all_pages(DB_ID)
    print(f"\n총 {len(pages)}개 페이지 조회됨\n")
    
    # 마크다운으로 변환
    pages_to_markdown(pages)

if __name__ == "__main__":
    main()
