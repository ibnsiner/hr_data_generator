"""
GDB 기반 HR 챗봇 프로젝트 - 일반적인 HR 데이터 생성 스크립트
200명 규모 조직의 다양한 HR 데이터셋 25종 생성 (채용 전형 검사 포함)
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os
import subprocess
import sys

# Faker 모듈 자동 설치 및 import
try:
    from faker import Faker
    fake = Faker('ko_KR')
    Faker.seed(42)
    FAKER_AVAILABLE = True
except ImportError:
    print("Faker 모듈이 설치되어 있지 않습니다. 자동 설치를 시도합니다...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 'faker'])
        from faker import Faker
        fake = Faker('ko_KR')
        Faker.seed(42)
        FAKER_AVAILABLE = True
        print("Faker 모듈 설치 완료!")
    except Exception as e:
        print(f"Faker 자동 설치 실패: {e}")
        print("한글 이름 생성 대체 로직을 사용합니다.")
        FAKER_AVAILABLE = False
        
        # Faker 대체 클래스 (간단한 한글 이름 생성)
        class SimpleFaker:
            def __init__(self):
                self.last_names = ['김', '이', '박', '최', '정', '강', '조', '윤', '장', '임', '한', '오', '서', '신', '권', '황', '안', '송', '류', '홍']
                self.first_names_male = ['민준', '서준', '도윤', '예준', '시우', '주원', '하준', '지호', '준서', '건우', '우진', '현우', '선우', '연우', '유준', '정우', '승우', '승현', '시윤', '준혁']
                self.first_names_female = ['서연', '서윤', '지우', '서현', '민서', '하은', '하윤', '윤서', '지유', '채원', '지민', '수아', '다은', '예은', '소율', '예린', '지안', '수빈', '시은', '소윤']
                random.seed(42)
            
            def name(self):
                last = random.choice(self.last_names)
                first = random.choice(self.first_names_male + self.first_names_female)
                return f"{last}{first}"
            
            def date_of_birth(self, minimum_age=25, maximum_age=60):
                from datetime import datetime
                current_year = 2024
                birth_year = current_year - random.randint(minimum_age, maximum_age)
                birth_month = random.randint(1, 12)
                birth_day = random.randint(1, 28)
                return datetime(birth_year, birth_month, birth_day)
            
            def date_between(self, start_date='-10y', end_date='today'):
                # 간단한 구현: -10y 같은 형식을 파싱
                if 'y' in start_date:
                    years_ago = int(start_date.replace('-', '').replace('y', ''))
                    start = datetime.now() - timedelta(days=years_ago * 365)
                else:
                    start = datetime.now() - timedelta(days=3650)  # 기본 10년
                
                if 'y' in end_date:
                    years_ago = int(end_date.replace('-', '').replace('y', ''))
                    end = datetime.now() - timedelta(days=years_ago * 365)
                else:
                    end = datetime.now()
                
                time_between = (end - start).days
                random_days = random.randint(0, time_between)
                return start + timedelta(days=random_days)
        
        fake = SimpleFaker()

np.random.seed(42)
random.seed(42)

# 출력 디렉토리 생성
os.makedirs('data', exist_ok=True)

print("=" * 80)
print("GDB-HR 프로젝트 데이터 생성 시작 (200명 규모 + 채용 전형 검사)")
print("=" * 80)

# ============================================================================
# 채용 전형 검사 메타데이터 정의
# ============================================================================

# CPI (California Personality Inventory) 메타데이터
CPI_METADATA = {
    "description": "캘리포니아 성격 검사(CPI)는 개인의 성격 특성을 다차원적으로 이해하고 예측하기 위해 사용되는 검사입니다.",
    "scales": {
        # 1군: 대인관계 및 자신감
        "Do": {"name": "지배성", "name_en": "Dominance", "group": "대인관계및자신감", 
               "definition": "리더십, 주도성, 자신감을 측정합니다."},
        "Cs": {"name": "지위추구성", "name_en": "Capacity for Status", "group": "대인관계및자신감",
               "definition": "사회적 지위를 얻고자 하는 욕구를 평가합니다."},
        "Sy": {"name": "사교성", "name_en": "Sociability", "group": "대인관계및자신감",
               "definition": "사교적이고 외향적인 성향을 측정합니다."},
        "Sp": {"name": "사회적존재감", "name_en": "Social Presence", "group": "대인관계및자신감",
               "definition": "대인관계에서 자신감과 자발성을 평가합니다."},
        "Sa": {"name": "자기수용", "name_en": "Self-acceptance", "group": "대인관계및자신감",
               "definition": "자신의 가치와 장점을 인정하는 정도를 측정합니다."},
        "In": {"name": "독립성", "name_en": "Independence", "group": "대인관계및자신감",
               "definition": "자율적이고 독립적으로 생각하고 행동하는 경향을 평가합니다."},
        "Em": {"name": "공감성", "name_en": "Empathy", "group": "대인관계및자신감",
               "definition": "타인의 감정을 이해하고 공유하는 능력을 측정합니다."},
        
        # 2군: 규범 지향성 및 가치관
        "Re": {"name": "책임감", "name_en": "Responsibility", "group": "규범지향성및가치관",
               "definition": "책임감이 있고 신뢰할 만한 정도를 평가합니다."},
        "So": {"name": "사회화", "name_en": "Socialization", "group": "규범지향성및가치관",
               "definition": "사회적 규범과 가치를 내면화한 정도를 측정합니다."},
        "Sc": {"name": "자기통제", "name_en": "Self-control", "group": "규범지향성및가치관",
               "definition": "충동을 억제하고 자신을 통제하는 능력을 평가합니다."},
        "Gi": {"name": "호감성", "name_en": "Good Impression", "group": "규범지향성및가치관",
               "definition": "타인에게 좋은 인상을 주려는 경향을 측정합니다."},
        "Cm": {"name": "공동체성", "name_en": "Communality", "group": "규범지향성및가치관",
               "definition": "일반적인 사람들과 유사하게 반응하는 정도를 평가합니다."},
        "Wb": {"name": "안녕감", "name_en": "Well-being", "group": "규범지향성및가치관",
               "definition": "전반적인 삶의 만족감과 행복감을 측정합니다."},
        "To": {"name": "관용성", "name_en": "Tolerance", "group": "규범지향성및가치관",
               "definition": "타인의 신념이나 태도에 대한 관용적인 태도를 평가합니다."},
        
        # 3군: 성취 잠재력 및 지적 효율성
        "Ac": {"name": "순응을통한성취", "name_en": "Achievement via Conformance", "group": "성취잠재력및지적효율성",
               "definition": "규칙적이고 체계적인 환경에서 성취를 이루는 경향을 측정합니다."},
        "Ai": {"name": "독립을통한성취", "name_en": "Achievement via Independence", "group": "성취잠재력및지적효율성",
               "definition": "독창적이고 자율적인 환경에서 성취를 이루는 경향을 평가합니다."},
        "Ie": {"name": "지적효율성", "name_en": "Intellectual Efficiency", "group": "성취잠재력및지적효율성",
               "definition": "지적 능력을 효율적으로 사용하는 정도를 측정합니다."},
        
        # 4군: 역할 및 개인적 스타일
        "Py": {"name": "심리지향성", "name_en": "Psychological-mindedness", "group": "역할및개인적스타일",
               "definition": "자신과 타인의 내면 및 동기에 대한 관심 정도를 평가합니다."},
        "Fx": {"name": "융통성", "name_en": "Flexibility", "group": "역할및개인적스타일",
               "definition": "변화에 개방적이고 적응을 잘하는 정도를 측정합니다."},
        "FM": {"name": "여성성남성성", "name_en": "Femininity/Masculinity", "group": "역할및개인적스타일",
               "definition": "전통적인 성 역할에 부합하는 관심과 태도를 측정합니다."},
        
        # 벡터척도
        "v1": {"name": "외향성내향성", "name_en": "Extraversion-Introversion", "group": "벡터척도",
               "definition": "외부 세계와 상호작용하는 방식을 측정합니다."},
        "v2": {"name": "규범지향규범회의", "name_en": "Norm-orientation vs Norm-doubting", "group": "벡터척도",
               "definition": "규범을 따르는 정도를 측정합니다."},
        "v3": {"name": "자아실현", "name_en": "Self-realization", "group": "벡터척도",
               "definition": "개인의 통합감과 자아실현 수준을 측정합니다."}
    },
    "lifestyle_types": {
        "Alpha": {"name": "알파형", "definition": "외향적이고 규범을 따르며, 능동적이고 리더십이 강한 실행형"},
        "Beta": {"name": "베타형", "definition": "내향적이고 규범을 따르며, 성실하고 책임감이 강한 협력형"},
        "Gamma": {"name": "감마형", "definition": "외향적이고 규범에 회의적이며, 혁신적이고 즐거움을 추구하는 혁신형"},
        "Delta": {"name": "델타형", "definition": "내향적이고 규범에 회의적이며, 사색적이고 독특한 경향이 있는 사색형"}
    }
}

# MMPI (Minnesota Multiphasic Personality Inventory) 메타데이터
MMPI_METADATA = {
    "description": "미네소타 다면적 인성검사(MMPI)는 개인의 성격 특성과 정신병리를 평가하기 위해 사용되는 심리 검사입니다.",
    "scales": {
        # 타당도 척도
        "L": {"name": "허위척도", "name_en": "Lie Scale", "group": "타당도척도",
              "definition": "자신을 의도적으로 좋게 보이려고 하거나 사회적으로 바람직한 방식으로 응답하는 경향을 측정합니다."},
        "F": {"name": "빈도척도", "name_en": "Frequency Scale", "group": "타당도척도",
              "definition": "일반적인 사람들과 다른 비전형적인 방식으로 응답하는 경향을 탐지합니다."},
        "K": {"name": "교정척도", "name_en": "Correction Scale", "group": "타당도척도",
              "definition": "자신을 방어적으로 드러내지 않으려는 태도를 측정합니다."},
        
        # 임상 척도
        "Hs": {"name": "건강염려증", "name_en": "Hypochondriasis", "group": "임상척도",
               "definition": "신체적 건강에 대한 과도한 염려와 집착을 측정합니다."},
        "D": {"name": "우울증", "name_en": "Depression", "group": "임상척도",
              "definition": "우울감, 비관주의, 무기력감 등 우울 증상과 관련된 특성을 평가합니다."},
        "Hy": {"name": "히스테리", "name_en": "Hysteria", "group": "임상척도",
               "definition": "스트레스 상황에서 신체적 증상을 나타내거나 부인, 억압과 같은 방어기제를 사용하는 경향을 측정합니다."},
        "Pd": {"name": "반사회성", "name_en": "Psychopathic Deviate", "group": "임상척도",
               "definition": "사회적 규범이나 권위에 대한 반항, 충동성, 대인관계에서의 갈등 등을 평가합니다."},
        "Mf": {"name": "남성성여성성", "name_en": "Masculinity-Femininity", "group": "임상척도",
               "definition": "전통적인 성 역할 고정관념과의 일치 정도를 측정합니다."},
        "Pa": {"name": "편집증", "name_en": "Paranoia", "group": "임상척도",
               "definition": "타인에 대한 의심, 민감성, 적대감과 같은 편집성향을 평가합니다."},
        "Pt": {"name": "강박증", "name_en": "Psychasthenia", "group": "임상척도",
               "definition": "불안, 걱정, 강박적 사고, 결단력 부족과 관련된 특성을 측정합니다."},
        "Sc": {"name": "정신분열병", "name_en": "Schizophrenia", "group": "임상척도",
               "definition": "혼란스러운 사고, 비현실감, 사회적 소외감 등 정신분열 스펙트럼과 관련된 특징을 평가합니다."},
        "Ma": {"name": "경조증", "name_en": "Hypomania", "group": "임상척도",
               "definition": "과잉 활동, 충동성, 흥분, 과대사고 등 경조증적 경향을 측정합니다."},
        "Si": {"name": "사회적내향성", "name_en": "Social Introversion", "group": "임상척도",
               "definition": "사교 상황에서의 불편감, 내향성, 사회적 회피 경향을 평가합니다."}
    }
}

# 적성검사 메타데이터
APTITUDE_METADATA = {
    "description": "직무 수행에 필요한 잠재적 능력을 다양한 요인을 통해 측정하는 검사입니다.",
    "factors": {
        # 언어적 능력
        "verbal_total": {"name": "언어적능력", "group": "상위요인", 
                        "definition": "어휘, 문장 구성 및 해독 등 언어와 관련된 종합적인 능력을 평가합니다."},
        "verbal_vocab": {"name": "어휘능력", "group": "언어적능력", 
                        "definition": "어휘의 의미를 정확히 이해하고 활용하는 능력입니다."},
        "verbal_composition": {"name": "문장구성력", "group": "언어적능력",
                              "definition": "문법에 맞고 논리적인 문장을 구성하는 능력입니다."},
        "verbal_decoding": {"name": "문장해독력", "group": "언어적능력",
                           "definition": "복잡한 문장의 의미를 정확히 파악하는 능력입니다."},
        "verbal_english": {"name": "영어능력", "group": "언어적능력",
                          "definition": "영어 독해 및 활용 능력입니다."},
        
        # 수리적 능력
        "numerical_total": {"name": "수리적능력", "group": "상위요인",
                           "definition": "수량 및 통계 자료를 이해하고 논리적으로 사고하는 능력을 평가합니다."},
        "numerical_quantity": {"name": "수량적처리능력", "group": "수리적능력",
                              "definition": "수치 데이터를 빠르고 정확하게 처리하는 능력입니다."},
        "numerical_statistics": {"name": "통계적처리능력", "group": "수리적능력",
                                "definition": "통계적 개념을 이해하고 적용하는 능력입니다."},
        "numerical_logic": {"name": "논리적사고능력", "group": "수리적능력",
                           "definition": "논리적 추론과 문제 해결 능력입니다."},
        
        # 상황판단 능력
        "situational_judgment": {"name": "상황판단능력", "group": "상위요인",
                                "definition": "조직 생활에서 발생 가능한 상황을 정확하게 판단하는 능력입니다."},
        
        # 사회적 상식
        "social_knowledge": {"name": "사회적상식", "group": "상위요인",
                            "definition": "사회 구성원으로서 최소한의 상식을 갖추고 있는 정도입니다."},
        
        # 대인관계능력
        "interpersonal_skills": {"name": "대인관계능력", "group": "상위요인",
                                "definition": "타인과 원활한 관계를 형성하고 유지하는 능력입니다."}
    }
}

# ============================================================================
# A그룹: 마스터 데이터 (Master Data)
# ============================================================================

# 0-1. organization_structure.csv - 조직 구조 (부서 간 위계)
print("\n[0-1/25] organization_structure.csv 생성 중...")

organization_structure = [
    # org_id, org_name, org_type, parent_org_id, level, head_employee_id
    ('ORG000', '넥스트젠 테크놀로지스', 'Company', None, 0, 'EMP000'),
    
    # 본부 (Level 1)
    ('ORG100', '경영지원본부', 'Division', 'ORG000', 1, 'DIV001'),
    ('ORG200', '기술본부', 'Division', 'ORG000', 1, 'DIV002'),
    ('ORG300', '비즈니스본부', 'Division', 'ORG000', 1, 'DIV003'),
    
    # 경영지원본부 산하 팀 (Level 2)
    ('ORG101', 'HR팀', 'Team', 'ORG100', 2, 'TL001'),
    ('ORG102', '재무팀', 'Team', 'ORG100', 2, 'TL002'),
    
    # 기술본부 산하 팀 (Level 2)
    ('ORG201', 'AI솔루션개발팀', 'Team', 'ORG200', 2, 'TL003'),
    ('ORG202', '플랫폼개발팀', 'Team', 'ORG200', 2, 'TL004'),
    ('ORG203', '데이터분석팀', 'Team', 'ORG200', 2, 'TL005'),
    ('ORG204', 'IT기획팀', 'Team', 'ORG200', 2, 'TL006'),
    ('ORG205', 'UI/UX디자인팀', 'Team', 'ORG200', 2, 'TL007'),
    ('ORG206', 'QA팀', 'Team', 'ORG200', 2, 'TL008'),
    
    # 비즈니스본부 산하 팀 (Level 2)
    ('ORG301', '마케팅팀', 'Team', 'ORG300', 2, 'TL009'),
    ('ORG302', '영업팀', 'Team', 'ORG300', 2, 'TL010'),
]

df_org_structure = pd.DataFrame(organization_structure, columns=[
    'org_id', 'org_name', 'org_type', 'parent_org_id', 'level', 'head_employee_id'
])
df_org_structure.to_csv('data/00_organization_structure.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_org_structure)}개 조직 단위 생성 완료")

# ============================================================================
# 1. hr_metrics_definition.csv - 평가 지표 사전
print("\n[1/25] hr_metrics_definition.csv 생성 중...")

metrics_data = [
    # 스킬 역량 (상세 정의 확장)
    ['SKILL_001', '데이터 분석', 'Competency Framework', 'Technical Skill', 
     '대량의 데이터를 수집, 정제, 분석하여 비즈니스 인사이트를 도출하고 의사결정을 지원하는 능력. 통계적 분석, 데이터 시각화, 패턴 인식을 포함함', '1-5점 척도',
     '복잡한 데이터에서 핵심 인사이트 도출, 예측 모델 구축, 데이터 기반 전략 수립, 고급 분석 도구 활용',
     '기초적 데이터 처리만 가능, 분석 결과 해석 어려움, 단순 집계 수준, 데이터 품질 검증 미흡'],
    
    ['SKILL_002', '커뮤니케이션', 'Competency Framework', 'Soft Skill',
     '다양한 이해관계자와 명확하고 효과적으로 의사소통하는 능력. 경청, 설득, 프레젠테이션, 문서 작성, 갈등 조정을 포함함', '1-5점 척도',
     '복잡한 내용을 명확히 전달, 이해관계자 설득, 갈등 중재, 효과적 프레젠테이션, 문서화 우수',
     '의사전달 불분명, 오해 빈발, 소극적 의견 표현, 문서 작성 미흡, 갈등 상황 회피'],
    
    ['SKILL_003', 'Python 프로그래밍', 'Competency Framework', 'Technical Skill',
     'Python 언어를 활용한 소프트웨어 개발, 데이터 처리, 자동화 스크립트 작성 능력. 라이브러리 활용, 코드 최적화, 디버깅 포함', '1-5점 척도',
     '고급 라이브러리 활용, 효율적 알고리즘 구현, 복잡한 시스템 개발, 코드 리뷰 및 멘토링',
     '기본 문법만 이해, 단순 스크립트 작성, 라이브러리 의존도 높음, 디버깅 어려움'],
    
    ['SKILL_004', '프로젝트 관리', 'Competency Framework', 'Management Skill',
     '프로젝트의 계획 수립부터 완료까지 전 과정을 체계적으로 관리하는 능력. 일정 관리, 자원 배분, 위험 관리, 품질 관리를 포함함', '1-5점 척도',
     '복잡한 프로젝트 성공적 완수, 일정 단축 달성, 예산 절감, 팀 생산성 향상, 위험 사전 대응',
     '일정 지연 빈발, 예산 초과, 품질 기준 미달, 팀 갈등 관리 미흡, 위험 대응 부족'],
    
    ['SKILL_005', '협업', 'Competency Framework', 'Soft Skill',
     '다양한 부서 및 팀원들과 효과적으로 협력하여 공동 목표를 달성하는 능력. 팀워크, 지식 공유, 상호 지원, 시너지 창출을 포함함', '1-5점 척도',
     '크로스팀 협업 주도, 지식 공유 활발, 갈등 해결 기여, 팀 시너지 창출, 협업 문화 조성',
     '개인 업무 위주, 정보 공유 소극적, 타 부서와 소통 부족, 협업 회피, 사일로 현상'],
    
    ['SKILL_006', '문제 해결', 'Competency Framework', 'Soft Skill',
     '복잡하고 모호한 문제를 체계적으로 분석하고 창의적이며 실용적인 해결책을 도출하는 능력. 논리적 사고, 창의적 접근, 대안 모색을 포함함', '1-5점 척도',
     '복잡한 문제 신속 해결, 창의적 솔루션 제시, 근본 원인 파악, 예방적 조치 수립, 문제 해결 프로세스 개선',
     '문제 인식 부족, 표면적 해결, 반복적 문제 발생, 해결책 부족, 문제 회피 경향'],
    
    ['SKILL_007', '기술 전문성', 'Competency Framework', 'Technical Skill',
     '담당 분야의 깊이 있는 기술적 지식과 실무 경험을 바탕으로 한 전문성. 최신 기술 동향 파악, 기술적 의사결정, 기술 멘토링을 포함함', '1-5점 척도',
     '업계 최신 기술 선도, 기술적 의사결정 주도, 전문가로 인정, 기술 멘토링 제공, 혁신 기술 도입',
     '기본 기술만 보유, 최신 동향 파악 부족, 기술적 판단 미흡, 의존적 업무 수행, 학습 의지 부족'],
    
    ['SKILL_008', '학습 민첩성', 'Competency Framework', 'Soft Skill',
     '변화하는 환경에서 새로운 기술, 지식, 스킬을 빠르게 습득하고 적용하는 능력. 자기주도 학습, 적응력, 성장 마인드를 포함함', '1-5점 척도',
     '신기술 빠른 습득, 자기주도 학습, 변화 적응 우수, 지속적 성장, 학습 내용 실무 적용',
     '학습 속도 느림, 변화 저항, 기존 방식 고수, 새로운 도전 회피, 성장 정체'],
    
    ['SKILL_009', '비즈니스 이해도', 'Competency Framework', 'Business Skill',
     '조직의 비즈니스 모델, 시장 환경, 고객 니즈를 이해하고 업무에 적용하는 능력. 시장 분석, 고객 관점, 수익성 고려를 포함함', '1-5점 척도',
     '시장 트렌드 파악, 고객 니즈 이해, 비즈니스 임팩트 고려, 수익성 개선 기여, 전략적 사고',
     '기술 중심 사고, 비즈니스 맥락 이해 부족, 고객 관점 부재, 단순 업무 처리, 시장 변화 무관심'],
    
    ['SKILL_010', '창의성', 'Competency Framework', 'Soft Skill',
     '기존 관념에서 벗어나 새롭고 독창적인 아이디어를 창출하고 실행하는 능력. 혁신적 사고, 아이디어 구현, 실험 정신을 포함함', '1-5점 척도',
     '혁신적 아이디어 제시, 창의적 솔루션 개발, 새로운 접근법 시도, 실험 정신, 변화 주도',
     '관습적 사고, 새로운 시도 부족, 아이디어 부족, 변화 저항, 안전한 방법만 선호'],
    
    # 리더십 역량 (상세 정의 확장)
    ['LEAD_001', '전략적 비전 제시', 'Leadership 360', 'Strategic Leadership',
     '조직의 장기적 방향성과 비전을 수립하고 구성원들에게 명확히 전달하여 공감대를 형성하는 능력. 미래 예측, 전략 수립, 비전 소통을 포함함', '1-5점 척도',
     '명확한 비전 제시, 전략적 방향 설정, 구성원 공감대 형성, 미래 트렌드 예측, 조직 변화 주도',
     '비전 부재, 단기적 사고, 방향성 불분명, 구성원 혼란, 전략적 사고 부족'],
    
    ['LEAD_002', '팀 육성 및 개발', 'Leadership 360', 'People Leadership',
     '팀원 개개인의 강점을 파악하고 성장할 수 있도록 지원하며 팀 전체의 역량을 향상시키는 능력. 개인 개발, 팀 빌딩, 성장 지원을 포함함', '1-5점 척도',
     '개인별 맞춤 육성, 성장 기회 제공, 팀 역량 향상, 후계자 양성, 학습 문화 조성',
     '팀원 방치, 개발 기회 부족, 획일적 관리, 성장 지원 미흡, 개인 특성 무시'],
    
    ['LEAD_003', '의사결정 능력', 'Leadership 360', 'Strategic Leadership',
     '복잡한 상황에서 충분한 정보를 수집하고 분석하여 적시에 효과적인 의사결정을 내리는 능력. 정보 분석, 대안 평가, 결정 실행을 포함함', '1-5점 척도',
     '신속하고 정확한 판단, 데이터 기반 의사결정, 리스크 고려, 결과에 대한 책임, 결정 실행력',
     '의사결정 지연, 우유부단함, 정보 부족한 판단, 책임 회피, 결정 번복 빈발'],
    
    ['LEAD_004', '변화 관리', 'Leadership 360', 'Change Leadership',
     '조직 내 변화를 계획하고 실행하며 구성원들의 변화 저항을 최소화하고 적응을 돕는 능력. 변화 계획, 저항 관리, 적응 지원을 포함함', '1-5점 척도',
     '변화 주도, 저항 극복, 구성원 설득, 변화 정착, 지속적 개선 문화',
     '변화 저항, 현상 유지 선호, 구성원 설득 실패, 변화 계획 부실, 추진력 부족'],
    
    ['LEAD_005', '코칭 및 피드백', 'Leadership 360', 'People Leadership',
     '팀원의 성과와 행동에 대해 건설적이고 구체적인 피드백을 제공하고 성장을 위한 코칭을 하는 능력. 성과 피드백, 행동 코칭, 개발 지원을 포함함', '1-5점 척도',
     '구체적 피드백 제공, 성장 지향 코칭, 강점 개발 지원, 개선점 명확 제시, 지속적 관심',
     '피드백 회피, 추상적 조언, 일방적 지시, 개발 지원 부족, 관심 부족'],
    
    ['LEAD_006', '신뢰 구축', 'Leadership 360', 'People Leadership',
     '일관된 행동과 투명한 소통을 통해 팀원들과 상호 신뢰 관계를 형성하고 유지하는 능력. 진정성, 일관성, 투명성, 약속 이행을 포함함', '1-5점 척도',
     '높은 신뢰도, 약속 이행, 투명한 소통, 일관된 행동, 팀원 존중, 진정성 있는 관계',
     '신뢰도 낮음, 약속 불이행, 불투명한 소통, 일관성 부족, 편파적 대우, 형식적 관계'],
    
    ['LEAD_007', '임파워먼트', 'Leadership 360', 'People Leadership',
     '팀원에게 적절한 권한과 책임을 위임하고 자율적으로 업무를 수행할 수 있도록 지원하는 능력. 권한 위임, 자율성 부여, 책임감 부여를 포함함', '1-5점 척도',
     '적절한 권한 위임, 자율적 업무 환경, 책임감 부여, 의사결정 참여 기회, 성장 기회 제공',
     '과도한 통제, 미시 관리, 권한 위임 부족, 의사결정 독점, 자율성 제한'],
    
    # 성과 지표 (상세 정의 확장)
    ['PERF_001', '업무 성과', 'Performance Review', 'Result',
     '설정된 목표와 KPI 대비 실제 달성한 성과의 정도. 양적 목표 달성, 질적 기준 충족, 기한 준수, 예산 효율성을 종합 평가', 'S/A/B/C/D 등급',
     'S등급: 목표 130% 이상 달성, 혁신적 성과, 조직 기여도 탁월 | A등급: 목표 110-129% 달성, 우수한 성과',
     'D등급: 목표 70% 미만, 기본 업무 미달 | C등급: 목표 70-89% 달성, 개선 필요'],
    
    ['PERF_002', '업무 효율성', 'Performance Review', 'Process',
     '주어진 시간, 인력, 예산 등 제한된 자원을 최적으로 활용하여 최대의 성과를 창출하는 능력. 시간 관리, 자원 활용, 프로세스 개선을 포함함', '1-5점 척도',
     '높은 생산성, 시간 관리 우수, 자원 최적 활용, 프로세스 개선, 업무 자동화 도입',
     '낮은 생산성, 시간 관리 부족, 자원 낭비, 비효율적 프로세스, 반복 업무 개선 미흡'],
    
    ['PERF_003', '창의성 및 혁신', 'Performance Review', 'Innovation',
     '기존 방식에서 벗어나 새로운 아이디어와 혁신적 접근법을 제시하고 실행하는 능력. 아이디어 창출, 혁신 실행, 개선 제안을 포함함', '1-5점 척도',
     '혁신적 아이디어 다수 제안, 새로운 방법론 도입, 프로세스 혁신, 창의적 문제 해결, 변화 주도',
     '관습적 업무 수행, 새로운 시도 부족, 개선 제안 없음, 변화 저항, 안전한 방법만 선호'],
    
    # 조직몰입도 관련 (상세 정의 확장)
    ['ENG_001', '직무 만족도', 'Engagement Survey', 'Job Satisfaction',
     '현재 수행하는 업무의 내용, 난이도, 의미, 성취감에 대한 전반적 만족도. 업무 흥미, 성취감, 의미감, 도전감을 포함함', '1-5점 척도',
     '업무에 대한 높은 흥미, 성취감 충만, 일의 의미 인식, 적절한 도전, 전문성 발휘 기회',
     '업무 흥미 부족, 성취감 낮음, 일의 의미 부재, 과소/과도한 업무량, 전문성 활용 기회 부족'],
    
    ['ENG_002', '상사와의 관계', 'Engagement Survey', 'Manager Relationship',
     '직속 상사와의 업무적, 인간적 관계에 대한 만족도. 소통 품질, 지원 정도, 신뢰 관계, 성장 지원을 포함함', '1-5점 척도',
     '원활한 소통, 적극적 지원, 높은 신뢰, 성장 기회 제공, 공정한 평가, 인간적 배려',
     '소통 단절, 지원 부족, 신뢰 부족, 성장 기회 제한, 불공정한 대우, 관계 갈등'],
    
    ['ENG_003', '이직 의도', 'Engagement Survey', 'Retention',
     '현재 조직을 떠나 다른 직장으로 이직하려는 의도의 강도. 조직 만족도, 커리어 전망, 대안 탐색을 반영함', '1-5점 척도',
     '높은 점수: 적극적 이직 준비, 대안 탐색 중, 조직 불만족, 커리어 정체감, 외부 기회 모색',
     '낮은 점수: 조직 만족, 장기 근무 의향, 성장 기회 인식, 조직 애착, 안정적 관계'],
    
    # Big-5 성격검사 요인들 (상세 정의 추가)
    ['BIG5_OPENNESS', '개방성', 'Big-5 성격검사', 'Personality',
     '새로운 경험과 아이디어에 대한 개방성과 호기심을 측정하는 성격 요인. 창의성, 상상력, 지적 호기심, 예술적 감수성, 변화 수용성을 포함함', '0-100점 척도',
     '높은 창의성과 상상력, 새로운 아이디어 수용, 예술적 감수성, 지적 호기심 왕성, 변화와 다양성 추구, 독창적 사고, 실험 정신',
     '보수적 사고, 새로운 것 기피, 예술적 관심 부족, 호기심 부족, 변화 저항, 관습적 접근, 안전한 선택 선호'],
    
    ['BIG5_CONSCIENTIOUSNESS', '성실성', 'Big-5 성격검사', 'Personality',
     '목표 지향적이고 자기 통제력이 있으며 조직적인 성향을 측정하는 성격 요인. 책임감, 근면성, 계획성, 자기 통제, 목표 지향성을 포함함', '0-100점 척도',
     '높은 책임감과 근면성, 체계적이고 조직적, 목표 지향적, 자기 통제력 우수, 계획적 행동, 성취 지향, 신뢰성 높음',
     '책임감 부족, 게으름, 비조직적, 목표 의식 부족, 자기 통제력 부족, 즉흥적 행동, 신뢰성 낮음'],
    
    ['BIG5_EXTRAVERSION', '외향성', 'Big-5 성격검사', 'Personality',
     '사회적 상황에서의 활동성과 에너지 수준을 측정하는 성격 요인. 사교성, 활동성, 자극 추구, 긍정적 정서, 주도성을 포함함', '0-100점 척도',
     '사교적이고 활동적, 에너지 넘침, 자극 추구, 긍정적 정서, 주도적 행동, 사람들과 함께 있기 선호, 외부 활동 적극적',
     '내향적이고 조용함, 에너지 절약, 자극 회피, 신중한 정서, 수동적 행동, 혼자 있기 선호, 내부 활동 선호'],
    
    ['BIG5_AGREEABLENESS', '친화성', 'Big-5 성격검사', 'Personality',
     '타인에 대한 신뢰와 협력적 태도를 측정하는 성격 요인. 신뢰성, 협력성, 배려심, 겸손함, 관용성을 포함함', '0-100점 척도',
     '높은 신뢰성과 협력성, 배려심 많음, 겸손하고 관용적, 타인 도움 적극적, 갈등 회피, 조화 추구, 팀워크 우수',
     '의심 많고 경쟁적, 배려심 부족, 자기중심적, 타인 도움 소극적, 갈등 유발, 대립적 태도, 개인주의'],
    
    ['BIG5_NEUROTICISM', '신경증', 'Big-5 성격검사', 'Personality',
     '정서적 불안정성과 부정적 감정의 경험 정도를 측정하는 성격 요인. 불안, 우울, 분노, 스트레스 취약성, 감정 변화를 포함함', '0-100점 척도',
     '높은 점수: 정서적 불안정, 스트레스 취약, 불안과 걱정 많음, 기분 변화 심함, 부정적 감정 빈발, 압박감 높음',
     '낮은 점수: 정서적 안정, 스트레스 저항력, 평온하고 차분함, 기분 안정, 긍정적 감정, 압박감 적음'],
]

# 채용 검사 지표들 추가 (상세 정의 포함)

# CPI 지표들 (상세 특성 정의)
cpi_detailed_definitions = {
    'Do': ('리더십과 주도성을 측정하는 척도. 타인을 이끌고 영향을 미치려는 경향, 자신감, 결단력을 평가함',
           '강한 리더십, 주도적 행동, 자신감 넘침, 결단력 있음, 영향력 발휘, 책임감 강함, 도전적 과제 선호',
           '수동적 태도, 리더십 회피, 자신감 부족, 우유부단함, 타인 의존적, 책임 회피, 안전한 업무 선호'),
    'Cs': ('사회적 지위와 성공에 대한 욕구를 측정하는 척도. 출세 지향성, 성취 동기, 사회적 인정 추구를 평가함',
           '출세 욕구 강함, 성취 지향적, 사회적 인정 추구, 경쟁심 강함, 목표 지향적, 성공 의지',
           '출세 욕구 낮음, 현상 만족, 경쟁 회피, 안정 추구, 소극적 태도, 성취 동기 부족'),
    'Sy': ('사교적이고 외향적인 성향을 측정하는 척도. 대인관계 선호, 사교 활동, 외향성을 평가함',
           '사교적, 외향적, 대인관계 활발, 모임 주도, 에너지 넘침, 표현력 풍부',
           '내향적, 사교 활동 기피, 대인관계 소극적, 혼자 있기 선호, 조용한 성격, 표현 절제'),
    'Sp': ('대인관계에서의 자신감과 자발성을 측정하는 척도. 사회적 자신감, 존재감, 영향력을 평가함',
           '사회적 자신감, 강한 존재감, 주목받기 좋아함, 발표력 우수, 카리스마, 사교적 리더십',
           '사회적 불안, 존재감 부족, 주목받기 싫어함, 발표 기피, 소극적 참여, 뒤에서 지원'),
    'Sa': ('자신의 가치와 장점을 인정하는 정도를 측정하는 척도. 자존감, 자기 효능감, 자기 수용을 평가함',
           '높은 자존감, 자기 확신, 장점 인식, 자기 효능감, 긍정적 자아상, 자기 수용',
           '낮은 자존감, 자기 의심, 단점 집착, 자기 효능감 부족, 부정적 자아상, 자기 비판'),
    'In': ('자율적이고 독립적인 사고와 행동 경향을 측정하는 척도. 독립성, 자율성, 개별성을 평가함',
           '독립적 사고, 자율적 행동, 개별성 추구, 독창적 접근, 자기 주도적, 타인 의견에 휘둘리지 않음',
           '의존적 성향, 타인 의견 추종, 집단 동조, 독립성 부족, 지시 의존적, 자율성 제한'),
    'Em': ('타인의 감정을 이해하고 공유하는 능력을 측정하는 척도. 공감 능력, 감정 이해, 배려심을 평가함',
           '높은 공감 능력, 타인 감정 이해, 배려심 많음, 감정적 지지 제공, 인간관계 우수',
           '공감 능력 부족, 타인 감정 무관심, 배려 부족, 감정적 둔감함, 인간관계 어려움'),
    'Re': ('책임감과 신뢰성을 측정하는 척도. 의무감, 신뢰성, 성실성, 약속 이행을 평가함',
           '강한 책임감, 높은 신뢰성, 약속 이행, 성실함, 의무감, 일관된 행동',
           '책임감 부족, 신뢰성 낮음, 약속 불이행, 불성실함, 의무감 부족, 일관성 부족'),
    'So': ('사회적 규범과 가치를 내면화한 정도를 측정하는 척도. 사회적 적응, 규범 준수, 도덕성을 평가함',
           '사회 규범 준수, 도덕적 행동, 사회적 적응 우수, 윤리 의식, 규칙 준수',
           '규범 무시, 반사회적 행동, 사회 부적응, 윤리 의식 부족, 규칙 위반'),
    'Sc': ('충동을 억제하고 자신을 통제하는 능력을 측정하는 척도. 자제력, 인내심, 감정 조절을 평가함',
           '높은 자제력, 감정 조절 우수, 인내심, 신중한 행동, 충동 억제, 계획적 행동',
           '충동적 행동, 감정 조절 어려움, 인내심 부족, 성급한 판단, 자제력 부족'),
    'Gi': ('타인에게 좋은 인상을 주려는 경향을 측정하는 척도. 인상 관리, 사회적 바람직성, 외적 이미지를 평가함',
           '좋은 인상 추구, 사회적 바람직성 높음, 외적 이미지 관리, 예의 바름, 호감형 행동',
           '인상 관리 무관심, 사회적 바람직성 낮음, 외적 이미지 소홀, 무뚝뚝함, 타인 시선 무관심'),
    'Cm': ('일반적인 사람들과 유사하게 반응하는 정도를 측정하는 척도. 일반성, 평범성, 사회적 동조를 평가함',
           '일반적 반응, 사회적 동조, 평범한 취향, 다수 의견 따름, 사회적 적응',
           '독특한 반응, 비일반적 취향, 다수 의견 거부, 개별적 선택, 사회적 부적응'),
    'Wb': ('전반적인 삶의 만족감과 행복감을 측정하는 척도. 심리적 안녕, 생활 만족, 긍정성을 평가함',
           '높은 생활 만족도, 긍정적 마인드, 심리적 안정, 행복감, 낙관적 태도, 스트레스 관리 우수',
           '생활 불만족, 부정적 마인드, 심리적 불안정, 우울감, 비관적 태도, 스트레스 취약'),
    'To': ('타인의 신념이나 태도에 대한 관용적 태도를 측정하는 척도. 포용성, 다양성 수용, 열린 마음을 평가함',
           '높은 포용성, 다양성 수용, 열린 마음, 편견 없음, 차이 인정, 관용적 태도',
           '편견과 고정관념, 다양성 거부, 닫힌 마음, 배타적 태도, 차이 불인정'),
    'Ac': ('규칙적이고 체계적인 환경에서 성취를 이루는 경향을 측정하는 척도. 조직 적응, 규칙 준수, 체계적 업무를 평가함',
           '체계적 업무 수행, 규칙 준수, 조직 적응 우수, 절차 중시, 안정적 성과',
           '비체계적 업무, 규칙 무시, 조직 부적응, 절차 경시, 불안정한 성과'),
    'Ai': ('독창적이고 자율적인 환경에서 성취를 이루는 경향을 측정하는 척도. 창의적 성취, 독립적 업무, 혁신 추구를 평가함',
           '창의적 성취, 독립적 업무 선호, 혁신 추구, 자율적 환경 선호, 독창적 접근',
           '창의성 부족, 의존적 업무, 혁신 기피, 통제된 환경 선호, 관습적 접근'),
    'Ie': ('지적 능력을 효율적으로 사용하는 정도를 측정하는 척도. 지적 효율성, 학습 능력, 정보 처리를 평가함',
           '높은 지적 효율성, 빠른 학습, 정보 처리 우수, 논리적 사고, 문제 해결 능력',
           '지적 효율성 낮음, 학습 속도 느림, 정보 처리 어려움, 논리적 사고 부족'),
    'Py': ('자신과 타인의 내면 및 동기에 대한 관심 정도를 측정하는 척도. 심리적 통찰, 내적 동기 이해, 자기 성찰을 평가함',
           '심리적 통찰력, 내적 동기 이해, 자기 성찰, 타인 심리 파악, 깊이 있는 사고',
           '심리적 둔감함, 표면적 사고, 자기 성찰 부족, 타인 심리 무관심, 단순한 사고'),
    'Fx': ('변화에 개방적이고 적응을 잘하는 정도를 측정하는 척도. 유연성, 적응력, 변화 수용을 평가함',
           '높은 유연성, 변화 적응 우수, 새로운 상황 대처, 다양한 관점 수용, 개방적 태도',
           '경직된 사고, 변화 저항, 적응 어려움, 고정된 관점, 폐쇄적 태도'),
    'FM': ('전통적인 성 역할에 부합하는 관심과 태도를 측정하는 척도. 성 역할 인식, 관심사, 행동 패턴을 평가함',
           '전통적 성 역할 수용, 성별 고정관념 강함, 전형적 관심사, 성 역할 기대 부합',
           '성 역할 고정관념 약함, 다양한 관심사, 성별 구분 없는 행동, 개방적 성 역할 인식'),
    'v1': ('외부 세계와 상호작용하는 방식을 측정하는 벡터척도. 외향성-내향성 차원을 평가함',
           '높은 점수(외향적): 사교적, 활동적, 자극 추구, 타인과의 상호작용 선호, 에너지 넘침',
           '낮은 점수(내향적): 조용함, 신중함, 혼자 시간 선호, 깊이 있는 관계, 내적 에너지'),
    'v2': ('규범을 따르는 정도를 측정하는 벡터척도. 규범지향-규범회의 차원을 평가함',
           '높은 점수(규범지향): 규칙 준수, 전통 존중, 안정 추구, 질서 중시, 보수적 성향',
           '낮은 점수(규범회의): 규칙 의문시, 변화 추구, 혁신적 사고, 기존 질서 도전, 진보적 성향'),
    'v3': ('개인의 통합감과 자아실현 수준을 측정하는 벡터척도. 자아 통합, 성숙도, 자아실현을 평가함',
           '높은 자아 통합, 성숙한 인격, 자아실현 추구, 내적 조화, 삶의 목적 명확, 균형잡힌 성격',
           '자아 분열, 미성숙함, 자아실현 어려움, 내적 갈등, 삶의 목적 불분명, 불균형한 성격')
}

for scale_code, scale_info in CPI_METADATA["scales"].items():
    detailed_def, high_char, low_char = cpi_detailed_definitions.get(scale_code, 
        (scale_info['definition'], '평균 이상 특성', '평균 이하 특성'))
    metrics_data.append([
        f'CPI_{scale_code}', scale_info['name'], 'CPI', scale_info['group'],
        detailed_def, 'T점수 (20-80)', high_char, low_char
    ])

# CPI 라이프스타일 유형들
lifestyle_characteristics = {
    'Alpha': ('외향적이고 규범을 따르며, 능동적이고 리더십이 강한 실행형. 사교적이면서 책임감이 강하고 목표 지향적임',
              '리더십 발휘, 사교적 활동, 목표 달성 지향, 책임감 강함, 조직 적응 우수, 실행력 뛰어남',
              '과도한 통제욕, 융통성 부족, 타인 의견 경시, 스트레스 과다, 완벽주의 경향'),
    'Beta': ('내향적이고 규범을 따르며, 성실하고 책임감이 강한 협력형. 신중하고 안정적이며 팀워크를 중시함',
             '높은 성실성, 팀워크 우수, 신뢰성 높음, 안정적 성과, 규칙 준수, 협력적 태도',
             '소극적 태도, 리더십 부족, 변화 저항, 창의성 부족, 도전 회피'),
    'Gamma': ('외향적이고 규범에 회의적이며, 혁신적이고 즐거움을 추구하는 혁신형. 창의적이고 자유로우며 변화를 추구함',
              '높은 창의성, 혁신 추구, 변화 주도, 자유로운 사고, 새로운 시도, 유연한 접근',
              '규칙 무시, 일관성 부족, 충동적 행동, 책임감 부족, 조직 부적응'),
    'Delta': ('내향적이고 규범에 회의적이며, 사색적이고 독특한 경향이 있는 사색형. 독립적이고 개별적이며 깊이 있는 사고를 함',
              '독창적 사고, 깊이 있는 분석, 독립적 판단, 개별성 추구, 내적 동기, 철학적 사고',
              '사회적 고립, 소통 어려움, 협업 기피, 실용성 부족, 현실 감각 부족')
}

for type_code, type_info in CPI_METADATA["lifestyle_types"].items():
    detailed_def, high_char, low_char = lifestyle_characteristics[type_code]
    metrics_data.append([
        f'CPI_LIFESTYLE_{type_code}', type_info['name'], 'CPI', '라이프스타일유형',
        detailed_def, '유형분류', high_char, low_char
    ])

# MMPI 지표들 (임상적 특성 포함)
mmpi_detailed_definitions = {
    'L': ('자신을 의도적으로 좋게 보이려는 경향을 측정하는 타당도 척도. 사회적 바람직성, 방어적 태도를 평가함',
          '높은 점수: 과도한 인상 관리, 방어적 태도, 사회적 바람직성 추구, 솔직하지 못함',
          '낮은 점수: 솔직한 응답, 자연스러운 태도, 인상 관리 적음, 진정성'),
    'F': ('비전형적이고 특이한 방식으로 응답하는 경향을 측정하는 타당도 척도. 응답 일관성, 집중도를 평가함',
          '높은 점수: 비전형적 응답, 주의 집중 부족, 혼란스러운 상태, 과장된 증상 호소',
          '낮은 점수: 일관된 응답, 집중도 양호, 안정된 상태, 현실적 자기 인식'),
    'K': ('자신을 방어적으로 드러내지 않으려는 태도를 측정하는 타당도 척도. 방어성, 은폐 경향을 평가함',
          '높은 점수: 강한 방어성, 문제 은폐, 완벽한 이미지 추구, 취약점 숨김',
          '낮은 점수: 개방적 태도, 솔직한 자기 개방, 취약점 인정, 도움 요청 가능'),
    'Hs': ('신체적 건강에 대한 과도한 염려와 집착을 측정하는 임상척도. 건강 염려, 신체 증상, 의료 추구를 평가함',
           '높은 점수: 건강 과도 염려, 신체 증상 호소, 의료진 자주 방문, 업무 집중 어려움',
           '낮은 점수: 건강 자신감, 신체 증상 적음, 의료 의존도 낮음, 업무 집중 양호'),
    'D': ('우울감, 비관주의, 무기력감 등 우울 증상을 측정하는 임상척도. 기분 상태, 동기, 에너지 수준을 평가함',
          '높은 점수: 우울감, 비관적 사고, 무기력감, 동기 저하, 에너지 부족, 절망감, 업무 의욕 저하',
          '낮은 점수: 긍정적 기분, 낙관적 사고, 활력, 높은 동기, 에너지 충만, 희망적 태도'),
    'Hy': ('스트레스 상황에서 신체 증상이나 방어기제를 사용하는 경향을 측정하는 임상척도',
           '높은 점수: 스트레스 시 신체 증상, 방어기제 사용, 감정 억압, 갈등 회피',
           '낮은 점수: 스트레스 직면, 현실적 대처, 감정 표현 적절, 갈등 해결 시도'),
    'Pd': ('사회적 규범이나 권위에 대한 반항과 충동성을 측정하는 임상척도. 반사회적 행동, 충동성, 권위 도전을 평가함',
           '높은 점수: 규칙 위반, 권위 도전, 충동적 행동, 반사회적 태도, 책임감 부족',
           '낮은 점수: 규칙 준수, 권위 존중, 신중한 행동, 사회적 적응, 책임감'),
    'Mf': ('전통적인 성 역할 고정관념과의 일치 정도를 측정하는 임상척도',
           '높은 점수: 전통적 성 역할 거부, 다양한 관심사, 성별 고정관념 약함',
           '낮은 점수: 전통적 성 역할 수용, 성별 고정관념 강함, 전형적 관심사'),
    'Pa': ('타인에 대한 의심과 적대감을 측정하는 임상척도. 편집성, 의심, 적대감을 평가함',
           '높은 점수: 타인 불신, 의심 많음, 적대적 태도, 피해 의식, 경계심 강함',
           '낮은 점수: 타인 신뢰, 의심 적음, 우호적 태도, 개방적 관계, 협력적'),
    'Pt': ('불안, 걱정, 강박적 사고를 측정하는 임상척도. 불안 수준, 걱정, 강박성을 평가함',
           '높은 점수: 높은 불안, 과도한 걱정, 강박적 사고, 완벽주의, 결정 어려움',
           '낮은 점수: 낮은 불안, 적절한 걱정, 유연한 사고, 현실적 기준, 결정력'),
    'Sc': ('혼란스러운 사고와 사회적 소외감을 측정하는 임상척도. 사고 혼란, 현실감, 사회적 연결을 평가함',
           '높은 점수: 사고 혼란, 현실감 부족, 사회적 소외, 이상한 경험, 집중력 부족',
           '낮은 점수: 명확한 사고, 현실감 양호, 사회적 연결, 일반적 경험, 집중력 양호'),
    'Ma': ('과잉 활동과 충동성을 측정하는 임상척도. 활동성, 충동성, 기분 변화를 평가함',
           '높은 점수: 과잉 활동, 충동적 행동, 기분 변화 심함, 성급함, 집중력 부족',
           '낮은 점수: 적절한 활동, 신중한 행동, 안정된 기분, 인내심, 집중력 양호'),
    'Si': ('사교 상황에서의 불편감과 내향성을 측정하는 임상척도. 사회적 내향성, 사교 불안을 평가함',
           '높은 점수: 사교 불안, 대인관계 어려움, 사회적 위축, 혼자 있기 선호, 소극적 참여',
           '낮은 점수: 사교적, 대인관계 원활, 사회적 자신감, 모임 참여 적극적, 외향적')
}

for scale_code, scale_info in MMPI_METADATA["scales"].items():
    detailed_def, high_char, low_char = mmpi_detailed_definitions.get(scale_code,
        (scale_info['definition'], '높은 점수 특성', '낮은 점수 특성'))
    metrics_data.append([
        f'MMPI_{scale_code}', scale_info['name'], 'MMPI', scale_info['group'],
        detailed_def, 'T점수 (20-80)', high_char, low_char
    ])

# 적성검사 지표들 (직무 연관성 포함)
aptitude_detailed_definitions = {
    'verbal_total': ('언어와 관련된 종합적 능력. 어휘력, 문장 이해력, 표현력을 종합 평가하여 언어적 업무 수행 능력을 측정함',
                    '높은 언어 이해력, 풍부한 어휘력, 명확한 표현력, 문서 작성 우수, 언어적 업무 적합',
                    '언어 이해력 부족, 제한된 어휘력, 표현력 부족, 문서 작성 어려움, 언어적 업무 부적합'),
    'verbal_vocab': ('어휘의 의미를 정확히 이해하고 적절히 활용하는 능력. 단어 이해력과 활용도를 측정함',
                    '풍부한 어휘력, 정확한 단어 선택, 맥락적 이해, 전문 용어 활용, 표현의 다양성',
                    '제한된 어휘력, 부정확한 단어 사용, 맥락 이해 부족, 전문 용어 어려움, 단조로운 표현'),
    'numerical_total': ('수량적 정보를 이해하고 논리적으로 사고하는 종합 능력. 수리적 업무 수행 능력을 측정함',
                       '높은 수리 능력, 논리적 사고, 통계적 이해, 데이터 분석 가능, 수리적 업무 적합',
                       '수리 능력 부족, 논리적 사고 어려움, 통계 이해 부족, 데이터 분석 어려움, 수리적 업무 부적합'),
    'situational_judgment': ('조직 상황에서의 적절한 판단력을 측정. 상황 인식, 대안 평가, 최적 선택 능력을 평가함',
                            '상황 판단 우수, 적절한 대응, 갈등 해결 능력, 조직 적응력, 현실적 판단',
                            '상황 판단 미흡, 부적절한 대응, 갈등 해결 어려움, 조직 부적응, 비현실적 판단'),
    'social_knowledge': ('사회 구성원으로서 필요한 기본 상식과 사회적 이해를 측정함',
                        '풍부한 사회 상식, 시사 이해, 사회 규범 인식, 상식적 판단, 사회적 적응',
                        '사회 상식 부족, 시사 무관심, 사회 규범 무지, 비상식적 판단, 사회적 부적응'),
    'interpersonal_skills': ('타인과의 관계 형성과 유지 능력을 측정. 대인관계 기술과 사회적 기술을 평가함',
                            '원활한 대인관계, 사회적 기술 우수, 갈등 조정 능력, 네트워킹 능력, 팀워크',
                            '대인관계 어려움, 사회적 기술 부족, 갈등 해결 미흡, 네트워킹 부족, 개인주의')
}

for factor_code, factor_info in APTITUDE_METADATA["factors"].items():
    if factor_code in aptitude_detailed_definitions:
        detailed_def, high_char, low_char = aptitude_detailed_definitions[factor_code]
    else:
        detailed_def = factor_info['definition']
        high_char = '우수한 능력'
        low_char = '개선 필요'
    
    measurement_scale = '100점 척도' if factor_info['group'] != '상위요인' else '평균점수'
    metrics_data.append([
        f'APT_{factor_code.upper()}', factor_info['name'], '적성검사', factor_info['group'],
        detailed_def, measurement_scale, high_char, low_char
    ])

df_metrics = pd.DataFrame(metrics_data, columns=[
    'metric_code', 'metric_name', 'tool_name', 'dimension', 
    'definition', 'measurement_scale', 'high_score_characteristics', 'low_score_characteristics'
])
df_metrics.to_csv('data/02_hr_metrics_definition.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_metrics)}개 평가 지표 정의 완료")

# ============================================================================
# 2. employee_info.csv - 직원 기본 정보 (200명, 위계 구조 반영)
print("\n[2/25] employee_info.csv 생성 중...")

# 조직 구조 정의 (org_id, org_name, parent_org, size)
departments = [
    # org_id, org_name, parent_org, division_name, team_size
    ('ORG101', 'HR팀', 'ORG100', '경영지원본부', 12),
    ('ORG102', '재무팀', 'ORG100', '경영지원본부', 10),
    ('ORG201', 'AI솔루션개발팀', 'ORG200', '기술본부', 28),
    ('ORG202', '플랫폼개발팀', 'ORG200', '기술본부', 32),
    ('ORG203', '데이터분석팀', 'ORG200', '기술본부', 24),
    ('ORG204', 'IT기획팀', 'ORG200', '기술본부', 20),
    ('ORG205', 'UI/UX디자인팀', 'ORG200', '기술본부', 16),
    ('ORG206', 'QA팀', 'ORG200', '기술본부', 18),
    ('ORG301', '마케팅팀', 'ORG300', '비즈니스본부', 20),
    ('ORG302', '영업팀', 'ORG300', '비즈니스본부', 26),
]

job_titles_hierarchy = {
    '사원': 1,
    '주임': 2,
    '대리': 3,
    '과장': 4,
    '차장': 5,
    '팀장': 6,
    '부장': 7,
    '본부장': 8,
    '이사': 9,
}

employees = []

# 1. 대표이사
employees.append({
    'employee_id': 'EMP000',
    'name': fake.name(),
    'gender': random.choice(['남', '여']),
    'birth_date': fake.date_of_birth(minimum_age=50, maximum_age=60).strftime('%Y-%m-%d'),
    'employment_type': '정규직',
    'hire_date': '2010-01-01',
    'org_id': 'ORG000',
    'org_name': '넥스트젠 테크놀로지스',
    'division_name': '대표이사',
    'job_title': '대표이사',
    'manager_id': None,
    'status': '재직'
})

# 2. 본부장 3명 (경영지원본부, 기술본부, 비즈니스본부)
division_heads = [
    ('DIV001', 'ORG100', '경영지원본부', '경영지원본부'),
    ('DIV002', 'ORG200', '기술본부', '기술본부'),
    ('DIV003', 'ORG300', '비즈니스본부', '비즈니스본부'),
]

for emp_id, org_id, org_name, div_name in division_heads:
    employees.append({
        'employee_id': emp_id,
        'name': fake.name(),
        'gender': random.choice(['남', '여']),
        'birth_date': fake.date_of_birth(minimum_age=45, maximum_age=55).strftime('%Y-%m-%d'),
        'employment_type': '정규직',
        'hire_date': fake.date_between(start_date='-14y', end_date='-8y').strftime('%Y-%m-%d'),
        'org_id': org_id,
        'org_name': org_name,
        'division_name': div_name,
        'job_title': '본부장',
        'manager_id': 'EMP000',
        'status': '재직'
    })

# 3. 팀장 10명
team_leader_counter = 1
for org_id, org_name, parent_org, div_name, _ in departments:
    # 해당 팀의 본부장 찾기
    if parent_org == 'ORG100':
        manager_id = 'DIV001'
    elif parent_org == 'ORG200':
        manager_id = 'DIV002'
    else:  # ORG300
        manager_id = 'DIV003'
    
    employees.append({
        'employee_id': f'TL{team_leader_counter:03d}',
        'name': fake.name(),
        'gender': random.choice(['남', '여']),
        'birth_date': fake.date_of_birth(minimum_age=38, maximum_age=50).strftime('%Y-%m-%d'),
        'employment_type': '정규직',
        'hire_date': fake.date_between(start_date='-12y', end_date='-5y').strftime('%Y-%m-%d'),
        'org_id': org_id,
        'org_name': org_name,
        'division_name': div_name,
        'job_title': '팀장',
        'manager_id': manager_id,
        'status': '재직'
    })
    team_leader_counter += 1

# 4. 일반 직원 생성 (팀별)
emp_counter = 1
for org_id, org_name, parent_org, div_name, team_size in departments:
    # 팀장 찾기
    team_leader = [e for e in employees if e['org_id'] == org_id and e['job_title'] == '팀장']
    manager_id = team_leader[0]['employee_id'] if team_leader else 'EMP000'
    
    # 팀원 생성 (팀장 1명 제외)
    for _ in range(team_size - 1):
        # 입사 연도 (2015-2024)
        hire_year = random.randint(2015, 2024)
        hire_month = random.randint(1, 12)
        hire_day = random.randint(1, 28)
        hire_date = datetime(hire_year, hire_month, hire_day)
        
        # 근속연수 계산
        years_of_service = 2024 - hire_year
        
        # 근속연수에 따른 직급 결정 (자연스러운 분포)
        if years_of_service < 2:
            job_title = '사원'
        elif years_of_service < 4:
            job_title = random.choice(['사원', '주임', '대리'])
        elif years_of_service < 6:
            job_title = random.choice(['주임', '대리', '과장'])
        elif years_of_service < 8:
            job_title = random.choice(['대리', '과장', '차장'])
        else:
            job_title = random.choice(['과장', '차장', '차장', '부장'])
        
        # 나이 계산 (직급과 연관성 있게)
        if job_title in ['사원', '주임']:
            age_range = (25, 32)
        elif job_title in ['대리', '과장']:
            age_range = (28, 38)
        elif job_title == '차장':
            age_range = (33, 45)
        else:
            age_range = (38, 55)
        
        # 재직/퇴사 상태 (약 90% 재직)
        status = random.choices(['재직', '퇴사'], weights=[90, 10])[0]
        
        employees.append({
            'employee_id': f'EMP{emp_counter:03d}',
            'name': fake.name(),
            'gender': random.choice(['남', '여']),
            'birth_date': fake.date_of_birth(minimum_age=age_range[0], maximum_age=age_range[1]).strftime('%Y-%m-%d'),
            'employment_type': random.choices(['정규직', '계약직'], weights=[95, 5])[0],
            'hire_date': hire_date.strftime('%Y-%m-%d'),
            'org_id': org_id,
            'org_name': org_name,
            'division_name': div_name,
            'job_title': job_title,
            'manager_id': manager_id,
            'status': status
        })
        emp_counter += 1

df_employees = pd.DataFrame(employees)
df_employees.to_csv('data/03_employee_info.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_employees)}명 직원 정보 생성 완료 (3단계 위계 구조)")

# ============================================================================
# 2-1. reporting_lines.csv - 전체 보고 라인 매핑
print("\n[2-1/25] reporting_lines.csv 생성 중...")

reporting_lines = []
line_counter = 1

for emp in employees:
    if emp['employee_id'] == 'EMP000':
        continue  # 대표이사는 보고 라인 없음
    
    # 직속 상사
    immediate_manager = emp['manager_id']
    
    # 2차 상사 (상사의 상사)
    manager_emp = next((e for e in employees if e['employee_id'] == immediate_manager), None)
    second_level_manager = manager_emp['manager_id'] if manager_emp and manager_emp['manager_id'] else None
    
    # 3차 상사 (본부장/대표)
    if second_level_manager:
        second_manager_emp = next((e for e in employees if e['employee_id'] == second_level_manager), None)
        third_level_manager = second_manager_emp['manager_id'] if second_manager_emp and second_manager_emp['manager_id'] else None
    else:
        third_level_manager = None
    
    reporting_lines.append({
        'reporting_line_id': f'RL{line_counter:04d}',
        'employee_id': emp['employee_id'],
        'employee_name': emp['name'],
        'job_title': emp['job_title'],
        'immediate_manager_id': immediate_manager,
        'immediate_manager_title': manager_emp['job_title'] if manager_emp else None,
        'second_level_manager_id': second_level_manager,
        'third_level_manager_id': third_level_manager,
        'reporting_depth': 1 if not second_level_manager else (2 if not third_level_manager else 3),
        'division_name': emp['division_name'],
        'org_name': emp['org_name']
    })
    line_counter += 1

df_reporting_lines = pd.DataFrame(reporting_lines)
df_reporting_lines.to_csv('data/01_reporting_lines.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_reporting_lines)}개 보고 라인 생성 완료")

# ============================================================================
# 3. job_history.csv - 직원 경력 경로
print("\n[3/25] job_history.csv 생성 중...")

job_history = []
history_counter = 1

for emp in employees:
    emp_id = emp['employee_id']
    hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
    current_title = emp['job_title']
    
    # 입사 시점 직급 결정 (모든 직원이 낮은 직급에서 시작)
    if current_title == '대표이사':
        initial_title = current_title  # 대표이사만 예외
    else:
        # 현재 직급보다 낮은 직급으로 시작 (팀장도 포함)
        current_level = job_titles_hierarchy.get(current_title, 1)
        if current_level <= 2:
            initial_title = '사원'
        elif current_level <= 4:  # 대리, 과장
            initial_title = random.choice(['사원', '주임'])
        elif current_level <= 6:  # 차장, 팀장
            initial_title = random.choice(['사원', '주임', '대리'])
        else:  # 부장, 본부장
            initial_title = random.choice(['주임', '대리', '과장'])
    
    # 입사 기록
    job_history.append({
            'history_id': f'HIST{history_counter:04d}',
            'employee_id': emp_id,
            'start_date': emp['hire_date'],
            'end_date': None if initial_title == current_title else None,
            'org_id': emp['org_id'],
            'job_title': initial_title,
            'change_type': '신규입사'
    })
    history_counter += 1
    
    # 승진 기록 생성 (입사일로부터 현재 직급까지)
    if initial_title != current_title:
        years_of_service = 2024 - hire_date.year
        current_level = job_titles_hierarchy.get(current_title, 1)
        initial_level = job_titles_hierarchy.get(initial_title, 1)
        
        # 승진 경로 생성
        promotion_path = []
        for level in range(initial_level + 1, current_level + 1):
            title = [k for k, v in job_titles_hierarchy.items() if v == level][0]
            promotion_path.append(title)
        
        # 승진 날짜 분산
        if promotion_path:
            years_per_promotion = years_of_service / len(promotion_path)
            for idx, promoted_title in enumerate(promotion_path):
                promotion_date = hire_date + timedelta(days=int((idx + 1) * years_per_promotion * 365))
                if promotion_date > datetime.now():
                    break
                
                # 이전 기록 종료
                if job_history:
                    job_history[-1]['end_date'] = (promotion_date - timedelta(days=1)).strftime('%Y-%m-%d')
                
                job_history.append({
                    'history_id': f'HIST{history_counter:04d}',
                    'employee_id': emp_id,
                    'start_date': promotion_date.strftime('%Y-%m-%d'),
                    'end_date': None if promoted_title == current_title else None,
                    'org_id': emp['org_id'],
                    'job_title': promoted_title,
                    'change_type': '승진'
                })
                history_counter += 1

df_job_history = pd.DataFrame(job_history)
df_job_history.to_csv('data/04_job_history.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_job_history)}건 경력 이력 생성 완료 (위계 반영)")

# ============================================================================
# 4. personal_traits.csv - Big-5 성격 검사
print("\n[4/25] personal_traits.csv 생성 중...")

traits_data = []
trait_counter = 1

# 모든 재직 중인 직원에게 Big-5 검사 실시
for emp in employees:
    if emp['status'] == '재직':
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
        assessment_date = hire_date + timedelta(days=random.randint(30, 120))
        
        # Big-5 점수 생성 (정규분포 활용, 0-100 척도)
        openness = int(np.clip(np.random.normal(65, 15), 30, 100))
        conscientiousness = int(np.clip(np.random.normal(70, 12), 40, 100))
        extraversion = int(np.clip(np.random.normal(60, 18), 20, 100))
        agreeableness = int(np.clip(np.random.normal(68, 14), 35, 100))
        neuroticism = int(np.clip(np.random.normal(45, 16), 10, 90))
        
        # 가장 높은 특성 찾기
        scores = {
            '개방성': openness,
            '성실성': conscientiousness,
            '외향성': extraversion,
            '친화성': agreeableness
        }
        highest_trait = max(scores, key=scores.get)
        highest_score = scores[highest_trait]
        
        # 강점 설명
        if highest_score >= 80:
            strength_desc = f'매우 높은 {highest_trait}'
        elif highest_score >= 70:
            strength_desc = f'높은 {highest_trait}'
        else:
            strength_desc = f'{highest_trait} 우세'
        
        traits_data.append({
            'trait_id': f'TRAIT{trait_counter:03d}',
            'employee_id': emp['employee_id'],
            'assessment_date': assessment_date.strftime('%Y-%m-%d'),
            'tool_name': 'Big-5 성격검사',
            'openness': openness,
            'conscientiousness': conscientiousness,
            'extraversion': extraversion,
            'agreeableness': agreeableness,
            'neuroticism': neuroticism,
            'primary_strength': strength_desc,
            'motivation_driver': random.choice(['성취', '안정', '관계', '성장', '인정', '자율성', '전문성', '영향력'])
        })
        trait_counter += 1

df_traits = pd.DataFrame(traits_data)
df_traits.to_csv('data/05_personal_traits.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_traits)}건 성격 특성 데이터 생성 완료")

print("\n" + "=" * 80)
print("A그룹 마스터 데이터 생성 완료")
print("=" * 80)

# ============================================================================
# B그룹: 채용, 온보딩, 교육 데이터
# ============================================================================

# 5. recruitment_history.csv - 채용 이력
print("\n[5/25] recruitment_history.csv 생성 중...")

recruitment_data = []
recruit_counter = 1

recruitment_channels = ['채용공고', '헤드헌팅', '추천', '채용박람회', '대학 채용', '인턴 전환', '경력 스카우트']

for emp in employees:
    if emp['status'] == '재직' or random.random() < 0.7:  # 재직자 + 일부 퇴사자
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
        
        apply_date = hire_date - timedelta(days=random.randint(60, 150))
        interview_date = apply_date + timedelta(days=random.randint(14, 35))
        offer_date = interview_date + timedelta(days=random.randint(7, 21))
        
        # 직급에 따른 채용 경로
        if emp['job_title'] in ['팀장', '부장', '이사', '대표이사']:
            channel = random.choice(['헤드헌팅', '경력 스카우트', '추천'])
        else:
            channel = random.choice(recruitment_channels)
        
        recruitment_data.append({
            'recruitment_id': f'REC{recruit_counter:04d}',
            'employee_id': emp['employee_id'],
            'position_title': emp['job_title'],
            'apply_date': apply_date.strftime('%Y-%m-%d'),
            'interview_date': interview_date.strftime('%Y-%m-%d'),
            'offer_date': offer_date.strftime('%Y-%m-%d'),
            'hire_date': emp['hire_date'],
            'recruitment_channel': channel,
            'interviewer_comment': random.choice([
                '직무 전문성이 뛰어나며 조직 적합도가 높음',
                '우수한 역량과 성장 가능성을 보임',
                '경험과 역량이 요구사항에 부합함',
                '기대 이상의 실력과 태도를 보임',
                '팀워크와 커뮤니케이션 능력이 우수함',
                '빠른 학습 능력과 적응력을 갖춤'
            ])
        })
        recruit_counter += 1

df_recruitment = pd.DataFrame(recruitment_data)
df_recruitment.to_csv('data/06_recruitment_history.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_recruitment)}건 채용 이력 생성 완료")

# ============================================================================
# 5-2. recruitment_aptitude_results.csv - 적성검사 결과
print("\n[6/25] recruitment_aptitude_results.csv 생성 중...")

aptitude_results = []
aptitude_counter = 1

def generate_t_score(mean=50, std=10, min_val=20, max_val=80):
    """T점수 생성 (평균 50, 표준편차 10)"""
    return int(np.clip(np.random.normal(mean, std), min_val, max_val))

def generate_aptitude_score(mean=75, std=12, min_val=30, max_val=100):
    """적성검사 점수 생성 (100점 만점)"""
    return int(np.clip(np.random.normal(mean, std), min_val, max_val))

for emp in employees:
    # 모든 직원 (재직자 + 퇴사자)에 대해 채용 시 적성검사 실시
    hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
    
    # 채용 프로세스: 지원일로부터 7-14일 후 적성검사 실시
    recruitment_record = next((r for r in recruitment_data if r['employee_id'] == emp['employee_id']), None)
    if recruitment_record:
        apply_date = datetime.strptime(recruitment_record['apply_date'], '%Y-%m-%d')
        test_date = apply_date + timedelta(days=random.randint(7, 14))
    else:
        # 채용 기록이 없는 경우 입사일 기준으로 역산
        test_date = hire_date - timedelta(days=random.randint(30, 60))
    
    # 직무별 적성 점수 조정
    job_adjustment = {
        '기술본부': {'numerical_total': 5, 'verbal_total': 0, 'situational_judgment': 3},
        '경영지원본부': {'numerical_total': 2, 'verbal_total': 5, 'situational_judgment': 5},
        '비즈니스본부': {'numerical_total': 0, 'verbal_total': 3, 'situational_judgment': 5}
    }
    
    division_adj = job_adjustment.get(emp['division_name'], {'numerical_total': 0, 'verbal_total': 0, 'situational_judgment': 0})
    
    # 퇴사자는 일부 점수를 낮게 조정 (채용 미스매치 반영)
    if emp['status'] == '퇴사':
        overall_adjustment = -8
    else:
        overall_adjustment = 0
    
    # 언어적 능력 하위 요인
    verbal_vocab = generate_aptitude_score(75 + division_adj['verbal_total'] + overall_adjustment)
    verbal_composition = generate_aptitude_score(75 + division_adj['verbal_total'] + overall_adjustment)
    verbal_decoding = generate_aptitude_score(75 + division_adj['verbal_total'] + overall_adjustment)
    verbal_english = generate_aptitude_score(70 + division_adj['verbal_total'] + overall_adjustment)
    verbal_total = round((verbal_vocab + verbal_composition + verbal_decoding + verbal_english) / 4, 1)
    
    # 수리적 능력 하위 요인
    numerical_quantity = generate_aptitude_score(75 + division_adj['numerical_total'] + overall_adjustment)
    numerical_statistics = generate_aptitude_score(75 + division_adj['numerical_total'] + overall_adjustment)
    numerical_logic = generate_aptitude_score(75 + division_adj['numerical_total'] + overall_adjustment)
    numerical_total = round((numerical_quantity + numerical_statistics + numerical_logic) / 3, 1)
    
    # 기타 능력
    situational_judgment = generate_aptitude_score(75 + division_adj['situational_judgment'] + overall_adjustment)
    social_knowledge = generate_aptitude_score(75 + overall_adjustment)
    interpersonal_skills = generate_aptitude_score(75 + overall_adjustment)
    
    # 전체 점수
    overall_aptitude_score = round((verbal_total + numerical_total + situational_judgment + social_knowledge + interpersonal_skills) / 5, 1)
    
    # 등급 산정
    if overall_aptitude_score >= 85:
        aptitude_grade = 'S'
    elif overall_aptitude_score >= 75:
        aptitude_grade = 'A'
    elif overall_aptitude_score >= 65:
        aptitude_grade = 'B'
    elif overall_aptitude_score >= 55:
        aptitude_grade = 'C'
    else:
        aptitude_grade = 'D'
    
    # 합격/불합격 (C등급 이상 합격)
    pass_fail_status = 'PASS' if aptitude_grade in ['S', 'A', 'B', 'C'] else 'FAIL'
    
    aptitude_results.append({
        'test_id': f'APT{aptitude_counter:04d}',
        'employee_id': emp['employee_id'],
        'test_date': test_date.strftime('%Y-%m-%d'),
        'recruitment_id': recruitment_record['recruitment_id'] if recruitment_record else f'REC{aptitude_counter:04d}',
        
        # 언어적 능력
        'verbal_total': verbal_total,
        'verbal_vocab': verbal_vocab,
        'verbal_composition': verbal_composition,
        'verbal_decoding': verbal_decoding,
        'verbal_english': verbal_english,
        
        # 수리적 능력
        'numerical_total': numerical_total,
        'numerical_quantity': numerical_quantity,
        'numerical_statistics': numerical_statistics,
        'numerical_logic': numerical_logic,
        
        # 기타 능력
        'situational_judgment': situational_judgment,
        'social_knowledge': social_knowledge,
        'interpersonal_skills': interpersonal_skills,
        
        # 종합
        'overall_aptitude_score': overall_aptitude_score,
        'aptitude_grade': aptitude_grade,
        'pass_fail_status': pass_fail_status
    })
    aptitude_counter += 1

df_aptitude_results = pd.DataFrame(aptitude_results)
df_aptitude_results.to_csv('data/07_recruitment_aptitude_results.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_aptitude_results)}건 적성검사 결과 생성 완료")

# ============================================================================
# 5-3. recruitment_cpi_results.csv - CPI 성격검사 결과
print("\n[7/25] recruitment_cpi_results.csv 생성 중...")

cpi_results = []
cpi_counter = 1

for emp in employees:
    # 적성검사 후 3-7일 후 CPI 실시
    aptitude_record = next((a for a in aptitude_results if a['employee_id'] == emp['employee_id']), None)
    if aptitude_record:
        aptitude_date = datetime.strptime(aptitude_record['test_date'], '%Y-%m-%d')
        test_date = aptitude_date + timedelta(days=random.randint(3, 7))
    else:
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
        test_date = hire_date - timedelta(days=random.randint(20, 40))
    
    # 퇴사자 특성 반영 (일부 척도에서 낮은 점수)
    if emp['status'] == '퇴사':
        adjustment = -5  # 전반적으로 낮은 점수
        wb_adjustment = -10  # 안녕감 특히 낮음
        re_adjustment = -8   # 책임감 낮음
    else:
        adjustment = 0
        wb_adjustment = 0
        re_adjustment = 0
    
    # 직급별 특성 반영
    if emp['job_title'] in ['팀장', '본부장', '대표이사']:
        leadership_bonus = 8
    elif emp['job_title'] in ['차장', '부장']:
        leadership_bonus = 5
    else:
        leadership_bonus = 0
    
    # CPI 20개 일상척도 생성 (T점수: 평균 50, 표준편차 10)
    # 1군: 대인관계 및 자신감
    Do = generate_t_score(50 + leadership_bonus + adjustment)  # 지배성
    Cs = generate_t_score(50 + leadership_bonus + adjustment)  # 지위추구성
    Sy = generate_t_score(50 + adjustment)  # 사교성
    Sp = generate_t_score(50 + leadership_bonus//2 + adjustment)  # 사회적존재감
    Sa = generate_t_score(50 + adjustment)  # 자기수용
    In = generate_t_score(50 + adjustment)  # 독립성
    Em = generate_t_score(50 + adjustment)  # 공감성
    
    # 2군: 규범 지향성 및 가치관
    Re = generate_t_score(50 + re_adjustment + adjustment)  # 책임감
    So = generate_t_score(50 + adjustment)  # 사회화
    Sc = generate_t_score(50 + adjustment)  # 자기통제
    Gi = generate_t_score(50 + adjustment)  # 호감성
    Cm = generate_t_score(50 + adjustment)  # 공동체성
    Wb = generate_t_score(50 + wb_adjustment + adjustment)  # 안녕감
    To = generate_t_score(50 + adjustment)  # 관용성
    
    # 3군: 성취 잠재력 및 지적 효율성
    Ac = generate_t_score(50 + adjustment)  # 순응을통한성취
    Ai = generate_t_score(50 + leadership_bonus//2 + adjustment)  # 독립을통한성취
    Ie = generate_t_score(50 + adjustment)  # 지적효율성
    
    # 4군: 역할 및 개인적 스타일
    Py = generate_t_score(50 + adjustment)  # 심리지향성
    Fx = generate_t_score(50 + adjustment)  # 융통성
    FM = generate_t_score(50 + adjustment)  # 여성성남성성
    
    # 벡터척도 (v1, v2, v3)
    v1 = generate_t_score(50 + adjustment)  # 외향성-내향성
    v2 = generate_t_score(50 + adjustment)  # 규범지향-규범회의
    v3 = generate_t_score(50 + adjustment)  # 자아실현
    
    # 라이프스타일 유형 결정 (v1, v2 기준)
    if v1 >= 50 and v2 >= 50:
        lifestyle_type = 'Alpha'  # 외향적 + 규범지향
    elif v1 < 50 and v2 >= 50:
        lifestyle_type = 'Beta'   # 내향적 + 규범지향
    elif v1 >= 50 and v2 < 50:
        lifestyle_type = 'Gamma'  # 외향적 + 규범회의
    else:
        lifestyle_type = 'Delta'  # 내향적 + 규범회의
    
    # 전체 CPI 점수 (주요 척도들의 평균)
    major_scales = [Do, Cs, Sy, Re, So, Sc, Ac, Ai, Ie]
    overall_cpi_score = round(np.mean(major_scales), 1)
    
    cpi_results.append({
        'test_id': f'CPI{cpi_counter:04d}',
        'employee_id': emp['employee_id'],
        'test_date': test_date.strftime('%Y-%m-%d'),
        'recruitment_id': aptitude_record['recruitment_id'] if aptitude_record else f'REC{cpi_counter:04d}',
        
        # 1군: 대인관계 및 자신감
        'dominance_do': Do,
        'capacity_status_cs': Cs,
        'sociability_sy': Sy,
        'social_presence_sp': Sp,
        'self_acceptance_sa': Sa,
        'independence_in': In,
        'empathy_em': Em,
        
        # 2군: 규범 지향성 및 가치관
        'responsibility_re': Re,
        'socialization_so': So,
        'self_control_sc': Sc,
        'good_impression_gi': Gi,
        'communality_cm': Cm,
        'well_being_wb': Wb,
        'tolerance_to': To,
        
        # 3군: 성취 잠재력 및 지적 효율성
        'achievement_conformance_ac': Ac,
        'achievement_independence_ai': Ai,
        'intellectual_efficiency_ie': Ie,
        
        # 4군: 역할 및 개인적 스타일
        'psychological_mindedness_py': Py,
        'flexibility_fx': Fx,
        'femininity_masculinity_fm': FM,
        
        # 벡터척도
        'vector_v1_extraversion': v1,
        'vector_v2_norm_orientation': v2,
        'vector_v3_self_realization': v3,
        'lifestyle_type': lifestyle_type,
        'overall_cpi_score': overall_cpi_score
    })
    cpi_counter += 1

df_cpi_results = pd.DataFrame(cpi_results)
df_cpi_results.to_csv('data/08_recruitment_cpi_results.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_cpi_results)}건 CPI 성격검사 결과 생성 완료")

# ============================================================================
# 5-4. recruitment_mmpi_results.csv - MMPI 진단검사 결과
print("\n[8/25] recruitment_mmpi_results.csv 생성 중...")

mmpi_results = []
mmpi_counter = 1

for emp in employees:
    # CPI 후 1-3일 후 MMPI 실시
    cpi_record = next((c for c in cpi_results if c['employee_id'] == emp['employee_id']), None)
    if cpi_record:
        cpi_date = datetime.strptime(cpi_record['test_date'], '%Y-%m-%d')
        test_date = cpi_date + timedelta(days=random.randint(1, 3))
    else:
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
        test_date = hire_date - timedelta(days=random.randint(15, 30))
    
    # 퇴사자 특성 반영 (우울, 불안 관련 척도 높음)
    if emp['status'] == '퇴사':
        depression_adj = 10  # 우울증 척도 높음
        anxiety_adj = 8      # 불안 관련 척도 높음
        adjustment_adj = 5   # 전반적 부적응
    else:
        depression_adj = 0
        anxiety_adj = 0
        adjustment_adj = 0
    
    # 타당도 척도 (일반적으로 낮은 점수 - 정상 범위)
    L = generate_t_score(45, 8, 30, 70)  # 허위척도
    F = generate_t_score(45, 8, 30, 75)  # 빈도척도
    K = generate_t_score(50, 8, 35, 70)  # 교정척도
    
    # 타당도 검증 (5% 정도는 무효 프로파일)
    if random.random() < 0.05:
        # 무효 프로파일 생성
        F = generate_t_score(75, 10, 70, 90)
        validity_status = 'INVALID'
    else:
        validity_status = 'VALID'
    
    # 임상 척도 (T점수: 평균 50, 표준편차 10, 70 이상 시 임상적 주의)
    Hs = generate_t_score(50 + adjustment_adj)  # 건강염려증
    D = generate_t_score(50 + depression_adj + adjustment_adj)  # 우울증
    Hy = generate_t_score(50 + adjustment_adj)  # 히스테리
    Pd = generate_t_score(50 + adjustment_adj)  # 반사회성
    Mf = generate_t_score(50)  # 남성성-여성성
    Pa = generate_t_score(50 + anxiety_adj + adjustment_adj)  # 편집증
    Pt = generate_t_score(50 + anxiety_adj + adjustment_adj)  # 강박증
    Sc = generate_t_score(50 + adjustment_adj)  # 정신분열병
    Ma = generate_t_score(50)  # 경조증
    Si = generate_t_score(50 + adjustment_adj)  # 사회적내향성
    
    # 임상 척도 상승 개수 (70T 이상)
    clinical_scales = [Hs, D, Hy, Pd, Pa, Pt, Sc, Ma, Si]
    clinical_elevation_count = sum(1 for score in clinical_scales if score >= 70)
    
    # 위험 수준 평가
    if clinical_elevation_count >= 3 or D >= 75 or Sc >= 75:
        risk_level = 'HIGH'
    elif clinical_elevation_count >= 1 or max(clinical_scales) >= 70:
        risk_level = 'MEDIUM'
    else:
        risk_level = 'LOW'
    
    # 전반적 적응도
    if risk_level == 'LOW' and validity_status == 'VALID':
        overall_adjustment = 'GOOD'
    elif risk_level == 'MEDIUM':
        overall_adjustment = 'FAIR'
    else:
        overall_adjustment = 'POOR'
    
    mmpi_results.append({
        'test_id': f'MMPI{mmpi_counter:04d}',
        'employee_id': emp['employee_id'],
        'test_date': test_date.strftime('%Y-%m-%d'),
        'recruitment_id': cpi_record['recruitment_id'] if cpi_record else f'REC{mmpi_counter:04d}',
        
        # 타당도 척도
        'lie_scale_l': L,
        'frequency_scale_f': F,
        'correction_scale_k': K,
        'validity_status': validity_status,
        
        # 임상 척도
        'hypochondriasis_hs': Hs,
        'depression_d': D,
        'hysteria_hy': Hy,
        'psychopathic_deviate_pd': Pd,
        'masculinity_femininity_mf': Mf,
        'paranoia_pa': Pa,
        'psychasthenia_pt': Pt,
        'schizophrenia_sc': Sc,
        'hypomania_ma': Ma,
        'social_introversion_si': Si,
        
        # 종합 평가
        'clinical_elevation_count': clinical_elevation_count,
        'risk_level': risk_level,
        'overall_adjustment': overall_adjustment
    })
    mmpi_counter += 1

df_mmpi_results = pd.DataFrame(mmpi_results)
df_mmpi_results.to_csv('data/09_recruitment_mmpi_results.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_mmpi_results)}건 MMPI 진단검사 결과 생성 완료")

# ============================================================================
# 6. onboarding_program.csv - 온보딩 프로그램  
print("\n[9/25] onboarding_program.csv 생성 중...")

onboarding_data = []
onboard_counter = 1

onboarding_programs = [
    '회사 소개 및 비전 공유',
    '조직문화 및 핵심가치 교육',
    '업무 시스템 사용법 교육',
    '부서별 업무 소개',
    '멘토 배정 및 OJT',
    '컴플라이언스 교육',
    '정보보안 교육',
]

# 최근 3년 입사자 대상
for emp in employees:
    hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
    if hire_date.year >= 2022 and emp['status'] == '재직':
        for idx, program in enumerate(onboarding_programs):
            program_date = hire_date + timedelta(days=idx * 2 + random.randint(0, 3))
            
            onboarding_data.append({
                'onboarding_id': f'ONB{onboard_counter:04d}',
                'employee_id': emp['employee_id'],
                'program_name': program,
                'scheduled_date': program_date.strftime('%Y-%m-%d'),
                'completion_status': random.choices(['완료', '미완료'], weights=[95, 5])[0],
                'satisfaction_score': round(random.uniform(3.5, 5.0), 1)
            })
            onboard_counter += 1

df_onboarding = pd.DataFrame(onboarding_data)
df_onboarding.to_csv('data/10_onboarding_program.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_onboarding)}건 온보딩 프로그램 기록 생성 완료")

# ============================================================================
# 7. training_history.csv - 교육 이력
print("\n[10/25] training_history.csv 생성 중...")

training_data = []
train_counter = 1

training_courses = [
    ('Python 기초', 'Technical', 16),
    ('Python 심화', 'Technical', 24),
    ('데이터 분석 실무', 'Technical', 24),
    ('SQL 데이터베이스', 'Technical', 16),
    ('효과적인 커뮤니케이션', 'Soft Skill', 8),
    ('프레젠테이션 스킬', 'Soft Skill', 8),
    ('리더십 기본', 'Leadership', 16),
    ('리더십 심화', 'Leadership', 20),
    ('프로젝트 관리 실무', 'Management', 20),
    ('애자일 방법론', 'Management', 16),
    ('협업 스킬 향상', 'Soft Skill', 8),
    ('AI/ML 기초', 'Technical', 32),
    ('AI/ML 실무', 'Technical', 40),
    ('문제해결 기법', 'Soft Skill', 12),
    ('디자인 씽킹', 'Soft Skill', 16),
    ('클라우드 컴퓨팅', 'Technical', 24),
    ('정보보안', 'Compliance', 8),
    ('개인정보보호', 'Compliance', 4),
]

for emp in employees:
    if emp['status'] == '재직':
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
        years_of_service = 2024 - hire_date.year
        
        # 근속연수에 따라 교육 수 결정
        num_trainings = min(random.randint(2, 8), years_of_service * 2)
        selected_courses = random.sample(training_courses, min(num_trainings, len(training_courses)))
        
        for course_name, category, hours in selected_courses:
            # 입사 후 랜덤 날짜
            days_after_hire = random.randint(90, years_of_service * 365)
            training_date = hire_date + timedelta(days=days_after_hire)
            
            if training_date > datetime.now():
                continue
            
            training_data.append({
                'training_id': f'TRN{train_counter:04d}',
                'employee_id': emp['employee_id'],
                'training_name': course_name,
                'category': category,
                'training_hours': hours,
                'start_date': training_date.strftime('%Y-%m-%d'),
                'completion_date': (training_date + timedelta(days=hours//2)).strftime('%Y-%m-%d'),
                'completion_status': random.choices(['수료', '미수료'], weights=[95, 5])[0],
                'assessment_score': round(random.uniform(70, 100), 1)
            })
            train_counter += 1

df_training = pd.DataFrame(training_data)
df_training.to_csv('data/11_training_history.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_training)}건 교육 이력 생성 완료")

print("\n" + "=" * 80)
print("B그룹 채용/온보딩/교육 데이터 생성 완료")
print("=" * 80)

# ============================================================================
# C그룹: 프로젝트 및 평가 데이터
# ============================================================================

# 8. project_history.csv - 프로젝트 이력
print("\n[11/25] project_history.csv 생성 중...")

project_data = []
project_counter = 1

# 다양한 프로젝트 생성 (2020-2024)
project_names = [
    '고객 데이터 분석 플랫폼', 'HR 챗봇 개발', '모바일 앱 리뉴얼', 
    '클라우드 마이그레이션', 'AI 추천 시스템', '레거시 시스템 개선',
    '보안 강화 프로젝트', '마케팅 자동화', 'CRM 시스템 구축',
    '데이터 웨어하우스 구축', 'API 게이트웨이 개발', 'MSA 전환',
    '고객 포털 개발', '내부 업무 시스템', '모니터링 시스템',
    'BI 대시보드 구축', '챗봇 고도화', '검색 엔진 최적화',
    '결제 시스템 개선', '인증 시스템 개선'
]

projects_list = []
for year in range(2020, 2025):
    num_projects = random.randint(8, 15)
    for i in range(num_projects):
        project_id = f'PRJ_{year}_{i+1:02d}'
        project_name = random.choice(project_names)
        start_month = random.randint(1, 10)
        duration_months = random.randint(3, 12)
        start_date = f'{year}-{start_month:02d}-{random.randint(1, 28):02d}'
        end_date = (datetime.strptime(start_date, '%Y-%m-%d') + timedelta(days=duration_months*30)).strftime('%Y-%m-%d')
        
        projects_list.append((project_id, project_name, start_date, end_date))

# 각 프로젝트에 직원 배정
for proj_id, proj_name, start_date, end_date in projects_list:
    # 프로젝트 규모 (3-10명)
    team_size = random.randint(3, 10)
    
    # 재직 중인 직원 중 랜덤 선택
    active_employees = [e for e in employees if e['status'] == '재직']
    selected_team = random.sample(active_employees, min(team_size, len(active_employees)))
    
    roles = ['PL', '개발자', '개발자', 'QA', '기획자', '디자이너', 'PM', '아키텍트']

    for idx, emp in enumerate(selected_team):
        role = roles[idx % len(roles)]

        project_data.append({
            'project_member_id': f'PM{project_counter:04d}',
            'employee_id': emp['employee_id'],
            'project_id': proj_id,
            'project_name': proj_name,
            'role': role,
            'pm_qualitative_feedback': random.choice([
                # 우수 성과 (40%)
                (
                    f"프로젝트 목표 {random.randint(105, 130)}% 달성. "
                    f"{random.choice(['일정을 앞당겨', '품질 기준을 초과하여', '예산 대비 효율적으로'])} 완수했으며, "
                    f"{random.choice(['팀원들의 신뢰', '이해관계자 만족도', '기술적 완성도'])}가 매우 높음."
                ),
                (
                    f"{random.choice(['복잡한 기술 이슈', '일정 지연 리스크', '요구사항 변경'])}를 "
                    f"{random.choice(['창의적으로', '신속하게', '체계적으로'])} 해결. "
                    f"{random.choice(['프로젝트 성공의 핵심 기여자', '팀의 롤모델', '기술 리더 역할 수행'])}."
                ),
                (
                    f"{random.choice(['탁월한 문제 해결 능력', '뛰어난 커뮤니케이션', '적극적인 책임감'])}으로 프로젝트에 기여. "
                    f"{random.choice(['향후 리더 역할 기대', '지속적 성장 예상', '핵심 인재로 평가'])}됨."
                ),
                # 양호 성과 (40%)
                (
                    f"맡은 역할을 성실히 수행. "
                    f"{random.choice(['기본 목표 달성', '안정적인 업무 처리', '주어진 작업 완수'])}. "
                    f"{random.choice(['보다 주도적인 역할 기대', '도전적 목표 설정 권장', '역량 확장 필요'])}."
                ),
                (
                    f"{random.choice(['일정대로', '큰 이슈 없이', '요구사항에 맞춰'])} 업무 완수. "
                    f"{random.choice(['팀과의 협업 양호', '기술적 역량 발휘', '책임감 있는 태도'])}. "
                    f"다음 프로젝트에서 {random.choice(['더 큰 역할 기대', '리더십 발휘 필요', '전문성 심화 요구'])}."
                ),
                (
                    f"전반적으로 만족스러운 기여. "
                    f"{random.choice(['커뮤니케이션 개선', '일정 관리 능력 향상', '기술 역량 강화'])} 시 더 큰 성과 기대."
                ),
                # 개선 필요 (20%)
                (
                    f"기본 작업은 완수했으나, "
                    f"{random.choice(['일정 준수에 어려움', '품질 기준 미달 부분 존재', '커뮤니케이션 개선 필요'])}. "
                    f"{random.choice(['추가 교육 권장', '멘토링 지원 필요', '역량 강화 계획 수립'])}."
                ),
                (
                    f"{random.choice(['타 팀과의 협업', '요구사항 이해', '기술적 난이도 해결'])}에서 어려움 노출. 개선 방안 논의 필요."
                ),
            ]),
            'peer_qualitative_feedback': random.choice([
                # 매우 긍정적 (30%)
                (
                    f"{random.choice(['항상 동료를 먼저 생각하고', '어려울 때 적극적으로 도와주며', '팀 분위기를 밝게 만들고'])} "
                    f"{random.choice(['신뢰할 수 있는', '함께 일하기 좋은', '배울 점이 많은'])} 동료. "
                    f"{random.choice(['전문성도 뛰어남', '커뮤니케이션이 탁월함', '문제 해결 능력 우수'])}."
                ),
                (
                    f"{random.choice(['기술적으로 뛰어나며', '책임감이 강하고', '열정적으로 일하며'])} "
                    f"{random.choice(['팀원들에게 지식을 공유', '후배들을 잘 가르침', '어려운 문제도 함께 고민'])}해줌. "
                    f"{random.choice(['팀의 기둥', '핵심 멤버', '없어서는 안 될 동료'])}."
                ),
                (
                    f"프로젝트 진행 중 {random.choice(['적극적인 소통', '빠른 피드백', '건설적인 의견 제시', '유연한 협업 태도'])}로 팀워크 향상에 기여. "
                    f"{random.choice(['함께 일하고 싶은 동료', '신뢰도 높음', '팀 성과에 큰 기여'])}."
                ),
                # 긍정적 (50%)
                (
                    f"{random.choice(['협력적이고', '성실하며', '책임감 있게'])} 업무를 수행. "
                    f"{random.choice(['커뮤니케이션 원활', '팀워크 양호', '맡은 일 잘 처리'])}함."
                ),
                (
                    f"{random.choice(['적극적으로 참여', '필요한 지원 제공', '협업에 긍정적'])}. "
                    f"{random.choice(['함께 일하기 좋음', '동료로서 만족', '믿고 맡길 수 있음'])}."
                ),
                (
                    f"프로젝트에 {random.choice(['성실히 기여', '전문성 발휘', '책임감 있게 참여'])}. "
                    f"{random.choice(['특별한 이슈 없음', '원활한 협업', '안정적인 성과'])}."
                ),
                # 보통/개선 필요 (20%)
                (
                    f"{random.choice(['기본적인 협업은 수행하나', '업무는 처리하지만', '맡은 역할은 하나'])} "
                    f"{random.choice(['커뮤니케이션이 부족', '주도적 참여 아쉬움', '적극성 필요'])}. "
                    f"{random.choice(['개선 여지 있음', '더 적극적인 참여 기대', '소통 개선 필요'])}."
                ),
            ]),
            'start_date': start_date,
            'end_date': end_date,
        })
        project_counter += 1

df_projects = pd.DataFrame(project_data)
df_projects.to_csv('data/12_project_history.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_projects)}건 프로젝트 이력 생성 완료")

# ============================================================================
# 9. performance_review.csv - 성과 평가
print("\n[12/25] performance_review.csv 생성 중...")

performance_data = []
review_counter = 1

review_periods = ['2022 H1', '2022 H2', '2023 H1', '2023 H2', '2024 H1']
grade_distribution = ['S', 'A', 'A', 'A', 'B', 'B', 'B', 'B', 'C', 'C', 'D']

for emp in employees:
    if emp['status'] == '재직':
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')

        for period in review_periods:
            year = int(period.split()[0])
            half = period.split()[1]

            if year < hire_date.year:
                continue
            if year == hire_date.year and half == 'H1' and hire_date.month > 6:
                continue

            # 성과 등급 (정규분포 기반)
            grade = random.choice(grade_distribution)

            # 등급별 코멘트 (반기 평가용 - 구체적이고 다양하게)
            comments_by_grade = {
                'S': [
                    (
                        f"반기 목표 {random.randint(130, 160)}% 달성으로 탁월한 성과. "
                        f"{random.choice(['핵심 프로젝트를 성공으로 이끔', '팀 전체 성과 향상에 기여', '혁신적 아이디어로 비즈니스 임팩트', '기술적 난제 해결로 회사 발전 기여'])}. "
                        f"{random.choice(['승진 적극 추천', '핵심인재로 관리', '보상 상향 필요', '리더 역할 부여 검토'])}."
                    ),
                    (
                        f"{random.choice(['뛰어난 리더십', 'exceptional한 전문성', '탁월한 실행력', '창의적 문제 해결'])}으로 조직에 큰 가치 창출. "
                        f"{random.choice(['차세대 리더 육성 대상', '경쟁사 스카우트 우려', '장기 유지 전략 필요', '보상 패키지 재검토'])}."
                    ),
                    (
                        f"기대를 크게 상회하는 성과. "
                        f"{random.choice(['고객사로부터 극찬', '이해관계자 만족도 최고', '프로젝트 수주 기여', '회사 평판 제고'])}. "
                        "회사의 미래를 책임질 핵심 인재."
                    ),
                ],
                'A': [
                    (
                        f"반기 목표 {random.randint(105, 120)}% 달성. "
                        f"{random.choice(['안정적이고 우수한 성과', '기대에 부응하는 기여', '전문성을 바탕으로 한 성과', '팀 목표 달성에 기여'])}. "
                        f"{random.choice(['리더십 기회 제공 검토', '전문가 트랙 육성', '도전적 과제 부여', '승진 후보 검토'])}."
                    ),
                    (
                        f"{random.choice(['기술적 전문성', '프로젝트 수행 능력', '협업 및 소통 역량', '책임감과 실행력'])} 우수. "
                        f"{random.choice(['지속적 성장 기대', '핵심 프로젝트 투입', '역량 확장 지원', '보상 인센티브'])}."
                    ),
                    (
                        f"우수한 성과. "
                        f"{random.choice(['전략적 사고', '리더십 역량', '글로벌 마인드', '혁신 역량'])} 개발 시 S등급 도약 가능. "
                        f"{random.choice(['교육 투자 예정', '멘토링 프로그램', '해외 연수 검토', '경력 개발 계획 수립'])}."
                    ),
                ],
                'B': [
                    (
                        f"기본 목표 달성. "
                        f"{random.choice(['일부 지연 발생', '품질 기준 충족', '평균 수준 성과', '무난한 업무 처리'])}. "
                        f"{random.choice(['주도성 강화', '기술 역량 보완', '커뮤니케이션 개선', '효율성 제고'])} 필요."
                    ),
                    (
                        f"{random.choice(['안정적이나 도전 부족', '맡은 일은 하나 확장성 없음', '평범한 수준', '기대치 수준'])}. "
                        f"{random.choice(['더 높은 목표 설정 권장', '자기주도적 개선', '적극성 제고', '시야 확대'])} 필요."
                    ),
                    (
                        f"평균적 성과. "
                        f"{random.choice(['프로세스 개선 기여도 낮음', '혁신 시도 미흡', '수동적 업무 태도', '성장 정체 우려'])}. "
                        f"{random.choice(['1:1 코칭', '교육 기회', '멘토 배정', '개선 계획'])} 지원."
                    ),
                ],
                'C': [
                    (
                        f"목표 달성률 {random.randint(60, 75)}%. "
                        f"{random.choice(['역량 부족', '태도 문제', '우선순위 오류', '협업 어려움'])} 파악. "
                        f"{random.choice(['집중 육성', '업무 재배치', 'PIP 수립', '멘토링 강화'])} 시급."
                    ),
                    (
                        f"{random.choice(['기대 이하 성과', '개선 미흡', '반복적 실수', '목표 이해 부족'])}. "
                        f"3개월 내 {random.choice(['명확한 개선', '구체적 발전', '태도 변화', '역량 향상'])} 없으면 "
                        f"{random.choice(['재배치 검토', '계약 갱신 논의', '추가 조치', '진로 상담'])}."
                    ),
                ],
                'D': [
                    (
                        f"심각한 수준의 저성과. "
                        f"{random.choice(['즉시 개선 조치', '역량 재평가', '적합성 검토', '근본 원인 파악'])} 필요. "
                        f"{random.choice(['PIP 즉시 적용', '전문가 코칭', '업무 전환', '고용 유지 재검토'])}."
                    ),
                ]
            }

            performance_data.append({
                'review_id': f'REV{review_counter:04d}',
                'employee_id': emp['employee_id'],
                'review_period': period,
                'final_grade': grade,
                'manager_comment_development': random.choice(comments_by_grade[grade])
            })
            review_counter += 1

df_performance = pd.DataFrame(performance_data)
df_performance.to_csv('data/13_performance_review.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_performance)}건 성과 평가 기록 생성 완료")

# ============================================================================
# 9-1. continuous_performance_review.csv - 수시 성과평가 (자기평가 + 상사평가)
print("\n[13/25] continuous_performance_review.csv 생성 중...")

continuous_review_data = []
continuous_review_counter = 1

# 수시 평가 유형
review_types = ['분기 평가', '프로젝트 종료 평가', '수시 평가', '목표 달성 평가']

for emp in employees:
    if emp['status'] == '재직':
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')

        # 2022-2024년 동안 직원당 5-15회의 수시 평가
        years_of_service = min(2024 - hire_date.year, 3)
        num_reviews = random.randint(3, 5) * years_of_service

        for _ in range(num_reviews):
            # 평가 대상 기간 (1-4개월)
            period_length = random.randint(30, 120)
            period_end_date = hire_date + timedelta(days=random.randint(30, 1095))

            if period_end_date > datetime.now():
                continue

            period_start_date = period_end_date - timedelta(days=period_length)

            # 자기평가 작성일 (평가 대상 기간 종료 후 1-7일)
            self_eval_date = period_end_date + timedelta(days=random.randint(1, 7))
            self_eval_timestamp = self_eval_date + timedelta(
                hours=random.randint(9, 18),
                minutes=random.randint(0, 59)
            )

            # 상사평가 작성일 (자기평가 후 2-10일)
            manager_eval_date = self_eval_date + timedelta(days=random.randint(2, 10))
            manager_eval_timestamp = manager_eval_date + timedelta(
                hours=random.randint(9, 18),
                minutes=random.randint(0, 59)
            )

            # 자기평가 등급 (일반적으로 높게 평가)
            self_rating_options = ['S', 'S', 'A', 'A', 'A', 'B', 'B']
            self_rating = random.choice(self_rating_options)

            # 상사평가 등급 (자기평가보다 보수적)
            manager_rating_map = {
                'S': random.choice(['S', 'A', 'A', 'A']),
                'A': random.choice(['A', 'A', 'B', 'B']),
                'B': random.choice(['B', 'B', 'C']),
                'C': random.choice(['B', 'C', 'C']),
            }
            manager_rating = manager_rating_map.get(self_rating, 'B')

            # 자기평가 코멘트 (더욱 다양하고 구체적으로)
            achievement_details = [
                f"분기 목표 {random.randint(95, 135)}% 달성",
                f"{random.choice(['핵심 KPI', '주요 마일스톤', '중요 deliverable'])} {random.randint(3, 8)}건 완료",
                f"{random.choice(['신규 고객', '매출', '생산성', '품질 지표'])} {random.randint(10, 40)}% 향상",
                f"{random.choice(['프로젝트', '업무 개선안', '혁신 과제'])} 일정 대비 {random.randint(5, 20)}일 조기 완료",
            ]

            skill_development = [
                f"{random.choice(['Python', 'AI/ML', '클라우드', '데이터 분석', '프로젝트 관리'])} 역량을 새롭게 습득",
                f"{random.choice(['사내 교육', '외부 컨퍼런스', '온라인 강의', '실무 프로젝트'])}를 통해 전문성 강화",
                f"{random.choice(['신기술 도입', '프로세스 자동화', '업무 효율화', '품질 개선'])} 방안 제안 및 실행",
                f"{random.choice(['기술 블로그 작성', '사내 세미나 발표', '스터디 그룹 운영', '후배 멘토링'])}으로 지식 공유",
            ]

            collaboration = [
                f"{random.choice(['타 부서와', '유관 팀과', '외부 파트너와', '크로스 팀으로'])} {random.randint(3, 10)}회 이상 협업 프로젝트 수행",
                f"{random.choice(['커뮤니케이션 개선', '정기 미팅 주도', '문서화 강화', '투명한 정보 공유'])}로 협업 효율성 증대",
                f"팀 내 {random.choice(['갈등 조정', '의견 조율', '합의 도출', '문제 해결'])}에 기여",
                f"{random.choice(['신규 입사자', '주니어 개발자', '타 팀 동료', '프로젝트 팀원'])} {random.randint(2, 5)}명 지원",
            ]

            self_comments = [
                (
                    f"해당 기간 동안 {random.choice(achievement_details)}하였습니다. "
                    f"특히 {random.choice(skill_development)}하여 전문성을 높였으며, "
                    f"{random.choice(collaboration)}하였습니다."
                ),
                (
                    f"{random.choice(achievement_details)}한 것이 가장 큰 성과입니다. "
                    f"또한 {random.choice(collaboration)}하고, "
                    f"{random.choice(['개인 역량 개발에도 집중', '지속적인 학습 진행', '업무 프로세스 개선에 기여'])}했습니다."
                ),
                (
                    f"핵심 업무 성과로 {random.choice(achievement_details)}했고, "
                    f"{random.choice(skill_development)}했습니다. "
                    f"앞으로도 {random.choice(['더 도전적인 목표 달성', '팀 기여도 확대', '리더십 역량 강화', '전문가로 성장'])}하고자 합니다."
                ),
                (
                    f"이번 기간 {random.choice(achievement_details)}하며 기대 이상의 성과를 냈다고 생각합니다. "
                    f"{random.choice(collaboration)}하는 과정에서 "
                    f"{random.choice(['팀워크의 중요성', '소통의 가치', '협업의 시너지', '상호 신뢰'])}를 다시 한번 깨달았습니다."
                ),
                (
                    f"{random.choice(skill_development)}하고, {random.choice(achievement_details)}했습니다. "
                    f"특히 {random.choice(['어려운 기술 문제 해결', '고객 요구사항 초과 달성', '프로세스 혁신 제안', '팀 생산성 향상'])}에서 기여도가 컸다고 자평합니다."
                ),
            ]

            # 상사평가 코멘트 (등급별로 구체적이고 다양하게)
            manager_comments_by_grade = {
                'S': [
                    (
                        f"목표를 {random.randint(120, 150)}% 초과 달성하는 탁월한 성과를 보였습니다. "
                        f"{random.choice(['기술적 난제를 혁신적으로 해결', '팀 성과를 이끄는 핵심 역할 수행', '이해관계자들로부터 극찬', '회사 전체 성과에 기여'])}했으며, "
                        f"{random.choice(['차세대 리더로 육성 필요', '핵심 프로젝트 리더 역할 부여 검토', '승진 후보로 추천', '보상 상향 조정 필요'])}."
                    ),
                    (
                        f"{random.choice(['탁월한 리더십', '뛰어난 기술력', '창의적 문제 해결 능력', 'exceptional한 실행력'])}으로 프로젝트를 성공으로 이끌었습니다. "
                        f"{random.choice(['팀원들의 롤모델', '조직의 핵심 자산', '반드시 유지해야 할 인재', '경쟁사 스카우트 우려'])}로 평가됩니다."
                    ),
                    (
                        f"기대를 훨씬 상회하는 성과입니다. "
                        f"{random.choice(['복잡한 프로젝트를 단독으로 이끔', '여러 위기 상황을 돌파', '팀 전체 생산성 향상에 기여', '신규 비즈니스 기회 창출'])}. "
                        "회사의 미래를 책임질 인재입니다."
                    ),
                ],
                'A': [
                    (
                        f"목표 {random.randint(100, 115)}% 달성으로 우수한 성과를 보였습니다. "
                        f"{random.choice(['기술적 전문성', '안정적인 프로젝트 수행', '적극적인 협업 태도', '높은 업무 이해도'])}가 돋보였으며, "
                        f"{random.choice(['리더십 역량 개발 시 더 큰 성장 기대', '다음 단계 역할 준비 필요', '전문가로서 입지 확고', '지속적 우수 성과 유지'])}."
                    ),
                    (
                        f"{random.choice(['일정 내 품질 기준 충족', '이해관계자 기대 부응', '팀 목표 달성에 기여', '안정적 결과물 산출'])}하는 우수한 성과. "
                        f"{random.choice(['보다 도전적인 과제 부여 검토', '역량 확장 기회 제공 예정', '차기 프로젝트 핵심 역할 기대', '승진 검토 대상'])}."
                    ),
                    (
                        f"전반적으로 만족스러운 성과입니다. "
                        f"{random.choice(['커뮤니케이션 역량', '기술적 깊이', '리더십 발휘', '문제 해결 능력'])}에서 강점을 보였으나, "
                        f"{random.choice(['더 큰 그림을 보는 시각', '전략적 사고', '이니셔티브 발휘', '타 팀 협업'])} 강화 시 S등급 기대."
                    ),
                ],
                'B': [
                    (
                        f"기본 목표는 달성했으나 "
                        f"{random.choice(['일정이 다소 지연', '품질 기준 일부 미달', '커뮤니케이션 개선 필요', '주도성 부족'])}한 부분이 있습니다. "
                        f"{random.choice(['시간 관리 능력 향상', '기술 역량 강화 교육', '협업 스킬 개발', '적극성 제고'])} 권장."
                    ),
                    (
                        f"{random.choice(['맡은 업무는 수행', '주어진 역할 완수', '기본 책임 이행'])}했으나, "
                        f"{random.choice(['보다 적극적인 태도', '능동적인 문제 해결', '창의적인 접근', '선제적 대응'])}이 필요합니다. "
                        f"다음 평가에서는 {random.choice(['도전적 목표 설정', '자기주도적 개선', '역량 향상 노력', '성과 제고'])} 기대."
                    ),
                    (
                        f"평균적인 성과입니다. "
                        f"{random.choice(['기술적 역량 보완', '업무 효율성 개선', '커뮤니케이션 강화', '시야 확대'])} 필요. "
                        f"{random.choice(['멘토링 지원 예정', '교육 기회 제공', '1:1 코칭 진행', '개선 계획 수립'])}하겠습니다."
                    ),
                ],
                'C': [
                    (
                        f"목표 달성률 {random.randint(60, 80)}%로 개선이 필요합니다. "
                        f"{random.choice(['기술적 어려움', '시간 관리 미흡', '우선순위 설정 오류', '협업 문제'])}가 주된 원인으로 파악됩니다. "
                        f"{random.choice(['집중 육성 프로그램 배정', '멘토 지정 및 지원 강화', '업무 범위 재조정', '역량 개발 계획 수립'])} 예정."
                    ),
                    (
                        f"{random.choice(['업무 이해도 부족', '실행력 미흡', '태도 개선 필요', '역량 격차'])}로 인해 기대에 미치지 못했습니다. "
                        f"향후 3개월간 {random.choice(['집중 관리', '정기 점검', '개선 모니터링', '1:1 코칭'])}을 통해 개선 필요."
                    ),
                    (
                        f"성과가 기대 수준 이하입니다. "
                        f"{random.choice(['즉시 개선 조치', '역량 진단 및 교육', '업무 재배치 검토', 'PIP(성과개선계획) 수립'])} 필요. "
                        "차기 평가에서 명확한 개선 확인 필요."
                    ),
                ]
            }

            self_comments_2 = [
                (
                    f"해당 기간 동안 {random.choice(achievement_details)}하였습니다. "
                    f"{random.choice(skill_development)}하며 전문성을 높였고, {random.choice(collaboration)}하였습니다."
                ),
                (
                    f"{random.choice(achievement_details)}한 것이 주요 성과입니다. "
                    f"특히 {random.choice(['어려운 기술 이슈를 독자적으로 해결', '이해관계자 기대를 초과 충족', '팀 전체 생산성 향상에 기여', '프로세스 혁신안 제안 및 적용'])}한 점이 의미 있었습니다."
                ),
                (
                    f"{random.choice(skill_development)}하고, {random.choice(achievement_details)}하며 기대 이상의 결과를 냈다고 자평합니다. "
                    f"{random.choice(collaboration)}하는 과정도 개인 성장에 도움이 되었습니다."
                ),
                (
                    f"이번 평가 기간의 핵심 성과는 {random.choice(achievement_details)}입니다. "
                    f"또한 {random.choice(['업무 효율화로 팀 전체 시간 20% 절감', '신규 도구 도입으로 품질 향상', '고객 만족도 점수 상승에 기여', '비용 절감 아이디어 실행'])}했습니다."
                ),
                (
                    f"{random.choice(collaboration)}하며 팀워크를 강화했고, {random.choice(achievement_details)}하는 성과를 냈습니다. "
                    f"향후 {random.choice(['더 큰 책임의 역할', '리더 포지션', '전문가 트랙', '혁신 프로젝트 리딩'])}에 도전하고 싶습니다."
                ),
            ]

            continuous_review_data.append({
                'review_id': f"CR{continuous_review_counter:05d}",
                'employee_id': emp['employee_id'],
                'review_type': random.choice(review_types),
                'evaluation_period_start': period_start_date.strftime('%Y-%m-%d'),
                'evaluation_period_end': period_end_date.strftime('%Y-%m-%d'),
                'self_evaluation_timestamp': self_eval_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'self_rating': self_rating,
                'self_comment': random.choice(self_comments_2),
                'manager_evaluation_timestamp': manager_eval_timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'manager_rating': manager_rating,
                'manager_comment': random.choice(manager_comments_by_grade.get(manager_rating, manager_comments_by_grade['B'])),
                'rating_gap': 1 if self_rating != manager_rating else 0,
                'evaluation_status': '완료'
            })
            continuous_review_counter += 1

df_continuous_review = pd.DataFrame(continuous_review_data)
df_continuous_review.to_csv('data/14_continuous_performance_review.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_continuous_review)}건 수시 성과평가 기록 생성 완료 (자기평가 + 상사평가 타임스탬프 포함)")

# ============================================================================
# 9-2. goal_management.csv - 목표 관리 (OKR/MBO)
print("\n[14/25] goal_management.csv 생성 중...")

goal_data = []
goal_counter = 1

goal_categories = ['업무 성과', '역량 개발', '프로젝트 완수', '프로세스 개선', '협업 강화', '혁신 과제']
goal_types = ['OKR', 'MBO', 'KPI']

for emp in employees:
    if emp['status'] == '재직':
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')

        # 2022-2024년 각 분기별 목표 설정
        for year in range(max(2022, hire_date.year), 2025):
            for quarter in ['Q1', 'Q2', 'Q3', 'Q4']:
                quarter_start_month = {'Q1': 1, 'Q2': 4, 'Q3': 7, 'Q4': 10}[quarter]
                goal_set_date = datetime(year, quarter_start_month, random.randint(1, 7))

                if goal_set_date < hire_date or goal_set_date > datetime.now():
                    continue

                # 분기당 2-4개 목표
                num_goals = random.randint(2, 4)

                for _ in range(num_goals):
                    category = random.choice(goal_categories)
                    goal_type = random.choice(goal_types)

                    # 목표 진행률 (분기가 지났으면 완료, 현재 분기면 진행중)
                    if year < 2024 or (year == 2024 and quarter_start_month < datetime.now().month):
                        progress = random.randint(70, 100)
                        status = '완료' if progress >= 80 else '부분 달성'
                    else:
                        progress = random.randint(30, 80)
                        status = '진행중'

                    # 목표 설명 생성
                    goal_descriptions = {
                        '업무 성과': [
                            f"{random.choice(['매출', '생산성', '품질', '고객 만족도'])} {random.randint(10, 30)}% 향상",
                            f"핵심 업무 지표 목표치 {random.randint(90, 120)}% 달성",
                        ],
                        '역량 개발': [
                            f"{random.choice(['Python', 'AI/ML', '리더십', '데이터 분석'])} 역량 강화 교육 이수",
                            "신규 기술 스택 학습 및 프로젝트 적용",
                        ],
                        '프로젝트 완수': [
                            f"{random.choice(['개발', '개선', '구축'])} 프로젝트 일정 내 완수",
                            f"프로젝트 목표 품질 기준 {random.randint(90, 100)}% 달성",
                        ],
                        '프로세스 개선': [
                            f"업무 프로세스 효율성 {random.randint(15, 40)}% 개선",
                            f"반복 업무 자동화로 시간 {random.randint(20, 50)}% 절감",
                        ],
                        '협업 강화': [
                            f"크로스 팀 협업 프로젝트 {random.randint(2, 5)}건 이상 참여",
                            "지식 공유 세션 주도 및 팀 역량 향상 기여",
                        ],
                        '혁신 과제': [
                            f"신규 아이디어 제안 및 실행 {random.randint(1, 3)}건",
                            "혁신 활동을 통한 비용 절감 또는 수익 창출",
                        ]
                    }

                    goal_data.append({
                        'goal_id': f'GOAL{goal_counter:05d}',
                        'employee_id': emp['employee_id'],
                        'goal_type': goal_type,
                        'goal_category': category,
                        'goal_description': random.choice(goal_descriptions[category]),
                        'target_period': f"{year} {quarter}",
                        'set_date': goal_set_date.strftime('%Y-%m-%d'),
                        'target_completion_date': (goal_set_date + timedelta(days=90)).strftime('%Y-%m-%d'),
                        'progress_percentage': progress,
                        'status': status,
                        'final_achievement_rate': progress if status == '완료' else None,
                        'manager_id': emp['manager_id'],
                    })
                    goal_counter += 1

df_goals = pd.DataFrame(goal_data)
df_goals.to_csv('data/15_goal_management.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_goals)}건 목표 관리 기록 생성 완료")

# ============================================================================
# 9-3. exit_interview.csv - 퇴사자 인터뷰
print("\n[15/25] exit_interview.csv 생성 중...")

exit_interview_data = []
exit_counter = 1

exit_reasons_primary = {
    '더 나은 기회': ['더 좋은 연봉 제안', '커리어 성장 기회', '원하는 직무로 이직', '더 큰 회사로 이직'],
    '보상 불만': ['낮은 연봉', '승진 누락', '동종 업계 대비 낮은 처우', '성과 대비 보상 불균형'],
    '업무 불만': ['과도한 업무량', '업무 내용 불만족', '비효율적인 프로세스', '의미 없는 업무'],
    '상사/관계': ['상사와의 갈등', '팀 내 갈등', '조직 문화 부적응', '커뮤니케이션 문제'],
    '성장 정체': ['경력 개발 기회 부족', '교육 기회 제한', '기술 발전 기회 없음', '역량 활용 불가'],
    '워라밸': ['과도한 야근', '휴가 사용 제한', '유연근무 불가', '번아웃'],
    '개인 사유': ['학업', '건강', '가족', '창업'],
}

for emp in employees:
    if emp['status'] == '퇴사':
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
        # 퇴사일 설정 (입사 후 6개월 ~ 8년)
        exit_date = hire_date + timedelta(days=random.randint(180, 2920))
        if exit_date > datetime.now():
            exit_date = datetime.now() - timedelta(days=random.randint(30, 365))

        # 인터뷰 일자 (퇴사일 1-7일 전)
        interview_date = exit_date - timedelta(days=random.randint(1, 7))

        # 주 퇴사 사유 선택
        primary_category = random.choice(list(exit_reasons_primary.keys()))
        primary_reason = random.choice(exit_reasons_primary[primary_category])

        # 부차적 사유
        secondary_categories = [k for k in exit_reasons_primary.keys() if k != primary_category]
        secondary_reason = random.choice(exit_reasons_primary[random.choice(secondary_categories)])

        # 회사 추천 의향 (퇴사 사유에 따라)
        if primary_category in ['개인 사유', '더 나은 기회']:
            recommend_score = round(random.uniform(3.5, 5.0), 1)
        elif primary_category in ['보상 불만', '성장 정체']:
            recommend_score = round(random.uniform(2.5, 4.0), 1)
        else:  # 상사/관계, 업무 불만, 워라밸
            recommend_score = round(random.uniform(1.5, 3.5), 1)

        # 정성 의견 (퇴사 사유별로 구체적이고 진솔하게)
        positive_aspects = [
            random.choice(["훌륭한 동료들", "우수한 기술 스택", "도전적인 프로젝트", "좋은 학습 기회", "전문성 개발 환경"]),
            random.choice(["체계적인 온보딩", "멘토의 헌신적 지원", "자유로운 기술 선택", "수평적 문화", "복리후생"]),
        ]

        negative_aspects = [
            f"{primary_reason} 문제가 {random.choice(['지속적으로', '반복적으로', '구조적으로'])} 발생",
            f"{secondary_reason}까지 겹치면서 {random.choice(['더 이상 개선 기대 어려움', '한계에 도달', '지속 근무 불가 판단', '커리어 재고'])}",
            f"{random.choice(['여러 차례 개선 요청했으나 변화 없음', '상사와 논의했으나 해결 안 됨', 'HR과 상담했으나 실질적 조치 없음', '기대했던 변화가 일어나지 않음'])}",
        ]

        qualitative_feedback = [
            (
                f"재직 기간 동안 {random.choice(positive_aspects)}에는 감사했습니다. 그러나 {random.choice(negative_aspects)}하여 최종적으로 퇴사를 결정했습니다. "
                f"특히 {primary_reason}은(는) {random.choice(['반드시 개선되어야 할 부분', '조직의 지속가능성을 위해 해결 필요', '우수 인재 유지를 위해 시급한 과제', '후배들을 위해서라도 변화 필요'])}입니다."
            ),
            (
                f"{random.choice(['처음에는 기대가 컸으나', '입사 당시 약속과 달리', '시간이 지나면서'])} {primary_reason} 문제가 심화되었습니다. {random.choice(positive_aspects)}은(는) 좋았지만, {secondary_reason}까지 겹치면서 {random.choice(['더 나은 환경을 찾아', '커리어 성장을 위해', '건강과 가정을 위해', '미래를 위해'])} 떠나기로 결정했습니다."
            ),
            (
                f"솔직히 말하면 {primary_reason}이(가) 결정적 이유입니다. {random.choice(['수차례 개선을 요청했지만 변화 없었고', '팀 내 여러 동료가 같은 문제 제기했으나', '상황이 점점 악화되면서', '더 이상 참기 어려운 수준이 되어'])} 퇴사를 결심했습니다. {random.choice(positive_aspects)}은(는) 아쉽지만, {random.choice(['개인 성장', '정신 건강', '커리어 발전', '일과 삶의 균형'])}을 위해 불가피한 선택이었습니다."
            ),
            (
                f"{random.choice(['회사의 비전과 제품에는 공감하나', '동료들은 훌륭하지만', '기술적 환경은 좋으나', '복지는 만족스러우나'])} {primary_reason}과(와) {secondary_reason} 때문에 {random.choice(['더 이상 성장하기 어렵다', '장기적으로 함께하기 힘들다', '다른 곳에서 기회를 찾아야겠다', '변화가 필요하다'])}고 판단했습니다. "
                f"{random.choice(['후배들을 위해서라도 이 부분은 개선되길', '조직 문화 혁신이 시급하다고', '리더십 교육이 필요하다고', '인사 정책 재검토가 필요하다고'])} 생각합니다."
            ),
        ]

        # 개선 제안
        improvement_suggestions = {
            '더 나은 기회': '경력 개발 경로 명확화, 내부 이동 기회 확대',
            '보상 불만': '시장 경쟁력 있는 보상 체계 수립, 투명한 보상 정책',
            '업무 불만': '업무 프로세스 개선, 불필요한 업무 제거',
            '상사/관계': '리더십 교육 강화, 조직 문화 개선, 갈등 해결 메커니즘 구축',
            '성장 정체': '교육 예산 확대, 외부 컨퍼런스 참여 지원, 사내 스터디 활성화',
            '워라밸': '유연근무제 확대, 불필요한 야근 문화 개선, 휴가 사용 장려',
            '개인 사유': '해당 없음'
        }

        exit_interview_data.append({
            'exit_interview_id': f'EXIT{exit_counter:04d}',
            'employee_id': emp['employee_id'],
            'interview_date': interview_date.strftime('%Y-%m-%d'),
            'exit_date': exit_date.strftime('%Y-%m-%d'),
            'tenure_years': round((exit_date - hire_date).days / 365.25, 1),
            'primary_reason_category': primary_category,
            'primary_reason_detail': primary_reason,
            'secondary_reason': secondary_reason,
            'would_recommend_company': recommend_score,
            'overall_satisfaction': round(random.uniform(2.0, 4.5), 1),
            'qualitative_feedback': random.choice(qualitative_feedback),
            'improvement_suggestion': improvement_suggestions[primary_category],
            'rehire_eligible': random.choice(['Yes', 'Yes', 'Yes', 'No']),
        })
        exit_counter += 1

df_exit_interview = pd.DataFrame(exit_interview_data)
df_exit_interview.to_csv('data/16_exit_interview.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_exit_interview)}건 퇴사자 인터뷰 기록 생성 완료")

# ============================================================================
# 9-4. team_culture_survey.csv - 팀별 조직문화 서베이 (정성+정량)
print("\n[16/25] team_culture_survey.csv 생성 중...")

team_culture_data = []
culture_counter = 1

# 팀별 특성 부여 (일부 팀은 문제가 있고, 일부는 좋음)
team_characteristics = {}
for org_id, org_name, parent_org, div_name, _ in departments:
    # 랜덤하게 팀 문화 수준 결정
    culture_level = random.choice(['excellent', 'good', 'good', 'average', 'average', 'poor'])
    team_characteristics[org_id] = culture_level

culture_questions = {
    'q_psychological_safety': '팀 내에서 자유롭게 의견을 표현할 수 있다',
    'q_trust_in_leadership': '팀 리더를 신뢰한다',
    'q_collaboration': '팀원 간 협업이 잘 이루어진다',
    'q_innovation_encouragement': '새로운 아이디어와 시도가 장려된다',
    'q_work_life_balance': '적절한 업무량과 워라밸이 보장된다',
    'q_recognition': '성과와 기여가 인정받는다',
    'q_fairness': '공정한 대우를 받는다'
}

for emp in employees:
    if emp['status'] == '재직':
        for year in [2023, 2024]:
            hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
            if year < hire_date.year:
                continue

            survey_date = datetime(year, random.randint(10, 11), random.randint(1, 28))

            # 팀 특성에 따른 점수 조정
            team_culture = team_characteristics.get(emp['org_id'], 'average')

            if team_culture == 'excellent':
                base_score = 4.5
                std_dev = 0.3
            elif team_culture == 'good':
                base_score = 4.0
                std_dev = 0.4
            elif team_culture == 'average':
                base_score = 3.5
                std_dev = 0.5
            else:  # poor
                base_score = 2.5
                std_dev = 0.6

            scores = {}
            for q_code in culture_questions.keys():
                scores[q_code] = round(np.clip(np.random.normal(base_score, std_dev), 1.0, 5.0), 1)

            # 정성 의견 (팀 문화별로 구체적이고 다양하게)
            if team_culture == 'excellent':
                comments = [
                    (
                        f"우리 팀은 {random.choice(['심리적 안전감', '상호 신뢰', '개방적 소통', '협력 문화'])}이 매우 잘 형성되어 있습니다. "
                        f"{random.choice(['실패를 두려워하지 않고 도전', '자유롭게 의견을 나누며 혁신', '서로 존중하며 성장', '함께 문제를 해결'])}"
                        "하는 분위기가 정착되어 있어 "
                        f"{random.choice(['업무 만족도가 높습니다', '팀에 대한 자부심이 큽니다', '최고의 팀이라 생각합니다', '오래 함께하고 싶습니다'])}."
                    ),
                    (
                        f"팀장님이 {random.choice(['팀원의 성장을 진심으로 지원', '공정하고 투명하게 의사결정', '권한을 적절히 위임하고 신뢰', '개개인의 강점을 살려 활용'])}해주십니다. "
                        f"{random.choice(['정기적인 1:1 미팅에서 커리어 고민을 함께 나누고', '실패해도 배움의 기회로 삼으며', '성과는 공정하게 인정하고', '개인 사정도 배려'])}해주셔서 감사합니다."
                    ),
                    (
                        f"팀원 모두가 {random.choice(['서로 돕는 문화', '지식 공유', '건설적 피드백', '긍정적 에너지'])}를 만들어가고 있습니다. "
                        f"{random.choice(['어려운 프로젝트도 함께라면 해낼 수 있다는 믿음', '동료들과 함께 성장하는 느낌', '이 팀에서 최고의 경험', '타 부서 동료들이 부러워하는 팀'])}입니다."
                    ),
                ]
            elif team_culture == 'good':
                comments = [
                    (
                        f"팀 분위기는 {random.choice(['대체로 만족스럽습니다', '좋은 편입니다', '긍정적입니다'])}. "
                        f"{random.choice(['리더의 지원', '동료 간 협업', '업무 자율성', '공정한 평가'])}은 좋으나, "
                        f"{random.choice(['업무량 조절', '프로세스 개선', '더 나은 소통', '혁신 기회'])} 측면에서 개선 여지가 있습니다."
                    ),
                    (
                        f"{random.choice(['팀원들과의 관계', '업무 환경', '리더십 스타일', '협업 문화'])}에 만족하고 있습니다. "
                        f"다만 {random.choice(['과도한 회의', '불필요한 보고', '의사결정 속도', '업무 분배'])}가 다소 개선되면 더 좋을 것 같습니다."
                    ),
                    (
                        f"전반적으로 {random.choice(['함께 일하기 좋은', '신뢰할 수 있는', '성장할 수 있는', '안정적인'])} 팀입니다. "
                        f"{random.choice(['더 많은 도전 기회', '명확한 경력 경로', '공정한 보상', '워라밸 개선'])}이 보완되면 excellent한 팀이 될 것입니다."
                    ),
                ]
            elif team_culture == 'average':
                comments = [
                    (
                        f"{random.choice(['팀 내 소통이 원활하지 않을 때가 있습니다', '업무 분배가 불균형하다고 느낍니다', '의사결정 과정이 불투명합니다', '팀 비전이 명확하지 않습니다'])}. "
                        f"{random.choice(['정기 팀 미팅 활성화', '역할과 책임 명확화', '리더의 적극적 소통', '프로세스 개선'])}이 필요합니다."
                    ),
                    (
                        f"{random.choice(['업무량이 과도하여 번아웃 우려', '성과 인정이 부족', '성장 기회가 제한적', '불공정한 평가'])}됩니다. "
                        f"팀 문화 개선을 위한 {random.choice(['리더십 변화', 'HR 개입', '팀 워크샵', '솔직한 대화의 장'])}이 필요해 보입니다."
                    ),
                    (
                        f"팀 분위기가 {random.choice(['예전만 못합니다', '점점 악화되는 느낌', '개선이 시급합니다', '침체되어 있습니다'])}. "
                        f"{random.choice(['핵심 인재 이탈', '업무 동기 저하', '팀 내 갈등', '리더 신뢰 문제'])}로 인해 "
                        f"{random.choice(['조직 개편 필요', '리더십 교체 검토', '문화 혁신 시급', '구성원 의견 청취'])} 상황입니다."
                    ),
                ]
            else:  # poor
                comments = [
                    (
                        f"팀 문화가 심각한 수준입니다. "
                        f"{random.choice(['리더가 일방적으로 지시만 하고 피드백 무시', '팀원 간 경쟁만 부추기고 협업 없음', '야근이 강요되며 휴가 사용 눈치', '불공정한 평가와 편애'])}가 만연합니다. "
                        f"{random.choice(['이직 준비 중', '더 이상 견디기 어려움', 'HR 면담 요청 예정', '조직 개편 없으면 퇴사 고려'])}."
                    ),
                    (
                        f"{random.choice(['심리적 안전감 전무', '의견 제시하면 무시당함', '실수하면 공개적으로 질책', '성과는 리더 공, 실패는 팀원 책임'])}합니다. "
                        f"이런 환경에서는 {random.choice(['성장 불가능', '창의성 발휘 어려움', '장기 근무 의사 없음', '팀 애정 사라짐'])}. 근본적 변화 필요."
                    ),
                    (
                        f"팀장의 {random.choice(['구시대적 관리 방식', '소통 부재', '편파적 태도', '역량 부족'])}으로 팀 전체가 "
                        f"{random.choice(['번아웃', '좌절', '불신', '분열'])} 상태입니다. "
                        f"{random.choice(['다수 팀원이 이직 준비', '팀 재편 논의 중', '본부장 면담 요청', '집단 민원 검토'])}. 시급한 조치 필요."
                    ),
                    (
                        f"과도한 {random.choice(['업무량', '야근', '주말 근무', '불필요한 회의'])}과 "
                        f"{random.choice(['성과 무시', '보상 불공정', '경력 개발 기회 차단', '소통 단절'])}로 "
                        f"{random.choice(['팀 사기 최저', '우수 인재 대거 이탈', '프로젝트 실패 반복', '조직 신뢰 붕괴'])} 상황. 즉각적인 개입 요청합니다."
                    ),
                ]

            team_culture_data.append({
                'survey_id': f'TCULTURE{culture_counter:05d}',
                'employee_id': emp['employee_id'],
                'org_id': emp['org_id'],
                'org_name': emp['org_name'],
                'division_name': emp['division_name'],
                'survey_year': year,
                'survey_date': survey_date.strftime('%Y-%m-%d'),
                **scores,
                'overall_team_satisfaction': round(np.mean(list(scores.values())), 1),
                'qualitative_comment': random.choice(comments),
                'would_recommend_team': round(np.clip(np.random.normal(base_score, std_dev), 1.0, 5.0), 1),
            })
            culture_counter += 1

df_team_culture = pd.DataFrame(team_culture_data)
df_team_culture.to_csv('data/16_team_culture_survey.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_team_culture)}건 팀 조직문화 서베이 기록 생성 완료")

# ============================================================================
# 9-5. rewards_and_discipline.csv - 포상 및 징계 이력
print("\n[17/25] rewards_and_discipline.csv 생성 중...")

rewards_discipline_data = []
rd_counter = 1

# 포상 유형
reward_types = {
    '우수사원상': ('월간 우수사원 선정', 500000),
    '공로상': ('프로젝트 성공적 완수', 1000000),
    '혁신상': ('혁신 아이디어 제안 및 실행', 2000000),
    '팀워크상': ('팀 협업 우수', 300000),
    '고객만족상': ('고객 만족도 향상 기여', 1500000)
}

# 징계 유형
discipline_types = {
    '구두경고': '업무 태만',
    '서면경고': '무단 지각 반복',
    '감봉': '업무상 과실',
    '정직': '중대 규정 위반'
}

for emp in employees:
    if emp['status'] == '재직':
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
        years_of_service = 2024 - hire_date.year
        
        # 근속 1년 미만은 포상 대상에서 제외
        if years_of_service < 1:
            continue
        
        # 포상: 우수 직원은 여러 번, 일반 직원은 가끔
        num_rewards = random.choices([0, 0, 0, 1, 1, 2, 3], weights=[40, 20, 10, 15, 10, 3, 2])[0]
        
        for _ in range(num_rewards):
            max_days = years_of_service * 365
            if max_days <= 180:
                continue
            reward_date = hire_date + timedelta(days=random.randint(180, max_days))
            if reward_date > datetime.now():
                continue
            
            reward_type, (reason, amount) = random.choice(list(reward_types.items()))
            
            rewards_discipline_data.append({
                'record_id': f'RD{rd_counter:05d}',
                'employee_id': emp['employee_id'],
                'record_type': '포상',
                'category': reward_type,
                'reason': reason,
                'action_date': reward_date.strftime('%Y-%m-%d'),
                'monetary_amount': amount,
                'issued_by': emp['manager_id'],
                'description': f'{reward_type} 수상: {reason}',
                'impact_on_record': 'Positive'
            })
            rd_counter += 1
        
        # 징계: 소수의 직원만 (5%), 근속 1년 이상
        if random.random() < 0.05 and years_of_service >= 1:
            max_days = years_of_service * 365
            if max_days > 180:
                discipline_date = hire_date + timedelta(days=random.randint(180, max_days))
            else:
                continue
            if discipline_date <= datetime.now():
                discipline_type, reason = random.choice(list(discipline_types.items()))
                
                rewards_discipline_data.append({
                    'record_id': f'RD{rd_counter:05d}',
                    'employee_id': emp['employee_id'],
                    'record_type': '징계',
                    'category': discipline_type,
                    'reason': reason,
                    'action_date': discipline_date.strftime('%Y-%m-%d'),
                    'monetary_amount': -500000 if discipline_type == '감봉' else 0,
                    'issued_by': emp['manager_id'],
                    'description': f'{discipline_type} 조치: {reason}',
                    'impact_on_record': 'Negative'
                })
                rd_counter += 1

df_rewards_discipline = pd.DataFrame(rewards_discipline_data)
df_rewards_discipline.to_csv('data/17_rewards_and_discipline.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_rewards_discipline)}건 포상/징계 이력 생성 완료")

# ============================================================================
# 9-6. one_on_one_meetings.csv - 1:1 미팅 기록
print("\n[18/25] one_on_one_meetings.csv 생성 중...")

meeting_data = []
meeting_counter = 1

meeting_topics = [
    '업무 진행 상황 점검',
    '성과 목표 검토 및 조정',
    '커리어 개발 논의',
    '업무 관련 어려움 및 지원 사항',
    '최근 프로젝트 피드백',
    '팀 협업 및 커뮤니케이션',
    '개인 역량 개발 계획',
    '업무 만족도 및 고충 상담',
    '차기 평가 준비',
    '교육 및 개발 기회 논의'
]

for emp in employees:
    if emp['status'] == '재직' and emp['manager_id']:
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
        
        # 2023년부터 월 1회 1:1 미팅
        start_date = max(datetime(2023, 1, 1), hire_date)
        current_date = start_date
        
        while current_date <= datetime.now():
            # 월 1회 (매월 랜덤한 날짜)
            meeting_date = current_date + timedelta(days=random.randint(0, 28))
            
            if meeting_date > datetime.now():
                break
            
            # 미팅 시간 (업무 시간 내)
            meeting_datetime = meeting_date + timedelta(
                hours=random.randint(10, 16),
                minutes=random.choice([0, 30])
            )
            
            # 미팅 시간 (30분 ~ 1시간)
            duration = random.choice([30, 45, 60])
            
            # 주요 논의 사항 (2-3개)
            num_topics = random.randint(2, 3)
            selected_topics = random.sample(meeting_topics, num_topics)
            
            # 액션 아이템
            action_items = [
                f'{random.choice(["교육 신청", "목표 수정", "프로젝트 배정", "역량 개발 계획 수립", "피드백 반영"])}',
                f'{random.choice(["다음 주까지", "이번 달 내", "다음 분기까지"])} {random.choice(["완료", "검토", "실행"])}',
            ]
            
            meeting_data.append({
                'meeting_id': f'MTG{meeting_counter:06d}',
                'employee_id': emp['employee_id'],
                'manager_id': emp['manager_id'],
                'meeting_datetime': meeting_datetime.strftime('%Y-%m-%d %H:%M:%S'),
                'duration_minutes': duration,
                'discussion_topics': ' | '.join(selected_topics),
                'action_items': ' | '.join(random.sample(action_items, random.randint(1, 2))),
                'next_meeting_scheduled': (meeting_datetime + timedelta(days=random.randint(25, 35))).strftime('%Y-%m-%d'),
                'employee_satisfaction_score': round(random.uniform(3.5, 5.0), 1),
                'meeting_status': '완료'
            })
            meeting_counter += 1
            
            # 다음 달로
            current_date = current_date + timedelta(days=30)

df_meetings = pd.DataFrame(meeting_data)
df_meetings.to_csv('data/18_one_on_one_meetings.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_meetings)}건 1:1 미팅 기록 생성 완료")

# ============================================================================
# 10. skill_assessment.csv - 역량 진단
print("\n[19/25] skill_assessment.csv 생성 중...")

skill_assessment_data = []
assess_counter = 1

assessment_date = '2023-11-10'
skill_metrics = ['SKILL_001', 'SKILL_002', 'SKILL_003', 'SKILL_004', 
                 'SKILL_005', 'SKILL_006', 'SKILL_007', 'SKILL_008']

for emp in employees:
    if emp['status'] == '재직':
        for metric_code in skill_metrics:
            # 정규분포 기반 점수 (3.5 평균, 표준편차 0.6)
            self_rating = round(np.clip(np.random.normal(3.7, 0.5), 1.0, 5.0), 1)
            manager_rating = round(np.clip(np.random.normal(3.5, 0.6), 1.0, 5.0), 1)
            peer_rating = round(np.clip(np.random.normal(3.6, 0.5), 1.0, 5.0), 1)
            
            skill_assessment_data.append({
                'assessment_id': f'SA{assess_counter:04d}',
                'employee_id': emp['employee_id'],
                'assessment_date': assessment_date,
                'metric_code': metric_code,
                'self_rating': self_rating,
                'manager_rating': manager_rating,
                'peer_rating_avg': peer_rating
            })
            assess_counter += 1

df_skill_assessment = pd.DataFrame(skill_assessment_data)
df_skill_assessment.to_csv('data/19_skill_assessment.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_skill_assessment)}건 역량 진단 기록 생성 완료")

# ============================================================================
# 11. leadership_360_review.csv - 리더십 360도 평가
print("\n[20/25] leadership_360_review.csv 생성 중...")

leadership_data = []
lead_counter = 1

leadership_metrics = ['LEAD_001', 'LEAD_002', 'LEAD_003', 'LEAD_004', 'LEAD_005', 'LEAD_006', 'LEAD_007']
leaders = [emp for emp in employees if emp['job_title'] in ['팀장', '부장', '본부장', '이사', '대표이사']]

for leader in leaders:
    for review_year in [2022, 2023, 2024]:
        for metric_code in leadership_metrics:
            # 리더십 점수 (정규분포, 3.5 평균)
            boss_score = round(np.clip(np.random.normal(3.7, 0.5), 2.0, 5.0), 1)
            direct_report_score = round(np.clip(np.random.normal(3.5, 0.6), 1.5, 5.0), 1)
            peer_score = round(np.clip(np.random.normal(3.6, 0.5), 2.0, 5.0), 1)
            
            # Boss 평가
            leadership_data.append({
                'review_id': f'L360_{lead_counter:04d}',
                'leader_employee_id': leader['employee_id'],
                'review_year': review_year,
                'rater_relationship': 'Boss',
                'metric_code': metric_code,
                'score': boss_score
            })
            lead_counter += 1
            
            # Direct Report 평가
            leadership_data.append({
                'review_id': f'L360_{lead_counter:04d}',
                'leader_employee_id': leader['employee_id'],
                'review_year': review_year,
                'rater_relationship': 'Direct Report',
                'metric_code': metric_code,
                'score': direct_report_score
            })
            lead_counter += 1
            
            # Peer 평가
            leadership_data.append({
                'review_id': f'L360_{lead_counter:04d}',
                'leader_employee_id': leader['employee_id'],
                'review_year': review_year,
                'rater_relationship': 'Peer',
                'metric_code': metric_code,
                'score': peer_score
            })
            lead_counter += 1

df_leadership = pd.DataFrame(leadership_data)
df_leadership.to_csv('data/20_leadership_360_review.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_leadership)}건 리더십 360도 평가 기록 생성 완료")

print("\n" + "=" * 80)
print("C그룹 프로젝트/평가 데이터 생성 완료")
print("=" * 80)

# ============================================================================
# D그룹: 조직 몰입도 및 보상 데이터
# ============================================================================

# 12. engagement_survey.csv - 조직 몰입도 설문
print("\n[21/25] engagement_survey.csv 생성 중...")

engagement_data = []
survey_counter = 1

survey_years = [2022, 2023, 2024]

for emp in employees:
    if emp['status'] == '재직':
        for year in survey_years:
            hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
            if year < hire_date.year:
                continue
            
            # 정규분포 기반 점수
            job_satisfaction = round(np.clip(np.random.normal(3.6, 0.7), 1.0, 5.0), 1)
            manager_relationship = round(np.clip(np.random.normal(3.7, 0.6), 1.0, 5.0), 1)
            turnover_intention = round(np.clip(np.random.normal(2.5, 0.8), 1.0, 5.0), 1)
            work_life_balance = round(np.clip(np.random.normal(3.4, 0.7), 1.0, 5.0), 1)
            growth_opportunity = round(np.clip(np.random.normal(3.5, 0.7), 1.0, 5.0), 1)
            
            engagement_data.append({
                'survey_id': f'ENG{survey_counter:04d}',
                'employee_id': emp['employee_id'],
                'survey_year': year,
                'q_job_satisfaction': job_satisfaction,
                'q_manager_relationship': manager_relationship,
                'q_turnover_intention': turnover_intention,
                'q_work_life_balance': work_life_balance,
                'q_growth_opportunity': growth_opportunity
            })
            survey_counter += 1

df_engagement = pd.DataFrame(engagement_data)
df_engagement.to_csv('data/21_engagement_survey.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_engagement)}건 조직 몰입도 설문 기록 생성 완료")

# ============================================================================
# 13. compensation_history.csv - 보상 이력
print("\n[22/25] compensation_history.csv 생성 중...")

compensation_data = []
comp_counter = 1

base_salary_ranges = {
    '사원': (35000000, 42000000),
    '주임': (40000000, 48000000),
    '대리': (48000000, 58000000),
    '과장': (58000000, 72000000),
    '차장': (72000000, 90000000),
    '팀장': (90000000, 120000000),
    '부장': (110000000, 140000000),
    '본부장': (130000000, 160000000),
    '이사': (150000000, 190000000),
    '대표이사': (200000000, 280000000)
}

for emp in employees:
    if emp['status'] == '재직':
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
        current_year = 2024
        
        for year in range(hire_date.year, current_year + 1):
            job_title = emp['job_title']
            salary_range = base_salary_ranges.get(job_title, (35000000, 50000000))
            
            # 기본 연봉 (범위 내 랜덤)
            base_salary = random.randint(salary_range[0], salary_range[1])
            
            # 성과 보너스 (0-25%, 정규분포)
            bonus_pct = np.clip(np.random.normal(0.12, 0.06), 0, 0.30)
            annual_bonus = int(base_salary * bonus_pct)
            
            compensation_data.append({
                'compensation_id': f'COMP{comp_counter:04d}',
                'employee_id': emp['employee_id'],
                'effective_date': f'{year}-01-01',
                'base_salary': base_salary,
                'annual_bonus_amount': annual_bonus,
                'total_compensation': base_salary + annual_bonus,
                'currency': 'KRW'
            })
            comp_counter += 1

df_compensation = pd.DataFrame(compensation_data)
df_compensation.to_csv('data/22_compensation_history.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_compensation)}건 보상 이력 생성 완료")

print("\n" + "=" * 80)
print("D그룹 몰입도/보상 데이터 생성 완료")
print("=" * 80)

# ============================================================================
# E그룹: 인재 관리 데이터 (Talent Management)
# ============================================================================

# 20. key_talent_pool.csv - 핵심인재 풀 (성과 기반 선정)
print("\n[23/25] key_talent_pool.csv 생성 중...")

key_talent_data = []
talent_counter = 1

# 핵심인재 선정 로직
for emp in employees:
    if emp['status'] == '재직' and emp['job_title'] not in ['대표이사']:
        # 최근 2년 성과 평가 가져오기
        recent_reviews = [p for p in performance_data 
                         if p['employee_id'] == emp['employee_id'] 
                         and p['review_period'] in ['2023 H1', '2023 H2', '2024 H1']]
        
        if not recent_reviews:
            continue
        
        # 성과 등급을 점수로 변환
        grade_scores = {'S': 5, 'A': 4, 'B': 3, 'C': 2, 'D': 1}
        avg_performance = np.mean([grade_scores[r['final_grade']] for r in recent_reviews])
        
        # 포상 이력 확인
        rewards_count = len([r for r in rewards_discipline_data 
                            if r['employee_id'] == emp['employee_id'] 
                            and r['record_type'] == '포상'])
        
        # 리더십 평가 (리더인 경우)
        leadership_score = None
        if emp['job_title'] in ['팀장', '본부장', '부장']:
            leader_reviews = [l for l in leadership_data 
                            if l['leader_employee_id'] == emp['employee_id'] 
                            and l['review_year'] == 2024
                            and l['rater_relationship'] == 'Direct Report']
            if leader_reviews:
                leadership_score = np.mean([l['score'] for l in leader_reviews])
        
        # 핵심인재 선정 기준
        is_key_talent = False
        talent_tier = None
        selection_reason = []
        
        # Tier 1: 최우수 인재 (성과 S등급 평균 + 포상 이력 or 리더십 우수)
        if avg_performance >= 4.5:  # A+ 이상
            if rewards_count >= 2 or (leadership_score and leadership_score >= 4.3):
                is_key_talent = True
                talent_tier = 'Tier 1 - Critical Talent'
                selection_reason.append('탁월한 성과 지속')
                if rewards_count >= 2:
                    selection_reason.append(f'포상 {rewards_count}회')
                if leadership_score and leadership_score >= 4.3:
                    selection_reason.append('우수한 리더십')
        
        # Tier 2: 우수 인재 (성과 A등급 이상 + 리더 또는 전문가)
        elif avg_performance >= 4.0:  # A 이상
            if emp['job_title'] in ['팀장', '본부장', '부장', '차장', '과장']:
                is_key_talent = True
                talent_tier = 'Tier 2 - High Potential'
                selection_reason.append('안정적 우수 성과')
                if leadership_score and leadership_score >= 4.0:
                    selection_reason.append('리더십 발휘')
                if rewards_count >= 1:
                    selection_reason.append('포상 이력')
        
        # Tier 3: 잠재 인재 (성과 A 이상 + 젊은 직원)
        elif avg_performance >= 3.8:
            hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
            years_of_service = 2024 - hire_date.year
            if years_of_service <= 5 and emp['job_title'] in ['사원', '주임', '대리', '과장']:
                is_key_talent = True
                talent_tier = 'Tier 3 - Emerging Talent'
                selection_reason.append('성장 가능성')
                selection_reason.append('안정적 성과')
        
        if is_key_talent:
            # 유지 리스크 평가 (engagement survey 기반)
            engagement_records = [e for e in engagement_data 
                                 if e['employee_id'] == emp['employee_id'] 
                                 and e['survey_year'] == 2024]
            
            if engagement_records:
                turnover_risk = engagement_records[0]['q_turnover_intention']
                if turnover_risk >= 4.0:
                    retention_risk = 'High'
                elif turnover_risk >= 3.0:
                    retention_risk = 'Medium'
                else:
                    retention_risk = 'Low'
            else:
                retention_risk = 'Medium'
            
            # 개발 우선순위
            if talent_tier == 'Tier 1 - Critical Talent':
                development_priority = '최우선'
            elif talent_tier == 'Tier 2 - High Potential':
                development_priority = '우선'
            else:
                development_priority = '일반'
            
            key_talent_data.append({
                'talent_id': f'TALENT{talent_counter:04d}',
                'employee_id': emp['employee_id'],
                'identification_date': '2024-06-30',
                'talent_tier': talent_tier,
                'avg_performance_score': round(avg_performance, 2),
                'leadership_score': round(leadership_score, 2) if leadership_score else None,
                'rewards_count': rewards_count,
                'selection_reason': ' | '.join(selection_reason),
                'retention_risk': retention_risk,
                'development_priority': development_priority,
                'succession_ready': 'Yes' if talent_tier in ['Tier 1 - Critical Talent', 'Tier 2 - High Potential'] else 'Developing',
                'review_date': '2024-12-31'
            })
            talent_counter += 1

df_key_talent = pd.DataFrame(key_talent_data)
df_key_talent.to_csv('data/23_key_talent_pool.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_key_talent)}명 핵심인재 선정 완료 (성과 평가 기반)")

# ============================================================================
# 21. succession_plan.csv - 승계 계획 (핵심 직책별 후보자)
print("\n[24/25] succession_plan.csv 생성 중...")

succession_data = []
succession_counter = 1

# 승계 대상 핵심 직책 (본부장 + 팀장)
critical_positions = [emp for emp in employees 
                     if emp['job_title'] in ['본부장', '팀장'] 
                     and emp['status'] == '재직']

# 핵심인재 풀 (승계 후보자가 될 수 있는 사람들)
key_talent_ids = [kt['employee_id'] for kt in key_talent_data 
                  if kt['succession_ready'] == 'Yes']

for position in critical_positions:
    # 같은 본부 또는 같은 팀의 핵심인재 중에서 후보 선정
    if position['job_title'] == '본부장':
        # 본부장 후보: 같은 본부의 팀장들 중 핵심인재
        candidates = [emp for emp in employees 
                     if emp['division_name'] == position['division_name']
                     and emp['employee_id'] in key_talent_ids
                     and emp['job_title'] in ['팀장', '차장', '부장']
                     and emp['employee_id'] != position['employee_id']]
    else:  # 팀장
        # 팀장 후보: 같은 팀의 차장/과장 중 핵심인재
        candidates = [emp for emp in employees 
                     if emp['org_id'] == position['org_id']
                     and emp['employee_id'] in key_talent_ids
                     and emp['job_title'] in ['차장', '과장', '대리']
                     and emp['employee_id'] != position['employee_id']]
    
    # 후보자가 없으면 다른 팀에서도 찾기
    if len(candidates) < 2:
        candidates.extend([emp for emp in employees 
                         if emp['division_name'] == position['division_name']
                         and emp['employee_id'] in key_talent_ids
                         and emp['job_title'] not in ['대표이사']
                         and emp['employee_id'] != position['employee_id']
                         and emp not in candidates][:3])
    
    # 후보자 1-3명 선정
    num_successors = min(len(candidates), random.randint(1, 3))
    selected_successors = random.sample(candidates, num_successors) if candidates else []
    
    for idx, successor in enumerate(selected_successors):
        # 준비도 평가
        successor_talent_info = next((kt for kt in key_talent_data 
                                     if kt['employee_id'] == successor['employee_id']), None)
        
        if successor_talent_info:
            perf_score = successor_talent_info['avg_performance_score']
            
            if perf_score >= 4.5:
                readiness = 'Ready Now'
                development_needed = '리더십 고도화, 전략적 사고'
            elif perf_score >= 4.0:
                readiness = '1-2 Years'
                development_needed = '관리 역량 강화, 의사결정 경험'
            else:
                readiness = '3+ Years'
                development_needed = '리더십 기본, 팀 관리 경험'
        else:
            readiness = '3+ Years'
            development_needed = '역량 전반 개발 필요'
        
        # 현 직책자의 퇴사 리스크
        position_talent_info = next((kt for kt in key_talent_data 
                                    if kt['employee_id'] == position['employee_id']), None)
        
        if position_talent_info:
            position_risk = position_talent_info['retention_risk']
        else:
            # 핵심인재가 아닌 리더는 리스크 높을 수 있음
            position_risk = random.choice(['Medium', 'High'])
        
        succession_data.append({
            'succession_plan_id': f'SUC{succession_counter:04d}',
            'critical_position': position['job_title'],
            'current_holder_id': position['employee_id'],
            'current_holder_name': position['name'],
            'org_name': position['org_name'],
            'division_name': position['division_name'],
            'successor_rank': idx + 1,  # 1st, 2nd, 3rd choice
            'successor_id': successor['employee_id'],
            'successor_name': successor['name'],
            'successor_current_title': successor['job_title'],
            'readiness_level': readiness,
            'development_needed': development_needed,
            'is_key_talent': 'Yes',
            'position_risk_level': position_risk,
            'plan_date': '2024-07-01',
            'next_review_date': '2025-01-01'
        })
        succession_counter += 1

df_succession = pd.DataFrame(succession_data)
df_succession.to_csv('data/24_succession_plan.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_succession)}건 승계 계획 생성 완료 (핵심인재 기반)")

print("\n" + "=" * 80)
print("E그룹 인재 관리 데이터 생성 완료")
print("=" * 80)

# ============================================================================
# 최종 파일: 연간 스냅샷
# ============================================================================

# 22. employee_yearly_snapshot.csv - 연간 요약
print("\n[25/25] employee_yearly_snapshot.csv 생성 중...")

snapshot_data = []
snapshot_counter = 1

for emp in employees:
    if emp['status'] == '재직':
        hire_date = datetime.strptime(emp['hire_date'], '%Y-%m-%d')
        
        for year in range(2022, 2025):
            if year < hire_date.year:
                continue
            
            # 해당 연도의 성과 등급
            perf_records = [p for p in performance_data 
                          if p['employee_id'] == emp['employee_id'] 
                          and str(year) in p['review_period']]
            perf_grade = perf_records[-1]['final_grade'] if perf_records else 'B'
            
            # 해당 연도의 보상
            comp_record = [c for c in compensation_data 
                          if c['employee_id'] == emp['employee_id'] 
                          and str(year) in c['effective_date']]
            total_comp = comp_record[0]['total_compensation'] if comp_record else 40000000
            
            # 역량 점수 평균
            skill_records = [s for s in skill_assessment_data 
                           if s['employee_id'] == emp['employee_id']]
            avg_skill = round(np.mean([s['peer_rating_avg'] for s in skill_records]), 2) if skill_records else 3.5
            
            # 프로젝트 수
            project_count = len([p for p in project_data 
                               if p['employee_id'] == emp['employee_id'] 
                               and str(year) in p['start_date']])
            
            snapshot_data.append({
                'snapshot_id': f'SNAP{snapshot_counter:04d}',
                'employee_id': emp['employee_id'],
                'snapshot_date': f'{year}-12-31',
                'division_name': emp['division_name'],
                'org_name': emp['org_name'],
                'job_title': emp['job_title'],
                'performance_grade': perf_grade,
                'total_compensation': total_comp,
                'key_skill_score_avg': avg_skill,
                'project_count': project_count,
                'employment_status': emp['status']
            })
            snapshot_counter += 1

df_snapshot = pd.DataFrame(snapshot_data)
df_snapshot.to_csv('data/25_employee_yearly_snapshot.csv', index=False, encoding='utf-8-sig')
print(f"   [OK] {len(df_snapshot)}건 연간 스냅샷 생성 완료")

print("\n" + "=" * 80)
print("전체 데이터 생성 완료!")
print("=" * 80)
print(f"\n=== 생성 요약 ===")
print(f"총 직원 수: {len(df_employees)}명")
print(f"재직자: {len([e for e in employees if e['status'] == '재직'])}명")
print(f"퇴사자: {len([e for e in employees if e['status'] == '퇴사'])}명")
print(f"\n생성된 파일:")
print("  [조직 구조]")
print("  00_organization_structure.csv (부서 간 위계)")
print("  00_reporting_lines.csv (전체 보고 라인)")
print("\n  [마스터 데이터]")
print("  01_hr_metrics_definition.csv (통합 지표 사전)")
print("  02_employee_info.csv (3단계 위계: 대표 → 본부장 → 팀장 → 팀원)")
print("  03_job_history.csv")
print("  04_personal_traits.csv")
print("\n  [채용/교육]")
print("  05_recruitment_history.csv")
print("  06_recruitment_aptitude_results.csv (적성검사)")
print("  07_recruitment_cpi_results.csv (CPI 성격검사)")
print("  08_recruitment_mmpi_results.csv (MMPI 진단검사)")
print("  09_onboarding_program.csv")
print("  10_training_history.csv")
print("\n  [프로젝트/성과]")
print("  11_project_history.csv")
print("  12_performance_review.csv")
print("  13_continuous_performance_review.csv")
print("  14_goal_management.csv")
print("\n  [조직 문화/퇴사]")
print("  15_exit_interview.csv")
print("  16_team_culture_survey.csv")
print("  17_rewards_and_discipline.csv")
print("  18_one_on_one_meetings.csv")
print("\n  [평가/보상]")
print("  19_skill_assessment.csv")
print("  20_leadership_360_review.csv")
print("  21_engagement_survey.csv")
print("  22_compensation_history.csv")
print("\n  [인재 관리]")
print("  23_key_talent_pool.csv (성과 기반 핵심인재 선정)")
print("  24_succession_plan.csv (승계 계획 - 핵심인재 연결)")
print("\n  [요약]")
print("  25_employee_yearly_snapshot.csv")

# 핵심인재 통계
print(f"\n=== 핵심인재 통계 ===")
tier1_count = len([t for t in key_talent_data if 'Tier 1' in t['talent_tier']])
tier2_count = len([t for t in key_talent_data if 'Tier 2' in t['talent_tier']])
tier3_count = len([t for t in key_talent_data if 'Tier 3' in t['talent_tier']])
print(f"Tier 1 (Critical Talent): {tier1_count}명")
print(f"Tier 2 (High Potential): {tier2_count}명")
print(f"Tier 3 (Emerging Talent): {tier3_count}명")
print(f"총 핵심인재: {len(key_talent_data)}명 ({len(key_talent_data)/len([e for e in employees if e['status']=='재직'])*100:.1f}%)")
print(f"\n승계 계획 수립 직책: {len(critical_positions)}개")
print(f"승계 후보자 매핑: {len(df_succession)}건")
print(f"\n모든 파일이 'data' 폴더에 UTF-8 인코딩으로 저장되었습니다.")
print("=" * 80)
