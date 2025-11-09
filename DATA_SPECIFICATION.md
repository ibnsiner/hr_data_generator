# GDB-HR 프로젝트 데이터 명세서

**버전**: 2.4  
**생성일**: 2024년  
**총 파일 수**: 25개  
**총 직원 수**: 210명 (재직자 약 195명, 퇴사자 15명)  
**조직 구조**: 3단계 위계 (대표 → 본부장 → 팀장 → 팀원)  
**데이터 기간**: 2015년 ~ 2024년  
**주요 특징**: 채용 전형 검사 + 통합 메타데이터 + 승진 이력 + **데이터 간 상관관계**  

---

## 📋 목차

1. [데이터 개요](#데이터-개요)
2. [파일 목록](#파일-목록)
3. [상세 스키마](#상세-스키마)
4. [데이터 관계도](#데이터-관계도)
5. [주요 사용 시나리오](#주요-사용-시나리오)

---

## 데이터 개요

이 데이터셋은 약 200명 규모의 가상 IT 기업 "넥스트젠 테크놀로지스"의 HR 데이터입니다. 
실제 기업 환경을 반영하여 생성되었으며, 다음과 같은 특징이 있습니다:

- **통계적 타당성**: 정규분포 기반 점수 생성
- **시간적 일관성**: 타임스탬프 및 이벤트 순서 보장
- **관계적 무결성**: 직원 ID, 관리자 ID 등 외래키 관계 유지
- **실무 반영**: 실제 HR 프로세스 기반 데이터 구조
- **조직 위계**: 3본부 10팀 구조로 명확한 보고 라인 구현

---

## 파일 목록

| 번호 | 파일명 | 설명 | 레코드 수 |
|------|--------|------|----------|
| **조직 구조** |
| 00 | `organization_structure.csv` | 조직/부서 간 위계 구조 | 14 |
| 01 | `reporting_lines.csv` | 전체 보고 라인 매핑 | 209 |
| **마스터 데이터** |
| 02 | `hr_metrics_definition.csv` | **통합 지표 사전** (80개 지표) | 80 |
| 03 | `employee_info.csv` | 직원 기본 정보 (3단계 위계) | 210 |
| 04 | `job_history.csv` | 직원 경력 경로 (승진 이력) | 527 |
| 05 | `personal_traits.csv` | Big-5 성격 검사 | 195 |
| **채용/교육** |
| 06 | `recruitment_history.csv` | 채용 이력 | 206 |
| 07 | `recruitment_aptitude_results.csv` | **적성검사 결과** | 210 |
| 08 | `recruitment_cpi_results.csv` | **CPI 성격검사 결과** | 210 |
| 09 | `recruitment_mmpi_results.csv` | **MMPI 진단검사 결과** | 210 |
| 10 | `onboarding_program.csv` | 온보딩 프로그램 | 378 |
| 11 | `training_history.csv` | 교육 이력 | 799 |
| **프로젝트/성과** |
| 12 | `project_history.csv` | 프로젝트 이력 | 372 |
| 13 | `performance_review.csv` | 반기별 성과 평가 | 857 |
| 14 | `continuous_performance_review.csv` | 수시 성과 평가 | 1,937 |
| 15 | `goal_management.csv` | 목표 관리 (OKR/MBO) | 6,099 |
| **조직 문화/퇴사** |
| 16 | `exit_interview.csv` | 퇴사자 인터뷰 | 15 |
| 17 | `team_culture_survey.csv` | 팀별 조직문화 서베이 | 376 |
| 18 | `rewards_and_discipline.csv` | 포상/징계 이력 | 68 |
| 19 | `one_on_one_meetings.csv` | 1:1 미팅 기록 | 6,414 |
| **평가/보상** |
| 20 | `skill_assessment.csv` | 역량 진단 | 1,560 |
| 21 | `leadership_360_review.csv` | 리더십 360도 평가 | 1,449 |
| 22 | `engagement_survey.csv` | 조직 몰입도 설문 | 537 |
| 23 | `compensation_history.csv` | 보상 이력 | 1,141 |
| **인재 관리** |
| 24 | `key_talent_pool.csv` | 핵심인재 풀 (성과 기반) | 4 |
| 25 | `succession_plan.csv` | 승계 계획 | 17 |
| **요약** |
| 26 | `employee_yearly_snapshot.csv` | 연간 요약 | 537 |

**총 레코드 수**: 약 **21,300+**  
**핵심 신규 기능**: 채용 전형 검사 (CPI, MMPI, 적성검사) + 통합 메타데이터 (80개 지표) + 현실적 승진 이력

---

## 상세 스키마

**핵심 특징**:
- ✅ **채용 전형 검사**: CPI, MMPI, 적성검사로 현실적 채용 프로세스 구현
- ✅ **통합 메타데이터**: 80개 지표의 완전한 정의 (높을때/낮을때 특성 포함)
- ✅ **현실적 승진 이력**: 팀장들도 하위 직급에서 점진적 승진 (평균 2.1회)
- ✅ **데이터 간 상관관계**: 검사 결과 간 현실적 상관관계 구현 (r=0.33~0.64)
  - 적성 대인관계 ↔ CPI 사교성/공감성 (r=0.33~0.39)
  - CPI 안녕감 ↔ MMPI 우울증 역상관 (r=-0.63)
  - 리더급 상황판단 ↔ CPI 지배성 (r=0.51)
- ✅ **퇴사자 특성 반영**: MMPI 우울 73.9 vs 재직자 48.8
- ✅ **직무별 차별화**: 본부별 요구 역량에 따른 적성검사 점수 차별화
- ✅ **조직 위계 구조**: 3본부 10팀 명확한 보고 라인
- ✅ **데이터 논리적 연결**: 성과 → 핵심인재 → 승계 후보
- ✅ **정성 의견 풍부화**: 조합형 문장으로 수백 가지 변형
- ✅ **CONFIG 설정**: 16개 설정값으로 쉬운 커스터마이징

### 00-1. organization_structure.csv
**목적**: 조직/부서 간 위계 구조 정의

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|-------------|------|------|
| `org_id` | STRING | 조직 고유 ID (PK) | ORG000, ORG100, ORG201 |
| `org_name` | STRING | 조직명 | 넥스트젠 테크놀로지스, 기술본부, AI솔루션개발팀 |
| `org_type` | STRING | 조직 유형 | Company, Division, Team |
| `parent_org_id` | STRING | 상위 조직 ID (FK) | ORG000, ORG200 |
| `level` | INTEGER | 조직 레벨 | 0=회사, 1=본부, 2=팀 |
| `head_employee_id` | STRING | 조직장 직원 ID (FK) | EMP000, DIV001, TL001 |

**조직 구조**:
```
넥스트젠 테크놀로지스 (ORG000) - Level 0
├── 경영지원본부 (ORG100) - Level 1
│   ├── HR팀 (ORG101) - Level 2
│   └── 재무팀 (ORG102) - Level 2
├── 기술본부 (ORG200) - Level 1
│   ├── AI솔루션개발팀 (ORG201) - Level 2
│   ├── 플랫폼개발팀 (ORG202) - Level 2
│   ├── 데이터분석팀 (ORG203) - Level 2
│   ├── IT기획팀 (ORG204) - Level 2
│   ├── UI/UX디자인팀 (ORG205) - Level 2
│   └── QA팀 (ORG206) - Level 2
└── 비즈니스본부 (ORG300) - Level 1
    ├── 마케팅팀 (ORG301) - Level 2
    └── 영업팀 (ORG302) - Level 2
```

**관계**: `employee_info`의 `org_id`와 연결

---

### 00-2. reporting_lines.csv
**목적**: 전체 직원의 보고 라인 (보고 체계) 매핑

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|-------------|------|------|
| `reporting_line_id` | STRING | 보고 라인 ID (PK) | RL0001 |
| `employee_id` | STRING | 직원 ID (FK) | EMP001 |
| `employee_name` | STRING | 직원명 | 김철수 |
| `job_title` | STRING | 직급 | 사원, 대리, 팀장 |
| `immediate_manager_id` | STRING | 직속 상사 ID (FK) | TL001 |
| `immediate_manager_title` | STRING | 직속 상사 직급 | 팀장 |
| `second_level_manager_id` | STRING | 2차 상사 ID (FK) | DIV002 (본부장) |
| `third_level_manager_id` | STRING | 3차 상사 ID (FK) | EMP000 (대표) |
| `reporting_depth` | INTEGER | 보고 라인 깊이 | 1, 2, 3 |
| `division_name` | STRING | 소속 본부 | 기술본부 |
| `org_name` | STRING | 소속 팀 | AI솔루션개발팀 |

**보고 라인 예시**:
- **일반 팀원** (Depth 3): 팀원 → 팀장 → 본부장 → 대표이사
- **팀장** (Depth 2): 팀장 → 본부장 → 대표이사
- **본부장** (Depth 1): 본부장 → 대표이사

**활용**:
- 조직 내 의사결정 경로 파악
- 리더십 영향 범위 분석
- 조직 구조 시각화

---

### 02. hr_metrics_definition.csv ⭐ **통합 메타데이터**
**목적**: 모든 평가 도구의 지표를 통합한 완전한 메타데이터 사전

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|-------------|------|------|
| `metric_code` | STRING | 지표 고유 코드 (PK) | SKILL_001, CPI_Do, MMPI_D, BIG5_OPENNESS |
| `metric_name` | STRING | 지표 명칭 | 데이터 분석, 지배성, 우울증, 개방성 |
| `tool_name` | STRING | 평가 도구명 | Competency Framework, CPI, MMPI, Big-5 성격검사 |
| `dimension` | STRING | 평가 차원 | Technical Skill, 대인관계및자신감, 임상척도, Personality |
| `definition` | STRING | **상세 지표 정의** | 대량의 데이터를 수집, 정제, 분석하여... |
| `measurement_scale` | STRING | 측정 척도 | 1-5점 척도, T점수 (20-80), 0-100점 척도 |
| `high_score_characteristics` | STRING | **높은 점수 특성** | 복잡한 데이터에서 핵심 인사이트 도출, 예측 모델 구축... |
| `low_score_characteristics` | STRING | **낮은 점수 특성** | 기초적 데이터 처리만 가능, 분석 결과 해석 어려움... |

**포함 도구 (총 80개 지표)**:
- **Competency Framework**: 10개 (기술/소프트스킬)
- **Leadership 360**: 7개 (리더십 역량)
- **Performance Review**: 3개 (성과 지표)
- **Engagement Survey**: 3개 (몰입도 지표)
- **Big-5 성격검사**: 5개 (개방성, 성실성, 외향성, 친화성, 신경증)
- **CPI**: 27개 (20개 일상척도 + 3개 벡터척도 + 4개 라이프스타일)
- **MMPI**: 13개 (3개 타당도척도 + 10개 임상척도)
- **적성검사**: 12개 (언어/수리/상황판단/사회상식/대인관계)

**AI 챗봇 활용 예시**:
```
사용자: "김철수의 CPI 지배성 점수가 높은데 이게 뭘 의미해?"
AI: "CPI 지배성(Do)은 리더십과 주도성을 측정하는 척도입니다. 
높은 점수는 강한 리더십, 주도적 행동, 자신감 넘침, 결단력 등을 의미하며
관리직이나 프로젝트 리더 역할에 적합한 특성입니다."
```

**관계**: 모든 평가 테이블에서 `metric_code`로 참조

---

### 03. employee_info.csv
**목적**: 직원 기본 정보 (마스터 테이블, 3단계 위계 구조)

| 컬럼명 | 데이터 타입 | 설명 | 예시 | 비고 |
|--------|-------------|------|------|------|
| `employee_id` | STRING | 직원 고유 ID (PK) | EMP001, TL001, DIV001 | TL=팀장, DIV=본부장 |
| `name` | STRING | 이름 | 김철수 | Faker 생성 |
| `gender` | STRING | 성별 | 남, 여 | |
| `birth_date` | DATE | 생년월일 | 1990-05-15 | YYYY-MM-DD |
| `employment_type` | STRING | 고용 형태 | 정규직, 계약직 | |
| `hire_date` | DATE | 입사일 | 2020-03-01 | |
| `org_id` | STRING | 조직 ID (FK) | ORG201 | organization_structure 참조 |
| `org_name` | STRING | 팀명 | AI솔루션개발팀 | |
| `division_name` | STRING | 본부명 | 기술본부 | |
| `job_title` | STRING | 직급 | 사원, 주임, 대리, 과장, 차장, 팀장, 부장, 본부장, 이사 | |
| `manager_id` | STRING | 직속 상사 ID (FK) | TL001 | employee_id 참조 |
| `status` | STRING | 재직 상태 | 재직, 퇴사 | |

**관계**: 거의 모든 테이블에서 `employee_id`로 참조됨

**조직 구조**:
- **경영지원본부**: HR팀, 재무팀
- **기술본부**: AI솔루션개발팀, 플랫폼개발팀, 데이터분석팀, IT기획팀, UI/UX디자인팀, QA팀
- **비즈니스본부**: 마케팅팀, 영업팀

**직급 체계**:
```
사원(1) → 주임(2) → 대리(3) → 과장(4) → 차장(5) 
→ 팀장(6) → 부장(7) → 본부장(8) → 이사(9) → 대표이사
```

**인원 구성**:
- 대표이사: 1명 (EMP000)
- 본부장: 3명 (DIV001, DIV002, DIV003)
- 팀장: 10명 (TL001~TL010)
- 일반 직원: ~186명

---

### 04. job_history.csv
**목적**: 직원의 모든 경력 경로 추적 (승진, 부서 이동)

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|-------------|------|------|
| `history_id` | STRING | 이력 고유 ID (PK) | HIST0001 |
| `employee_id` | STRING | 직원 ID (FK) | EMP001 |
| `start_date` | DATE | 시작일 | 2020-03-01 |
| `end_date` | DATE | 종료일 | 2022-01-31 (NULL=현재) |
| `org_id` | STRING | 조직 ID | ORG201 |
| `job_title` | STRING | 직급 | 사원, 대리, 과장 등 |
| `change_type` | STRING | 변경 유형 | 신규입사, 승진, 부서이동 |

**비즈니스 규칙**:
- 한 직원은 여러 이력 레코드를 가질 수 있음
- 현재 직급/부서는 `end_date`가 NULL인 레코드

---

### 05. personal_traits.csv
**목적**: Big-5 성격 검사 결과

| 컬럼명 | 데이터 타입 | 설명 | 범위 |
|--------|-------------|------|------|
| `trait_id` | STRING | 특성 ID (PK) | TRAIT001 |
| `employee_id` | STRING | 직원 ID (FK) | EMP001 |
| `assessment_date` | DATE | 검사일 | 2020-04-15 |
| `tool_name` | STRING | 검사 도구명 | Big-5 성격검사 |
| `openness` | INTEGER | 개방성 점수 | 0-100 |
| `conscientiousness` | INTEGER | 성실성 점수 | 0-100 |
| `extraversion` | INTEGER | 외향성 점수 | 0-100 |
| `agreeableness` | INTEGER | 친화성 점수 | 0-100 |
| `neuroticism` | INTEGER | 신경증 점수 | 0-100 |
| `primary_strength` | STRING | 주요 강점 | 높은 성실성, 매우 높은 친화성 |
| `motivation_driver` | STRING | 동기 부여 요인 | 성취, 안정, 관계, 성장, 인정 등 |

**해석**:
- 점수가 높을수록 해당 특성이 강함 (neuroticism 제외)
- 정규분포 기반: 평균 65, 표준편차 15

---

### 06. recruitment_history.csv
**목적**: 채용 프로세스 이력

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `recruitment_id` | STRING | 채용 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `position_title` | STRING | 채용 직급 |
| `apply_date` | DATE | 지원일 |
| `interview_date` | DATE | 면접일 |
| `offer_date` | DATE | 합격 통보일 |
| `hire_date` | DATE | 입사일 |
| `recruitment_channel` | STRING | 채용 경로 (채용공고, 헤드헌팅, 추천 등) |
| `interviewer_comment` | STRING | 면접관 코멘트 |

**프로세스 플로우**: 지원 → 적성검사 → CPI검사 → MMPI검사 → 면접 → 합격 통보 → 입사

---

### 07. recruitment_aptitude_results.csv
**목적**: 채용 전형 검사의 모든 지표 메타데이터

| 컬럼명 | 데이터 타입 | 설명 | 예시 |
|--------|-------------|------|------|
| `test_type` | STRING | 검사 유형 | CPI, MMPI, APTITUDE |
| `category_level1` | STRING | 상위 분류 | 대인관계및자신감, 타당도척도, 언어적능력 |
| `category_level2` | STRING | 하위 분류 | NULL (필요시 사용) |
| `factor_code` | STRING | 요인 코드 (PK) | Do, L, verbal_total |
| `factor_name_kr` | STRING | 한글 명칭 | 지배성, 허위척도, 언어적능력 |
| `factor_name_en` | STRING | 영문 명칭 | Dominance, Lie Scale, Verbal Ability |
| `definition` | STRING | 상세 정의 | 리더십, 주도성, 자신감을 측정합니다 |
| `score_range_min` | INTEGER | 최소 점수 | 20 (T점수), 0 (적성검사) |
| `score_range_max` | INTEGER | 최대 점수 | 80 (T점수), 100 (적성검사) |
| `interpretation_low` | STRING | 낮은 점수 해석 | 평균 이하, 정상 범위 |
| `interpretation_high` | STRING | 높은 점수 해석 | 평균 이상, 임상적 주의 |

**포함 검사**:
- **CPI**: 20개 일상척도 + 3개 벡터척도 + 4개 라이프스타일 유형
- **MMPI**: 3개 타당도척도 + 10개 임상척도
- **적성검사**: 5개 상위요인 + 8개 하위요인

---

### 05-2. recruitment_aptitude_results.csv
**목적**: 채용 시 실시한 적성검사 결과

| 컬럼명 | 데이터 타입 | 설명 | 범위 |
|--------|-------------|------|------|
| `test_id` | STRING | 검사 ID (PK) | APT0001 |
| `employee_id` | STRING | 직원 ID (FK) | EMP001 |
| `test_date` | DATE | 검사일 | 2020-02-12 |
| `recruitment_id` | STRING | 채용 ID (FK) | REC0001 |
| **언어적 능력** |
| `verbal_total` | FLOAT | 언어적 능력 총점 | 0-100 |
| `verbal_vocab` | INTEGER | 어휘능력 | 0-100 |
| `verbal_composition` | INTEGER | 문장구성력 | 0-100 |
| `verbal_decoding` | INTEGER | 문장해독력 | 0-100 |
| `verbal_english` | INTEGER | 영어능력 | 0-100 |
| **수리적 능력** |
| `numerical_total` | FLOAT | 수리적 능력 총점 | 0-100 |
| `numerical_quantity` | INTEGER | 수량적처리능력 | 0-100 |
| `numerical_statistics` | INTEGER | 통계적처리능력 | 0-100 |
| `numerical_logic` | INTEGER | 논리적사고능력 | 0-100 |
| **기타 능력** |
| `situational_judgment` | INTEGER | 상황판단능력 | 0-100 |
| `social_knowledge` | INTEGER | 사회적상식 | 0-100 |
| `interpersonal_skills` | INTEGER | 대인관계능력 | 0-100 |
| **종합 평가** |
| `overall_aptitude_score` | FLOAT | 전체 적성 점수 | 0-100 |
| `aptitude_grade` | STRING | 적성 등급 | S, A, B, C, D |
| `pass_fail_status` | STRING | 합격 여부 | PASS, FAIL |

**특징**:
- **직무별 차별화**: 기술본부(수리↑), 경영지원본부(언어↑), 비즈니스본부(상황판단↑)
- **퇴사자 특성**: 전반적으로 낮은 점수 (채용 미스매치 반영)
- **등급 기준**: S(85+), A(75-84), B(65-74), C(55-64), D(55미만)

---

### 05-3. recruitment_cpi_results.csv
**목적**: 채용 시 실시한 CPI 성격검사 결과

| 컬럼명 | 데이터 타입 | 설명 | 범위 |
|--------|-------------|------|------|
| `test_id` | STRING | 검사 ID (PK) | CPI0001 |
| `employee_id` | STRING | 직원 ID (FK) | EMP001 |
| `test_date` | DATE | 검사일 | 2020-02-15 |
| `recruitment_id` | STRING | 채용 ID (FK) | REC0001 |
| **1군: 대인관계 및 자신감** |
| `dominance_do` | INTEGER | 지배성 | 20-80 (T점수) |
| `capacity_status_cs` | INTEGER | 지위추구성 | 20-80 |
| `sociability_sy` | INTEGER | 사교성 | 20-80 |
| `social_presence_sp` | INTEGER | 사회적존재감 | 20-80 |
| `self_acceptance_sa` | INTEGER | 자기수용 | 20-80 |
| `independence_in` | INTEGER | 독립성 | 20-80 |
| `empathy_em` | INTEGER | 공감성 | 20-80 |
| **2군: 규범 지향성 및 가치관** |
| `responsibility_re` | INTEGER | 책임감 | 20-80 |
| `socialization_so` | INTEGER | 사회화 | 20-80 |
| `self_control_sc` | INTEGER | 자기통제 | 20-80 |
| `good_impression_gi` | INTEGER | 호감성 | 20-80 |
| `communality_cm` | INTEGER | 공동체성 | 20-80 |
| `well_being_wb` | INTEGER | 안녕감 | 20-80 |
| `tolerance_to` | INTEGER | 관용성 | 20-80 |
| **3군: 성취 잠재력 및 지적 효율성** |
| `achievement_conformance_ac` | INTEGER | 순응을통한성취 | 20-80 |
| `achievement_independence_ai` | INTEGER | 독립을통한성취 | 20-80 |
| `intellectual_efficiency_ie` | INTEGER | 지적효율성 | 20-80 |
| **4군: 역할 및 개인적 스타일** |
| `psychological_mindedness_py` | INTEGER | 심리지향성 | 20-80 |
| `flexibility_fx` | INTEGER | 융통성 | 20-80 |
| `femininity_masculinity_fm` | INTEGER | 여성성남성성 | 20-80 |
| **벡터척도** |
| `vector_v1_extraversion` | INTEGER | 외향성-내향성 | 20-80 |
| `vector_v2_norm_orientation` | INTEGER | 규범지향-규범회의 | 20-80 |
| `vector_v3_self_realization` | INTEGER | 자아실현 | 20-80 |
| `lifestyle_type` | STRING | 라이프스타일 유형 | Alpha, Beta, Gamma, Delta |
| `overall_cpi_score` | FLOAT | 전체 CPI 점수 | 20-80 |

**라이프스타일 유형**:
- **Alpha**: 외향적 + 규범지향 (리더십 강한 실행형)
- **Beta**: 내향적 + 규범지향 (성실한 협력형)
- **Gamma**: 외향적 + 규범회의 (혁신적 창조형)
- **Delta**: 내향적 + 규범회의 (사색적 독립형)

**특징**:
- **직급별 차별화**: 리더급(지배성↑, 지위추구성↑), 일반직원(평균 수준)
- **퇴사자 특성**: 안녕감↓, 책임감↓ (조직 부적응 반영)

---

### 05-4. recruitment_mmpi_results.csv
**목적**: 채용 시 실시한 MMPI 진단검사 결과

| 컬럼명 | 데이터 타입 | 설명 | 범위 |
|--------|-------------|------|------|
| `test_id` | STRING | 검사 ID (PK) | MMPI0001 |
| `employee_id` | STRING | 직원 ID (FK) | EMP001 |
| `test_date` | DATE | 검사일 | 2020-02-18 |
| `recruitment_id` | STRING | 채용 ID (FK) | REC0001 |
| **타당도 척도** |
| `lie_scale_l` | INTEGER | L척도 (허위척도) | 20-80 (T점수) |
| `frequency_scale_f` | INTEGER | F척도 (빈도척도) | 20-80 |
| `correction_scale_k` | INTEGER | K척도 (교정척도) | 20-80 |
| `validity_status` | STRING | 타당도 상태 | VALID, INVALID |
| **임상 척도** |
| `hypochondriasis_hs` | INTEGER | 척도1 (건강염려증) | 20-80 |
| `depression_d` | INTEGER | 척도2 (우울증) | 20-80 |
| `hysteria_hy` | INTEGER | 척도3 (히스테리) | 20-80 |
| `psychopathic_deviate_pd` | INTEGER | 척도4 (반사회성) | 20-80 |
| `masculinity_femininity_mf` | INTEGER | 척도5 (남성성-여성성) | 20-80 |
| `paranoia_pa` | INTEGER | 척도6 (편집증) | 20-80 |
| `psychasthenia_pt` | INTEGER | 척도7 (강박증) | 20-80 |
| `schizophrenia_sc` | INTEGER | 척도8 (정신분열병) | 20-80 |
| `hypomania_ma` | INTEGER | 척도9 (경조증) | 20-80 |
| `social_introversion_si` | INTEGER | 척도0 (사회적내향성) | 20-80 |
| **종합 평가** |
| `clinical_elevation_count` | INTEGER | 임상척도 상승 개수 | 0-10 (70T 이상) |
| `risk_level` | STRING | 위험 수준 | LOW, MEDIUM, HIGH |
| `overall_adjustment` | STRING | 전반적 적응도 | GOOD, FAIR, POOR |

**해석 기준**:
- **정상 범위**: T점수 30-70
- **임상적 주의**: T점수 70 이상
- **위험 수준**: 상승 척도 3개 이상 또는 우울/정신분열 75 이상 시 HIGH

**특징**:
- **퇴사자 특성**: 우울척도↑, 불안관련척도↑ (퇴사 원인 반영)
- **타당도 관리**: 5% 무효 프로파일 포함 (F척도 상승)

---

### 06. onboarding_program.csv
**목적**: 온보딩 프로그램 이수 현황

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `onboarding_id` | STRING | 온보딩 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `program_name` | STRING | 프로그램명 |
| `scheduled_date` | DATE | 예정일 |
| `completion_status` | STRING | 완료 여부 (완료, 미완료) |
| `satisfaction_score` | FLOAT | 만족도 점수 (1-5) |

**온보딩 프로그램 목록**:
1. 회사 소개 및 비전 공유
2. 조직문화 및 핵심가치 교육
3. 업무 시스템 사용법 교육
4. 부서별 업무 소개
5. 멘토 배정 및 OJT
6. 컴플라이언스 교육
7. 정보보안 교육

---

### 07. training_history.csv
**목적**: 교육 이수 이력

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `training_id` | STRING | 교육 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `training_name` | STRING | 교육명 |
| `category` | STRING | 카테고리 (Technical, Soft Skill, Leadership, Management, Compliance) |
| `training_hours` | INTEGER | 교육 시간 |
| `start_date` | DATE | 시작일 |
| `completion_date` | DATE | 종료일 |
| `completion_status` | STRING | 수료 여부 (수료, 미수료) |
| `assessment_score` | FLOAT | 평가 점수 (70-100) |

---

### 08. project_history.csv
**목적**: 프로젝트 참여 이력 및 피드백

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `project_member_id` | STRING | 프로젝트 멤버 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `project_id` | STRING | 프로젝트 ID |
| `project_name` | STRING | 프로젝트명 |
| `role` | STRING | 역할 (PL, 개발자, 기획자, QA, 디자이너 등) |
| `pm_qualitative_feedback` | STRING | PM 정성 피드백 |
| `peer_qualitative_feedback` | STRING | 동료 정성 피드백 |
| `start_date` | DATE | 시작일 |
| `end_date` | DATE | 종료일 |

**프로젝트 기간**: 2020-2024년, 연간 8-15개 프로젝트

**정성 피드백 특징**:
- **PM 피드백**: 구체적 달성률 (105-130%), 문제 해결 사례, 향후 역할 제안 포함
  - 예: "프로젝트 목표 118% 달성. 일정을 앞당겨 완수했으며, 팀원들의 신뢰가 매우 높음."
- **동료 피드백**: 협업 태도, 기술 기여, 팀워크 평가
  - 예: "기술적으로 뛰어나며 후배들을 잘 가르쳐줌. 팀의 기둥."

---

### 09. performance_review.csv
**목적**: 반기별 공식 성과 평가

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `review_id` | STRING | 평가 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `review_period` | STRING | 평가 기간 (예: 2023 H1, 2023 H2) |
| `final_grade` | STRING | 최종 등급 (S, A, B, C, D) |
| `manager_comment_development` | STRING | 관리자 코멘트 |

**등급 분포** (목표):
- S: 5%
- A: 25%
- B: 50%
- C: 15%
- D: 5%

**관리자 코멘트 특징**:
- **등급별 차별화**: S등급은 승진 추천, C등급은 PIP 수립 등 구체적 액션
- **수치 포함**: "반기 목표 145% 달성", "달성률 72%" 등
- **구체적 개선 방향**: "리더십 역량 개발 시 S등급 기대", "1:1 코칭 지원" 등
- **예시**:
  - S: "반기 목표 145% 달성으로 탁월한 성과. 핵심 프로젝트를 성공으로 이끔. 승진 적극 추천."
  - B: "기본 목표 달성. 품질 기준 충족. 주도성 강화 필요."

---

### 09-1. continuous_performance_review.csv
**목적**: 수시 성과 평가 (자기평가 + 상사평가)

| 컬럼명 | 데이터 타입 | 설명 | 비고 |
|--------|-------------|------|------|
| `review_id` | STRING | 평가 ID (PK) | CR00001 |
| `employee_id` | STRING | 직원 ID (FK) | EMP001 |
| `review_type` | STRING | 평가 유형 | 분기 평가, 프로젝트 종료 평가, 수시 평가, 목표 달성 평가 |
| `evaluation_period_start` | DATE | 평가 대상 기간 시작 | 2023-01-01 |
| `evaluation_period_end` | DATE | 평가 대상 기간 종료 | 2023-03-31 |
| `self_evaluation_timestamp` | DATETIME | 자기평가 작성 일시 | 2023-04-03 14:30:00 |
| `self_rating` | STRING | 자기평가 등급 | S, A, B, C, D |
| `self_comment` | STRING | 자기평가 정성 의견 | |
| `manager_evaluation_timestamp` | DATETIME | 상사평가 작성 일시 | 2023-04-08 11:15:00 |
| `manager_rating` | STRING | 상사평가 등급 | S, A, B, C, D |
| `manager_comment` | STRING | 상사평가 의견 | |
| `rating_gap` | INTEGER | 평가 등급 차이 여부 | 0=일치, 1=불일치 |
| `evaluation_status` | STRING | 평가 상태 | 완료 |

**핵심 특징**:
- **시간차 반영**: 자기평가 먼저, 상사평가가 2-10일 후 작성 (타임스탬프로 확인 가능)
- **평가 경향**: 자기평가는 일반적으로 높게, 상사평가는 보수적 (종종 한 단계 낮음)
- **정성 의견 품질**:
  - 자기평가: 구체적 성과 수치 + 역량 개발 + 협업 활동 조합
    - 예: "분기 목표 125% 달성하였습니다. Python 역량을 새롭게 습득하여 전문성을 높였으며, 타 부서와 7회 이상 협업 프로젝트 수행하였습니다."
  - 상사평가: 등급별 차별화된 구체적 피드백 + 개발 방향
    - 예: "목표 108% 달성으로 우수한 성과. 기술적 전문성이 돋보였으며, 리더십 역량 개발 시 더 큰 성장 기대."

---

### 09-2. goal_management.csv
**목적**: 목표 설정 및 달성도 관리 (OKR/MBO)

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `goal_id` | STRING | 목표 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `goal_type` | STRING | 목표 유형 (OKR, MBO, KPI) |
| `goal_category` | STRING | 목표 카테고리 (업무 성과, 역량 개발, 프로젝트 완수 등) |
| `goal_description` | STRING | 목표 설명 (SMART 형식) |
| `target_period` | STRING | 목표 기간 (2023 Q1, 2023 Q2 등) |
| `set_date` | DATE | 목표 설정일 |
| `target_completion_date` | DATE | 목표 완료 예정일 |
| `progress_percentage` | INTEGER | 진행률 (0-100%) |
| `status` | STRING | 상태 (진행중, 완료, 부분 달성) |
| `final_achievement_rate` | INTEGER | 최종 달성률 (완료 시) |
| `manager_id` | STRING | 관리자 ID (FK) |

**목표 카테고리**:
1. 업무 성과
2. 역량 개발
3. 프로젝트 완수
4. 프로세스 개선
5. 협업 강화
6. 혁신 과제

---

### 09-3. exit_interview.csv
**목적**: 퇴사자 인터뷰 (퇴사 사유, 만족도, 개선 제안)

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `exit_interview_id` | STRING | 인터뷰 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `interview_date` | DATE | 인터뷰 일자 |
| `exit_date` | DATE | 퇴사일 |
| `tenure_years` | FLOAT | 근속 연수 |
| `primary_reason_category` | STRING | 주 퇴사 사유 카테고리 |
| `primary_reason_detail` | STRING | 주 퇴사 사유 상세 |
| `secondary_reason` | STRING | 부차적 사유 |
| `would_recommend_company` | FLOAT | 회사 추천 의향 (1-5) |
| `overall_satisfaction` | FLOAT | 전반적 만족도 (1-5) |
| `qualitative_feedback` | STRING | 정성 피드백 |
| `improvement_suggestion` | STRING | 개선 제안사항 |
| `rehire_eligible` | STRING | 재입사 가능 여부 (Yes/No) |

**퇴사 사유 카테고리**:
1. 더 나은 기회 (더 좋은 연봉, 커리어 성장)
2. 보상 불만 (낮은 연봉, 승진 누락)
3. 업무 불만 (과도한 업무량, 업무 내용 불만족)
4. 상사/관계 (상사 갈등, 조직 문화 부적응)
5. 성장 정체 (경력 개발 기회 부족)
6. 워라밸 (과도한 야근, 번아웃)
7. 개인 사유 (학업, 건강, 가족, 창업)

**정성 피드백 예시**:
```
"재직 기간 동안 훌륭한 동료들에는 감사했습니다. 그러나 낮은 연봉 문제가 
구조적으로 발생하여 최종적으로 퇴사를 결정했습니다. 특히 낮은 연봉은 
우수 인재 유지를 위해 시급한 과제입니다."

"처음에는 기대가 컸으나 상사와의 갈등 문제가 심화되었습니다. 
우수한 기술 스택은 좋았지만, 과도한 야근까지 겹치면서 
건강과 가정을 위해 떠나기로 결정했습니다."
```

**분석 활용**:
- 퇴사 사유 트렌드 분석
- 부서별/직급별 퇴사 패턴
- 조직 문제점 식별
- 퇴사 사유와 팀 문화 서베이 연결 분석

---

### 09-4. team_culture_survey.csv
**목적**: 팀별 조직문화 서베이 (정성+정량 평가)

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `survey_id` | STRING | 서베이 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `org_id` | STRING | 조직 ID (FK) |
| `org_name` | STRING | 팀명 |
| `division_name` | STRING | 본부명 |
| `survey_year` | INTEGER | 서베이 연도 |
| `survey_date` | DATE | 서베이 일자 |
| `q_psychological_safety` | FLOAT | 심리적 안전감 (1-5) |
| `q_trust_in_leadership` | FLOAT | 리더 신뢰도 (1-5) |
| `q_collaboration` | FLOAT | 협업 수준 (1-5) |
| `q_innovation_encouragement` | FLOAT | 혁신 장려 (1-5) |
| `q_work_life_balance` | FLOAT | 워라밸 (1-5) |
| `q_recognition` | FLOAT | 인정과 보상 (1-5) |
| `q_fairness` | FLOAT | 공정성 (1-5) |
| `overall_team_satisfaction` | FLOAT | 전체 팀 만족도 (1-5) |
| `qualitative_comment` | STRING | 정성 의견 |
| `would_recommend_team` | FLOAT | 팀 추천 의향 (1-5) |

**핵심 특징**:
- **팀별 문화 수준 차이 반영** (excellent/good/average/poor)
  - Excellent: 평균 4.5점, 긍정적 의견
  - Good: 평균 4.0점, 만족하나 개선점 제시
  - Average: 평균 3.5점, 문제점 지적
  - Poor: 평균 2.5점, 심각한 문제 토로
- **리더십 평가와 연결**하여 팀장 영향력 분석 가능
- **정성 의견 예시**:
  - Excellent: "우리 팀은 심리적 안전감이 매우 잘 형성되어 있습니다. 실패를 두려워하지 않고 도전하는 분위기가 정착되어 있어 팀에 대한 자부심이 큽니다."
  - Poor: "팀 문화가 심각한 수준입니다. 리더가 일방적으로 지시만 하고 피드백 무시가 만연합니다. 이직 준비 중."

**분석 시나리오**:
- 팀별 문화 비교
- 리더십 평가와 팀 문화 상관관계
- 이직률이 높은 팀의 문화적 특징
- Poor 등급 팀의 리더십 360도 평가 연결 분석

---

### 09-5. rewards_and_discipline.csv
**목적**: 포상 및 징계 이력

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `record_id` | STRING | 기록 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `record_type` | STRING | 기록 유형 (포상, 징계) |
| `category` | STRING | 세부 유형 |
| `reason` | STRING | 사유 |
| `action_date` | DATE | 조치 일자 |
| `monetary_amount` | INTEGER | 금전적 금액 (원) |
| `issued_by` | STRING | 발행자 (관리자 ID) |
| `description` | STRING | 상세 설명 |
| `impact_on_record` | STRING | 인사 기록 영향 (Positive/Negative) |

**포상 유형**:
- 우수사원상 (50만원)
- 공로상 (100만원)
- 혁신상 (200만원)
- 팀워크상 (30만원)
- 고객만족상 (150만원)

**징계 유형**:
- 구두경고
- 서면경고
- 감봉 (-50만원)
- 정직

**분석 활용**:
- 성과 평가와 포상의 연결성
- 징계 후 성과 변화 추이
- 우수 인재 식별

---

### 09-6. one_on_one_meetings.csv
**목적**: 관리자-직원 간 1:1 미팅 기록

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `meeting_id` | STRING | 미팅 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `manager_id` | STRING | 관리자 ID (FK) |
| `meeting_datetime` | DATETIME | 미팅 일시 |
| `duration_minutes` | INTEGER | 미팅 시간 (분) |
| `discussion_topics` | STRING | 논의 주제 (파이프 구분) |
| `action_items` | STRING | 액션 아이템 (파이프 구분) |
| `next_meeting_scheduled` | DATE | 다음 미팅 예정일 |
| `employee_satisfaction_score` | FLOAT | 직원 만족도 (1-5) |
| `meeting_status` | STRING | 미팅 상태 (완료) |

**논의 주제 예시**:
- 업무 진행 상황 점검
- 성과 목표 검토 및 조정
- 커리어 개발 논의
- 업무 관련 어려움 및 지원 사항
- 최근 프로젝트 피드백

**빈도**: 월 1회 정기 미팅

---

### 10. skill_assessment.csv
**목적**: 다면 역량 진단 (자기/관리자/동료 평가)

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `assessment_id` | STRING | 진단 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `assessment_date` | DATE | 진단일 |
| `metric_code` | STRING | 지표 코드 (FK) |
| `self_rating` | FLOAT | 자기 평가 (1-5) |
| `manager_rating` | FLOAT | 관리자 평가 (1-5) |
| `peer_rating_avg` | FLOAT | 동료 평가 평균 (1-5) |

**평가 지표**: SKILL_001 ~ SKILL_010 (hr_metrics_definition 참조)

**인사이트**:
- 자기평가 vs 타인평가 갭 분석 가능
- 관리자 평가 vs 동료 평가 차이 확인

---

### 11. leadership_360_review.csv
**목적**: 리더십 360도 평가

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `review_id` | STRING | 평가 ID (PK) |
| `leader_employee_id` | STRING | 리더 직원 ID (FK) |
| `review_year` | INTEGER | 평가 연도 |
| `rater_relationship` | STRING | 평가자 관계 (Boss, Direct Report, Peer) |
| `metric_code` | STRING | 리더십 지표 코드 (FK) |
| `score` | FLOAT | 점수 (1-5) |

**평가 대상**: 팀장, 부장, 이사, 대표이사

**리더십 지표**: LEAD_001 ~ LEAD_007

**평가 관점**:
- Boss: 상사 관점
- Direct Report: 부하직원 관점
- Peer: 동료 리더 관점

---

### 12. engagement_survey.csv
**목적**: 조직 몰입도 설문 (연 1회)

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `survey_id` | STRING | 설문 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `survey_year` | INTEGER | 설문 연도 |
| `q_job_satisfaction` | FLOAT | 직무 만족도 (1-5) |
| `q_manager_relationship` | FLOAT | 상사 관계 (1-5) |
| `q_turnover_intention` | FLOAT | 이직 의도 (1-5, 높을수록 이직 의도 높음) |
| `q_work_life_balance` | FLOAT | 워라밸 (1-5) |
| `q_growth_opportunity` | FLOAT | 성장 기회 (1-5) |

**조사 연도**: 2022, 2023, 2024

---

### 13. compensation_history.csv
**목적**: 연도별 보상 이력

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `compensation_id` | STRING | 보상 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `effective_date` | DATE | 적용일 (매년 1월 1일) |
| `base_salary` | INTEGER | 기본 연봉 (원) |
| `annual_bonus_amount` | INTEGER | 연간 보너스 (원) |
| `total_compensation` | INTEGER | 총 보상 (원) |
| `currency` | STRING | 통화 (KRW) |

**직급별 기본 연봉 범위** (KRW):
- 사원: 35,000,000 ~ 42,000,000
- 주임: 40,000,000 ~ 48,000,000
- 대리: 48,000,000 ~ 58,000,000
- 과장: 58,000,000 ~ 72,000,000
- 차장: 72,000,000 ~ 90,000,000
- 팀장: 90,000,000 ~ 120,000,000
- 부장: 110,000,000 ~ 140,000,000
- 이사: 130,000,000 ~ 170,000,000

---

### 14. employee_yearly_snapshot.csv
**목적**: 연말 기준 직원 상태 스냅샷

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `snapshot_id` | STRING | 스냅샷 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `snapshot_date` | DATE | 스냅샷 기준일 (매년 12월 31일) |
| `division_name` | STRING | 본부명 |
| `org_name` | STRING | 팀명 |
| `job_title` | STRING | 직급 |
| `performance_grade` | STRING | 성과 등급 |
| `total_compensation` | INTEGER | 총 보상 |
| `key_skill_score_avg` | FLOAT | 핵심 역량 평균 점수 |
| `project_count` | INTEGER | 연간 참여 프로젝트 수 |
| `employment_status` | STRING | 재직 상태 |

**용도**: 시계열 분석, 직원별 연도 추이 파악

---

### 14. key_talent_pool.csv
**목적**: 핵심인재 풀 (성과 평가 기반 선정)

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `talent_id` | STRING | 인재 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `identification_date` | DATE | 선정 일자 |
| `talent_tier` | STRING | 인재 등급 (Tier 1/2/3) |
| `avg_performance_score` | FLOAT | 평균 성과 점수 (최근 2년) |
| `leadership_score` | FLOAT | 리더십 점수 (리더인 경우) |
| `rewards_count` | INTEGER | 포상 횟수 |
| `selection_reason` | STRING | 선정 사유 |
| `retention_risk` | STRING | 유지 리스크 (Low/Medium/High) |
| `development_priority` | STRING | 개발 우선순위 (최우선/우선/일반) |
| `succession_ready` | STRING | 승계 준비 여부 (Yes/Developing) |
| `review_date` | DATE | 검토 일자 |

**인재 등급 (Tier)**:
- **Tier 1 - Critical Talent**: 최우수 인재
  - 조건: 성과 4.5+ & (포상 2회+ OR 리더십 4.3+)
  - 인원: 약 5-10명 (전체의 3-5%)
  - 육성 방향: 차세대 리더, 핵심 프로젝트 리더
  
- **Tier 2 - High Potential**: 우수 인재
  - 조건: 성과 4.0+ & 관리자급 (과장 이상)
  - 인원: 약 15-25명 (전체의 10-15%)
  - 육성 방향: 리더십 개발, 전문가 트랙
  
- **Tier 3 - Emerging Talent**: 잠재 인재
  - 조건: 성과 3.8+ & 근속 5년 이하 & 젊은 직급
  - 인원: 약 10-15명 (전체의 5-8%)
  - 육성 방향: 장기 육성, 성장 기회 제공

**선정 기준 (우선순위)**:
1. ⭐⭐⭐ 최근 2년(2023-2024) 성과 평가 평균
2. ⭐⭐ 포상 이력 (객관적 우수성 증명)
3. ⭐⭐ 리더십 360도 평가 (리더인 경우, Direct Report 점수)
4. ⭐ 직급 및 경력 (잠재력 판단)

**유지 리스크 산정**:
- **데이터 소스**: Engagement Survey의 이직 의도(`q_turnover_intention`) 점수
- **분류 기준**:
  - High: 4.0+ (즉시 대응 필요, 보상/역할 재검토)
  - Medium: 3.0-3.9 (모니터링 필요)
  - Low: <3.0 (안정적)

**개발 우선순위**:
- Tier 1: **최우선** → 리더십 고도화 프로그램, 해외 연수, 임원 멘토링
- Tier 2: **우선** → 리더십 교육, 전문가 인증, 프로젝트 리더 기회
- Tier 3: **일반** → 기술 교육, 크로스팀 프로젝트, 멘토 배정

**분석 활용**:
- 인재 유지 전략 수립 (특히 High Risk 핵심인재)
- 핵심인재 이탈 시 조직 임팩트 분석
- 육성 투자 우선순위 결정 및 ROI 측정
- 승계 후보자 풀 확보

---

### 15. succession_plan.csv
**목적**: 핵심 직책별 승계 후보자 매핑

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `succession_plan_id` | STRING | 승계 계획 ID (PK) |
| `critical_position` | STRING | 핵심 직책 (팀장, 본부장) |
| `current_holder_id` | STRING | 현 담당자 ID (FK) |
| `current_holder_name` | STRING | 현 담당자 이름 |
| `org_name` | STRING | 조직명 |
| `division_name` | STRING | 본부명 |
| `successor_rank` | INTEGER | 후보자 순위 (1st/2nd/3rd choice) |
| `successor_id` | STRING | 후보자 ID (FK) |
| `successor_name` | STRING | 후보자 이름 |
| `successor_current_title` | STRING | 후보자 현 직급 |
| `readiness_level` | STRING | 준비도 (Ready Now / 1-2 Years / 3+ Years) |
| `development_needed` | STRING | 개발 필요 역량 |
| `is_key_talent` | STRING | 핵심인재 여부 (Yes/No) |
| `position_risk_level` | STRING | 직책 공백 리스크 (Low/Medium/High) |
| `plan_date` | DATE | 계획 수립일 |
| `next_review_date` | DATE | 차기 검토 예정일 |

**승계 대상 직책**:
- 본부장 3명
- 팀장 10명

**후보자 선정 로직** (데이터 기반):
1. **필수 조건**: `key_talent_pool`에서 `succession_ready = 'Yes'`인 인재만 (Tier 1/2)
2. **우선 순위**:
   - **본부장 후보**: 같은 본부의 팀장/차장 중 핵심인재 (같은 division_name)
   - **팀장 후보**: 같은 팀의 차장/과장 중 핵심인재 (같은 org_id)
   - 후보 부족 시: 같은 본부 내 타 팀에서 확대 검색
3. **준비도 평가** (성과 점수 기반):
   - **Ready Now**: 성과 4.5+ → 즉시 승계 가능, 개발 필요: "리더십 고도화, 전략적 사고"
   - **1-2 Years**: 성과 4.0-4.5 → 추가 육성 후 가능, 개발 필요: "관리 역량 강화, 의사결정 경험"
   - **3+ Years**: 성과 <4.0 → 장기 육성, 개발 필요: "리더십 기본, 팀 관리 경험"
4. **후보자 순위**: 각 직책당 1-3명 (1st/2nd/3rd choice)

**직책 리스크 평가**:
- **데이터 소스**: 현 직책자의 `key_talent_pool.retention_risk`
- **리스크 레벨**:
  - High: 현 담당자 퇴사 가능성 높음 → 승계 준비 최우선
  - Medium: 모니터링 필요
  - Low: 안정적
- **리스크 미포함**: 현 담당자가 핵심인재가 아닌 경우 (Medium/High로 랜덤 설정)

**승계 계획 매트릭스 예시**:
```
[본부장 직책]
현 담당자: DIV002 (기술본부장) - 리스크 Low
├─ 1st choice: TL003 (AI솔루션개발팀장) - Ready Now - Tier 1
├─ 2nd choice: TL004 (플랫폼개발팀장) - 1-2 Years - Tier 2
└─ 3rd choice: EMP045 (차장) - 3+ Years - Tier 2

[팀장 직책] 
현 담당자: TL003 (AI솔루션개발팀장) - 리스크 High
├─ 1st choice: EMP012 (과장) - Ready Now - Tier 1
└─ 2nd choice: EMP034 (과장) - 1-2 Years - Tier 2
⚠️ 승계 후보 부족 - 타 팀에서 영입 검토 필요
```

**분석 시나리오**:
- ⚠️ **고위험 상황**: 승계 후보 없음 + 직책 리스크 High
- 📊 **후보자 품질**: Ready Now 후보가 있는 직책 vs 없는 직책
- 🎯 **핵심인재 경력 경로**: 여러 직책의 후보로 지목된 인재 (고속 성장 트랙)
- 🔄 **조직 리스크 관리**: 동시 퇴사 시 조직 마비 가능성

---

### 16. employee_yearly_snapshot.csv
**목적**: 연말 기준 직원 상태 스냅샷

| 컬럼명 | 데이터 타입 | 설명 |
|--------|-------------|------|
| `snapshot_id` | STRING | 스냅샷 ID (PK) |
| `employee_id` | STRING | 직원 ID (FK) |
| `snapshot_date` | DATE | 스냅샷 기준일 (매년 12월 31일) |
| `division_name` | STRING | 본부명 |
| `org_name` | STRING | 팀명 |
| `job_title` | STRING | 직급 |
| `performance_grade` | STRING | 성과 등급 |
| `total_compensation` | INTEGER | 총 보상 |
| `key_skill_score_avg` | FLOAT | 핵심 역량 평균 점수 |
| `project_count` | INTEGER | 연간 참여 프로젝트 수 |
| `employment_status` | STRING | 재직 상태 |

**용도**: 시계열 분석, 직원별 연도 추이 파악

---

## 데이터 관계도

```
organization_structure (조직 위계)
├── org_id, parent_org_id (자기 참조)
└── head_employee_id → employee_info.employee_id

employee_info (중심 테이블)
├── org_id → organization_structure.org_id
├── manager_id → employee_info.employee_id (자기 참조)
├── job_history (1:N)
│   └── org_id → organization_structure.org_id
├── personal_traits (1:1)
├── recruitment_history (1:1)
├── onboarding_program (1:N)
├── training_history (1:N)
├── project_history (1:N)
├── performance_review (1:N)
├── continuous_performance_review (1:N)
├── goal_management (1:N)
│   └── manager_id → employee_info.employee_id
├── exit_interview (1:1) - 퇴사자만
├── team_culture_survey (1:N)
│   └── org_id → organization_structure.org_id
├── rewards_and_discipline (1:N)
├── one_on_one_meetings (1:N)
│   └── manager_id → employee_info.employee_id
├── skill_assessment (1:N)
│   └── metric_code → hr_metrics_definition.metric_code
├── leadership_360_review (1:N) - 리더만
│   ├── leader_employee_id → employee_info.employee_id
│   └── metric_code → hr_metrics_definition.metric_code
├── engagement_survey (1:N)
├── compensation_history (1:N)
├── key_talent_pool (1:1) - 핵심인재만
│   └── 성과평가, 포상, 리더십 데이터 기반 선정
└── employee_yearly_snapshot (1:N)

reporting_lines (보고 라인)
├── employee_id → employee_info.employee_id
├── immediate_manager_id → employee_info.employee_id
├── second_level_manager_id → employee_info.employee_id
└── third_level_manager_id → employee_info.employee_id

succession_plan (승계 계획)
├── current_holder_id → employee_info.employee_id
└── successor_id → key_talent_pool.employee_id (핵심인재 풀에서만)
```

**주요 외래키**:
- `employee_id`: 거의 모든 테이블
- `manager_id`: employee_info.employee_id를 참조
- `org_id`: organization_structure.org_id를 참조
- `metric_code`: hr_metrics_definition을 참조

**데이터 논리적 연결**:
```
성과 평가 (우수) + 포상 이력 + 리더십 평가 (우수)
           ↓
    핵심인재 선정 (Tier 1/2/3)
           ↓
    승계 후보자로 매핑
           ↓
    육성 및 개발 계획
```

---

## 주요 사용 시나리오

### 1. 조직도 및 보고 라인 조회
```
-- 전체 조직 구조
SELECT org_id, org_name, org_type, level, 
       parent_org_id, head_employee_id
FROM organization_structure
ORDER BY level, org_id;

-- 특정 직원의 보고 라인
SELECT r.employee_name,
       r.immediate_manager_id,
       r.second_level_manager_id,
       r.third_level_manager_id,
       r.reporting_depth
FROM reporting_lines r
WHERE r.employee_id = 'EMP001';

-- 본부별 팀 및 인원
SELECT o1.org_name as division,
       o2.org_name as team,
       COUNT(e.employee_id) as headcount
FROM organization_structure o1
JOIN organization_structure o2 ON o1.org_id = o2.parent_org_id
JOIN employee_info e ON o2.org_id = e.org_id
WHERE o1.level = 1
GROUP BY o1.org_name, o2.org_name
ORDER BY o1.org_name, o2.org_name;
```

### 2. 직원 종합 프로필 조회
```
SELECT e.name, e.job_title, 
       e.org_name as team, 
       e.division_name,
       p.openness, p.conscientiousness, p.extraversion,
       c.total_compensation
FROM employee_info e
LEFT JOIN personal_traits p ON e.employee_id = p.employee_id
LEFT JOIN compensation_history c ON e.employee_id = c.employee_id
WHERE e.employee_id = 'EMP001'
  AND c.effective_date = '2024-01-01';
```

### 2. 성과-목표-보상 연계 분석
```
SELECT g.goal_description, 
       g.final_achievement_rate,
       pr.final_grade,
       c.annual_bonus_amount
FROM goal_management g
JOIN performance_review pr ON g.employee_id = pr.employee_id
JOIN compensation_history c ON g.employee_id = c.employee_id
WHERE g.employee_id = 'EMP001'
  AND g.target_period = '2023 Q4'
  AND pr.review_period = '2023 H2';
```

### 3. 리더십 평가 추이 분석
```
SELECT leader_employee_id,
       review_year,
       rater_relationship,
       AVG(score) as avg_score
FROM leadership_360_review
WHERE metric_code = 'LEAD_002'  -- 팀 육성 및 개발
GROUP BY leader_employee_id, review_year, rater_relationship
ORDER BY leader_employee_id, review_year;
```

### 4. 퇴사 사유 분석 및 패턴
```
SELECT primary_reason_category,
       COUNT(*) as exit_count,
       AVG(tenure_years) as avg_tenure,
       AVG(would_recommend_company) as avg_recommend_score,
       AVG(overall_satisfaction) as avg_satisfaction
FROM exit_interview
GROUP BY primary_reason_category
ORDER BY exit_count DESC;
```

### 5. 자기평가 vs 상사평가 갭 분석
```
SELECT employee_id,
       self_rating,
       manager_rating,
       self_comment,
       manager_comment,
       DATEDIFF(manager_evaluation_timestamp, self_evaluation_timestamp) as review_gap_days
FROM continuous_performance_review
WHERE rating_gap = 1  -- 등급 불일치
ORDER BY review_gap_days DESC;
```

### 6. 팀별 문화와 리더십의 상관관계
```
SELECT tc.department_name,
       AVG(tc.overall_team_satisfaction) as team_culture_score,
       AVG(l.score) as leadership_score,
       COUNT(DISTINCT e.employee_id) as team_member_count
FROM team_culture_survey tc
JOIN employee_info e ON tc.department_id = e.department_id
JOIN leadership_360_review l ON e.manager_id = l.leader_employee_id
WHERE tc.survey_year = 2024
  AND l.review_year = 2024
  AND l.rater_relationship = 'Direct Report'
GROUP BY tc.department_name
ORDER BY team_culture_score DESC;
```

### 7. 포상 이력과 성과 평가의 연결성
```
SELECT rd.employee_id,
       COUNT(CASE WHEN rd.record_type = '포상' THEN 1 END) as reward_count,
       SUM(rd.monetary_amount) as total_reward_amount,
       AVG(CASE WHEN pr.final_grade = 'S' THEN 5
                WHEN pr.final_grade = 'A' THEN 4
                WHEN pr.final_grade = 'B' THEN 3
                ELSE 2 END) as avg_performance_score
FROM rewards_and_discipline rd
JOIN performance_review pr ON rd.employee_id = pr.employee_id
WHERE rd.record_type = '포상'
GROUP BY rd.employee_id
ORDER BY reward_count DESC;
```

### 8. 본부별 성과 및 보상 분석
```
SELECT e.division_name,
       AVG(CASE WHEN pr.final_grade = 'S' THEN 5
                WHEN pr.final_grade = 'A' THEN 4
                WHEN pr.final_grade = 'B' THEN 3
                WHEN pr.final_grade = 'C' THEN 2
                ELSE 1 END) as avg_performance_score,
       AVG(c.total_compensation) as avg_total_comp,
       COUNT(DISTINCT e.employee_id) as headcount
FROM employee_info e
JOIN performance_review pr ON e.employee_id = pr.employee_id
JOIN compensation_history c ON e.employee_id = c.employee_id
WHERE pr.review_period = '2024 H1'
  AND c.effective_date = '2024-01-01'
GROUP BY e.division_name
ORDER BY avg_performance_score DESC;
```

### 9. 리더의 관리 범위 (Span of Control)
```
SELECT m.employee_id as manager_id,
       m.name as manager_name,
       m.job_title,
       COUNT(e.employee_id) as direct_reports,
       AVG(pr.final_grade) as team_avg_performance
FROM employee_info m
JOIN employee_info e ON m.employee_id = e.manager_id
LEFT JOIN performance_review pr ON e.employee_id = pr.employee_id
WHERE pr.review_period = '2024 H1'
  AND m.job_title IN ('팀장', '본부장')
GROUP BY m.employee_id, m.name, m.job_title
ORDER BY direct_reports DESC;
```

### 10. 핵심인재 분석 및 유지 리스크
```
SELECT kt.talent_tier,
       COUNT(*) as talent_count,
       AVG(kt.avg_performance_score) as avg_performance,
       SUM(CASE WHEN kt.retention_risk = 'High' THEN 1 ELSE 0 END) as high_risk_count,
       AVG(c.total_compensation) as avg_compensation
FROM key_talent_pool kt
JOIN compensation_history c ON kt.employee_id = c.employee_id
WHERE c.effective_date = '2024-01-01'
GROUP BY kt.talent_tier
ORDER BY avg_performance DESC;
```

### 11. 승계 계획 준비도 현황
```
SELECT sp.critical_position,
       sp.org_name,
       COUNT(*) as successor_count,
       SUM(CASE WHEN sp.readiness_level = 'Ready Now' THEN 1 ELSE 0 END) as ready_now_count,
       sp.position_risk_level
FROM succession_plan sp
GROUP BY sp.critical_position, sp.org_name, sp.position_risk_level
HAVING ready_now_count = 0  -- 즉시 승계 가능한 후보 없음
ORDER BY sp.position_risk_level DESC;
```

### 12. 핵심인재 육성 효과 분석
```
SELECT kt.employee_id,
       kt.talent_tier,
       COUNT(t.training_id) as training_count,
       kt.avg_performance_score,
       kt.development_priority
FROM key_talent_pool kt
LEFT JOIN training_history t ON kt.employee_id = t.employee_id
WHERE t.start_date >= '2023-01-01'
GROUP BY kt.employee_id, kt.talent_tier, kt.avg_performance_score, kt.development_priority
ORDER BY kt.development_priority, kt.avg_performance_score DESC;
```

---

## 데이터 품질 및 제약사항

### 데이터 품질 특징
✅ **강점**:
- 통계적 타당성: 정규분포 기반 점수
- 시간적 일관성: 타임스탬프 순서 보장
- 관계적 무결성: FK 관계 유지
- 현실 반영: 실제 HR 프로세스 기반

⚠️ **제약사항**:
- 가상 데이터: 실제 기업 데이터 아님
- 단순화: 복잡한 HR 프로세스를 단순화함
- 한계: 일부 edge case 미반영

### 데이터 생성 규칙
- **정규분포 사용**: 성과 점수, 역량 평가, 만족도 등
- **시계열 일관성**: 입사일 < 교육일 < 평가일 < 승계 계획
- **비율 유지**: 재직 90%, 퇴사 10%, 핵심인재 15-20%
- **현실적 분포**: 직급별 연봉 범위 준수
- **정성 의견 생성**: 
  - 조합형 문장 생성으로 수백 가지 변형 (템플릿 반복 최소화)
  - 구체적 수치 포함 (예: "목표 125% 달성", "협업 7회 수행")
  - 등급/상황별 차별화된 톤과 내용
- **데이터 논리적 연결**: 
  - 성과 우수 → 포상 → 핵심인재 선정 → 승계 후보
  - 팀 문화 Poor → 리더십 평가 낮음 → 이직률 높음

---

## 업데이트 이력

| 버전 | 날짜 | 변경 내역 |
|------|------|-----------|
| 1.0 | 2024 | 초기 버전 생성 (17개 파일)<br>- 기본 HR 데이터 구조 |
| 2.0 | 2024 | 조직 구조 및 보고 라인 추가 (19개 파일)<br>- organization_structure.csv 추가<br>- reporting_lines.csv 추가<br>- employee_info에 org_id, division_name 추가<br>- 3단계 위계 구조 구현 (본부장 직급 추가) |
| 2.1 | 2024 | **인재 관리 및 정성 의견 개선 (21개 파일)**<br>- key_talent_pool.csv 추가 (성과 기반 핵심인재 선정)<br>- succession_plan.csv 추가 (승계 계획)<br>- 데이터 간 논리적 연결: 성과 → 핵심인재 → 승계후보<br>- **정성 의견 대폭 개선**: 조합형 생성으로 다양성↑ 구체성↑<br>- 프로젝트, 성과평가, 팀문화, 퇴사인터뷰 피드백 풍부화 |
| 2.2 | 2024 | **채용 전형 검사 데이터 추가 (25개 파일)**<br>- recruitment_test_definitions.csv 추가 (검사 메타데이터)<br>- recruitment_aptitude_results.csv 추가 (적성검사: 언어/수리/상황판단/사회상식/대인관계)<br>- recruitment_cpi_results.csv 추가 (CPI 성격검사: 20개 일상척도 + 벡터척도 + 라이프스타일)<br>- recruitment_mmpi_results.csv 추가 (MMPI 진단검사: 타당도척도 + 10개 임상척도)<br>- **현실적 채용 프로세스**: 지원→적성검사→인성검사→면접→합격<br>- **퇴사자 vs 재직자 비교**: 채용 시 검사 결과와 퇴사 상관관계 분석 가능<br>- **직무별 특성 반영**: 본부별 요구 역량에 따른 점수 차별화 |
| 2.3 | 2024 | **메타데이터 통합 및 승진 이력 개선 (25개 파일)**<br>- **통합 메타데이터**: 모든 지표를 hr_metrics_definition.csv에 통합 (80개 지표)<br>- **풍부한 정의**: 각 지표별 상세 정의 + 높을때/낮을때 특성 추가<br>- **Big-5 요인 추가**: 개방성, 성실성, 외향성, 친화성, 신경증 메타데이터 포함<br>- **승진 이력 개선**: 팀장들도 하위 직급에서 시작하여 점진적 승진<br>- **파일 번호 정리**: 00-25번 순차 정렬, 중복 해결<br>- **AI 챗봇 최적화**: 단일 메타데이터 소스에서 모든 성격/역량 질문 답변 가능 |
| 2.4 | 2024 | **CONFIG 설정 분리 및 데이터 간 상관관계 강화 (25개 파일)**<br>- **CONFIG 딕셔너리**: 16개 설정값 분리로 쉬운 커스터마이징<br>- **데이터 간 상관관계 구현**: 검사 결과 간 현실적 상관관계 (r=0.33~0.64)<br>  * 적성 대인관계 ↔ CPI 사교성/공감성 (r=0.33~0.39)<br>  * 적성 상황판단 ↔ CPI 지배성 (r=0.39, 리더급 0.51)<br>  * CPI 안녕감 ↔ MMPI 우울증 역상관 (r=-0.63)<br>  * CPI 사교성 ↔ MMPI 사회적내향성 역상관 (r=-0.64)<br>- **상관관계 ON/OFF**: CONFIG['ENABLE_CORRELATION']로 제어 가능<br>- **강도 조정 가능**: CONFIG['CORRELATION_STRENGTH'] (0.0~1.0)<br>- **README 상세화**: 채용 검사 파일별 상세 설명 추가 |

---

## 문의 및 개선 제안

이 데이터셋에 대한 질문이나 개선 제안이 있으시면 이슈를 등록해주세요.

**생성 스크립트**: `generate_hr_data.py`

