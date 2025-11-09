# GDB-HR 프로젝트 데이터셋

**넥스트젠 테크놀로지스 HR 데이터 - 200명 규모 종합 HR 시스템**

## 📊 프로젝트 개요

이 프로젝트는 GDB(Graph Database) 기반 HR 챗봇을 위한 **현실적이고 포괄적인 HR 데이터셋**을 생성합니다.

- **조직 규모**: 200명 (재직자 약 180명)
- **조직 구조**: 3본부 10팀 (경영지원, 기술, 비즈니스)
- **데이터 기간**: 2015년 ~ 2024년 (10년)
- **총 파일 수**: 25개 CSV
- **총 레코드**: 약 21,300+
- **신규 추가**: 채용 전형 검사 (CPI, MMPI, 적성검사)

## 🚀 빠른 시작

### 1. 환경 설정
```bash
pip install pandas numpy faker
```

### 2. 데이터 생성
```bash
python generate_hr_data.py
```

### 3. 결과 확인
```bash
ls data/
# 25개 CSV 파일이 생성됩니다 (채용 전형 검사 4개 포함)
```

## 📁 생성되는 파일 목록

### 조직 구조 (2개)
- `00_organization_structure.csv` - 부서 간 위계 (3본부 10팀)
- `01_reporting_lines.csv` - 전체 보고 라인 (대표→본부장→팀장→팀원)

### 마스터 데이터 (4개)
- `02_hr_metrics_definition.csv` - **통합 지표 사전** (80개 지표)
- `03_employee_info.csv` - 직원 기본 정보
- `04_job_history.csv` - 경력 이력 (현실적 승진 과정)
- `05_personal_traits.csv` - Big-5 성격 검사

### 채용/교육 (6개) ⭐ **채용 전형 검사 추가**
- `06_recruitment_history.csv` - 채용 이력 (지원~합격~입사 전 과정)
- `07_recruitment_aptitude_results.csv` - **적성검사 결과**
  - 언어적 능력 (어휘, 문장구성, 해독, 영어)
  - 수리적 능력 (수량처리, 통계처리, 논리사고)
  - 상황판단, 사회상식, 대인관계 능력
  - 직무별 점수 차별화 (기술본부 수리↑, 경영지원본부 언어↑)
- `08_recruitment_cpi_results.csv` - **CPI 성격검사 결과**
  - 20개 일상척도 (지배성, 사교성, 책임감, 자기통제 등)
  - 3개 벡터척도 (외향성-내향성, 규범지향-규범회의, 자아실현)
  - 라이프스타일 유형 (Alpha, Beta, Gamma, Delta)
  - T점수 기반, 리더급 vs 일반직원 특성 차별화
- `09_recruitment_mmpi_results.csv` - **MMPI 진단검사 결과**
  - 타당도 척도 (L, F, K) - 응답 신뢰성 검증
  - 10개 임상척도 (우울, 불안, 반사회성 등)
  - 퇴사자 특성 반영 (우울척도 65 vs 재직자 50)
- `10_onboarding_program.csv` - 온보딩
- `11_training_history.csv` - 교육 이력

### 프로젝트/성과 (4개)
- `12_project_history.csv` - 프로젝트 이력
- `13_performance_review.csv` - 반기별 성과 평가
- `14_continuous_performance_review.csv` - 수시 성과평가 (자기/상사 타임스탬프)
- `15_goal_management.csv` - 목표 관리 (OKR/MBO)

### 조직 문화/퇴사 (4개)
- `16_exit_interview.csv` - 퇴사자 인터뷰
- `17_team_culture_survey.csv` - 팀별 조직문화 (정성+정량)
- `18_rewards_and_discipline.csv` - 포상/징계
- `19_one_on_one_meetings.csv` - 1:1 미팅

### 평가/보상 (4개)
- `20_skill_assessment.csv` - 역량 진단 (다면평가)
- `21_leadership_360_review.csv` - 리더십 360도
- `22_engagement_survey.csv` - 조직 몰입도
- `23_compensation_history.csv` - 보상 이력

### 인재 관리 (2개)
- `24_key_talent_pool.csv` - **핵심인재 풀** (성과 기반 선정)
- `25_succession_plan.csv` - **승계 계획** (후보자 매핑)

### 요약 (1개)
- `26_employee_yearly_snapshot.csv` - 연간 스냅샷

## 🎯 핵심 특징

### ✅ 1. 조직 위계 구조
```
넥스트젠 테크놀로지스
├── 경영지원본부 (본부장: DIV001)
│   ├── HR팀 (팀장: TL001)
│   └── 재무팀 (팀장: TL002)
├── 기술본부 (본부장: DIV002)
│   ├── AI솔루션개발팀 (팀장: TL003)
│   ├── 플랫폼개발팀 (팀장: TL004)
│   └── ... (6개 팀)
└── 비즈니스본부 (본부장: DIV003)
    ├── 마케팅팀 (팀장: TL009)
    └── 영업팀 (팀장: TL010)
```

### ✅ 2. 데이터 논리적 연결
```
성과 평가 (우수) + 포상 이력 + 리더십 평가
           ↓
    핵심인재 선정 (Tier 1/2/3)
           ↓
    승계 후보자 매핑
           ↓
    육성 계획 수립
```

### ✅ 3. 풍부한 정성 의견
- **조합형 문장 생성**: 수백 가지 변형 (반복 최소화)
- **구체적 수치**: "목표 125% 달성", "협업 7회", "달성률 72%"
- **차별화**: 등급별, 팀 문화별, 상황별 다른 톤

**예시**:
```
[프로젝트 PM 피드백]
"프로젝트 목표 118% 달성. 품질 기준을 초과하여 완수했으며, 
이해관계자 만족도가 매우 높음. 향후 리더 역할 기대."

[수시 평가 자기평가]
"핵심 KPI 5건 완료하였습니다. AI/ML 역량을 새롭게 습득하며 
전문성을 높였고, 타 부서와 7회 이상 협업 프로젝트 수행하였습니다."

[팀 문화 서베이 - Poor 팀]
"팀 문화가 심각한 수준입니다. 리더가 일방적으로 지시만 하고 
피드백 무시가 만연합니다. 이직 준비 중."
```

### ✅ 4. 통계적 타당성
- 정규분포 기반 점수 생성
- 성과 등급 분포: S(5%), A(25%), B(50%), C(15%), D(5%)
- Big-5 성격 점수: 평균 65, 표준편차 15

## 💡 주요 분석 시나리오

### 1. 핵심인재 이탈 리스크
```sql
SELECT kt.employee_id, kt.talent_tier, kt.retention_risk,
       e.name, e.job_title
FROM key_talent_pool kt
JOIN employee_info e ON kt.employee_id = e.employee_id
WHERE kt.retention_risk = 'High'
  AND kt.talent_tier = 'Tier 1 - Critical Talent';
```
→ **인사이트**: 즉시 보상/역할 조정 필요한 핵심인재 식별

### 2. 승계 공백 리스크
```sql
SELECT sp.org_name, sp.critical_position, sp.position_risk_level,
       COUNT(*) as successor_count
FROM succession_plan sp
GROUP BY sp.org_name, sp.critical_position, sp.position_risk_level
HAVING successor_count = 0 AND position_risk_level = 'High';
```
→ **인사이트**: 후보자 없는 고위험 직책 (조직 리스크)

### 3. 팀 문화와 리더십 상관관계
```sql
SELECT tc.org_name,
       AVG(tc.q_trust_in_leadership) as trust_score,
       AVG(l360.score) as leadership_score
FROM team_culture_survey tc
JOIN employee_info e ON tc.org_id = e.org_id
JOIN leadership_360_review l360 ON e.manager_id = l360.leader_employee_id
WHERE tc.survey_year = 2024
  AND l360.review_year = 2024
  AND l360.rater_relationship = 'Direct Report'
GROUP BY tc.org_name;
```
→ **인사이트**: 리더십 점수 낮은 팀의 문화 문제

### 4. 자기평가 vs 상사평가 갭
```sql
SELECT employee_id, self_rating, manager_rating,
       DATEDIFF(day, self_evaluation_timestamp, manager_evaluation_timestamp) as review_gap
FROM continuous_performance_review
WHERE rating_gap = 1
ORDER BY review_gap;
```
→ **인사이트**: 인식 차이 큰 직원 식별

## 📖 상세 문서

자세한 데이터 명세는 **[DATA_SPECIFICATION.md](DATA_SPECIFICATION.md)** 참조

- 전체 스키마 설명
- 컬럼별 상세 정의
- 데이터 관계도
- 12가지 쿼리 시나리오
- 샘플 데이터 예시

## 🔧 커스터마이징

### 직원 수 변경
```python
# generate_hr_data.py 수정
while len(employees) < 120:  # 120명으로 변경
```

### 평가 기간 조정
```python
review_periods = ['2023 H1', '2023 H2', '2024 H1', '2024 H2']  # 기간 추가
```

### 핵심인재 선정 기준 변경
```python
if avg_performance >= 4.3:  # 기준 조정
    talent_tier = 'Tier 1 - Critical Talent'
```

## 📊 생성 결과 예시

```
=== 생성 요약 ===
총 직원 수: 200명
재직자: 180명
퇴사자: 20명

=== 핵심인재 통계 ===
Tier 1 (Critical Talent): 8명
Tier 2 (High Potential): 22명
Tier 3 (Emerging Talent): 12명
총 핵심인재: 42명 (23.3%)

승계 계획 수립 직책: 13개
승계 후보자 매핑: 28건
```

## 🎓 GDB 활용 예시

이 데이터는 Neo4j, AWS Neptune 등 그래프 DB에서 다음과 같이 활용됩니다:

```cypher
// Neo4j 예시: 핵심인재의 네트워크 분석
MATCH (e:Employee)-[:IS_KEY_TALENT]->(kt:KeyTalent)
WHERE kt.talent_tier = 'Tier 1 - Critical Talent'
MATCH (e)-[:WORKS_IN]->(team:Team)-[:BELONGS_TO]->(div:Division)
MATCH (e)-[:HAS_MANAGER]->(manager:Employee)
RETURN e.name, team.name, div.name, 
       kt.retention_risk, kt.avg_performance_score;
```

## ⚠️ 주의사항

- 이 데이터는 **교육/실험 목적의 가상 데이터**입니다
- 실제 개인정보가 아니며, Faker 라이브러리로 생성됨
- 실제 HR 시스템에 사용 시 개인정보보호법 준수 필요

## 📞 문의 및 기여

이슈나 개선 제안은 환영합니다!

---

**License**: MIT  
**Author**: HR Data Generation Team  
**Last Updated**: 2024

