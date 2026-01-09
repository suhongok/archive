#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Obsidian 파일 간 연관성 기반 링크 자동 생성 스크립트
내용 유사도와 주제를 기반으로 마크다운 파일 간의 wiki link를 생성합니다.
"""

import os
import re
from pathlib import Path
from collections import defaultdict
from difflib import SequenceMatcher
import json

class ObsidianLinkGenerator:
    def __init__(self, vault_path):
        self.vault_path = Path(vault_path)
        self.files = {}
        self.keywords_map = defaultdict(list)
        self.project_categories = {
            '사이버트럭': ['사이버트럭', 'cybertruck', 'LED', '초음파'],
            '지게차': ['지게차', '컨트롤박스', 'forklift'],
            '라즈베리파이': ['라즈베리파이', 'raspberry', 'GPIO', 'RPi'],
            '드론': ['드론', 'drone', '자율주행', 'autonomy'],
            '센서': ['센서', 'sensor', '온습도', 'ToF', 'DHT', 'LED', '초음파'],
            '모터제어': ['모터', 'motor', 'DC모터', '서보', 'motor control'],
            '네트워크': ['네트워크', 'network', 'wifi', 'WiFi', 'AP', 'hostapd', 'DNS'],
            'IoT시스템': ['IoT', 'node-red', '스마트팜', 'smartfarm', 'mqtt'],
            '이미지인식': ['이미지', 'image', '인식', '검출', 'detection', 'recognition'],
            '농업': ['농업', 'farm', '농작물', '비닐하우스', '스마트팜'],
        }
        
    def load_files(self):
        """vault의 모든 마크다운 파일 로드"""
        for file_path in self.vault_path.glob('**/*.md'):
            # .obsidian 폴더 제외
            if '.obsidian' in str(file_path):
                continue
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                relative_path = file_path.relative_to(self.vault_path)
                self.files[str(relative_path)] = {
                    'path': file_path,
                    'content': content,
                    'name': file_path.stem,
                    'size': len(content)
                }
            except Exception as e:
                print(f"파일 로드 실패: {file_path} - {e}")
    
    def extract_keywords(self, content):
        """파일 내용에서 주요 키워드 추출"""
        keywords = set()
        
        # 제목에서 추출
        titles = re.findall(r'^#+\s+(.+)$', content, re.MULTILINE)
        for title in titles:
            keywords.add(title.lower().strip())
        
        # 프로젝트 카테고리 확인
        for category, keywords_list in self.project_categories.items():
            for kw in keywords_list:
                if kw.lower() in content.lower():
                    keywords.add(category)
                    break
        
        # 날짜 추출 (연관성 판단에 사용)
        dates = re.findall(r'\d{1,2}월\s+\d{1,2}일', content)
        if dates:
            keywords.add(f"날짜_{dates[0]}")
        
        return keywords
    
    def find_related_files(self, source_file, min_similarity=0.15):
        """유사한 파일들 찾기"""
        source_content = self.files[source_file]['content'].lower()
        source_keywords = self.extract_keywords(self.files[source_file]['content'])
        
        related = []
        
        for target_file, file_info in self.files.items():
            if source_file == target_file:
                continue
            
            target_content = file_info['content'].lower()
            target_keywords = self.extract_keywords(file_info['content'])
            
            # 공통 키워드 개수
            common_keywords = len(source_keywords & target_keywords)
            
            # 내용 유사도 계산 (긴 파일의 경우 일부만 비교)
            snippet_size = min(200, len(source_content) // 2)
            similarity = SequenceMatcher(None, 
                                        source_content[:snippet_size], 
                                        target_content[:snippet_size]).ratio()
            
            # 점수 계산
            score = common_keywords * 0.7 + similarity * 0.3
            
            if score > min_similarity or common_keywords > 0:
                related.append({
                    'file': target_file,
                    'name': file_info['name'],
                    'score': score,
                    'common_keywords': common_keywords
                })
        
        # 점수 기준 정렬
        related.sort(key=lambda x: x['score'], reverse=True)
        return related[:5]  # 상위 5개만
    
    def exists_link(self, content, target_name):
        """파일에 이미 해당 링크가 있는지 확인"""
        # [[filename]] 형식 확인
        if f"[[{target_name}]]" in content:
            return True
        # 경로 포함 형식 [[folder/filename]] 확인
        if f"[[" in content and target_name in content:
            return True
        return False
    
    def add_links_to_file(self, file_path, related_files, dry_run=True):
        """파일에 링크 추가"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            new_content = content
            links_added = []
            
            # 참고 섹션 찾기 또는 생성
            if '\n## 📎 연관 문서' not in content:
                new_content += '\n\n## 📎 연관 문서\n\n'
            
            # 기존 링크 섹션 찾기
            if '## 📎 연관 문서' in new_content:
                section_start = new_content.find('## 📎 연관 문서')
                # 섹션 끝 찾기 (다음 ## 또는 파일 끝)
                next_section = new_content.find('\n##', section_start + 1)
                if next_section == -1:
                    section_end = len(new_content)
                else:
                    section_end = next_section
                
                links_section = new_content[section_start:section_end]
                
                for rel_file in related_files:
                    if not self.exists_link(links_section, rel_file['name']):
                        new_link = f"\n- [[{rel_file['name']}]] - {rel_file['common_keywords']}개 공통 주제"
                        new_content = new_content[:section_end] + new_link + new_content[section_end:]
                        links_added.append(rel_file['name'])
            
            if not dry_run and links_added:
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                return len(links_added)
            
            return len(links_added)
        
        except Exception as e:
            print(f"링크 추가 실패 {file_path}: {e}")
            return 0
    
    def generate_report(self):
        """분석 보고서 생성"""
        report = {
            'total_files': len(self.files),
            'file_relationships': {}
        }
        
        for source_file in self.files:
            related = self.find_related_files(source_file)
            if related:
                report['file_relationships'][self.files[source_file]['name']] = [
                    {
                        'related': r['name'],
                        'score': round(r['score'], 3),
                        'common_keywords': r['common_keywords']
                    }
                    for r in related
                ]
        
        return report

def main():
    vault_path = '/home/sm/archive'
    generator = ObsidianLinkGenerator(vault_path)
    
    print("📚 Obsidian 링크 생성기 시작...")
    print(f"📁 Vault 경로: {vault_path}")
    
    # 1단계: 파일 로드
    print("\n📖 파일 로드 중...")
    generator.load_files()
    print(f"✅ {len(generator.files)}개 파일 로드 완료")
    
    # 2단계: 분석 보고서 생성
    print("\n🔍 파일 관계 분석 중...")
    report = generator.generate_report()
    
    # 결과 출력
    print("\n📊 분석 결과:")
    print(f"총 파일: {report['total_files']}")
    
    print("\n🔗 추천 링크:")
    for file_name, relationships in sorted(report['file_relationships'].items()):
        print(f"\n📄 {file_name}")
        for rel in relationships[:3]:
            print(f"   → [[{rel['related']}]] (점수: {rel['score']}, 공통주제: {rel['common_keywords']})")
    
    # 3단계: 링크 추가 (실제 적용)
    print("\n\n🔗 파일에 링크 추가 중...")
    total_links = 0
    modified_files = []
    
    for source_file in generator.files.keys():
        related = generator.find_related_files(source_file)
        if related:
            links = generator.add_links_to_file(
                generator.files[source_file]['path'], 
                related, 
                dry_run=False  # 실제 적용
            )
            if links > 0:
                total_links += links
                modified_files.append(generator.files[source_file]['name'])
    
    print(f"\n✅ 총 {total_links}개 링크 추가됨")
    print(f"✅ {len(modified_files)}개 파일 수정됨")
    
    if modified_files:
        print("\n수정된 파일 목록 (처음 20개):")
        for fname in modified_files[:20]:
            print(f"  • {fname}")

if __name__ == '__main__':
    main()
