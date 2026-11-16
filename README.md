# K-Digital Asset Policy Intelligence (K-DAPI)

해외 디지털자산·토큰화 사업모델을 공식 근거로 조사하고, 한국 법률·정책과 비교해 국내 도입 조건과 금융기관·핀테크의 사업적 시사점을 도출하는 Agent Skill입니다.

단순 요약이 아니라 다음 흐름을 재사용 가능한 방법론으로 제공합니다.

> 해외 사업모델 → 해외 규제 → 한국 규제 → 제도 격차 → 국내 적용 조건 → 사업 시사점

## 주요 기능

- 영문 PDF·공식 URL·연구질문 기반 분석
- 법률, 정책 발표, 입법예고, 시행 상태 분리
- 주장별 Evidence ID와 사실·추론·미검증·검토필요 등급
- 국문 심층 보고서와 영문 Executive Summary
- JSON Schema와 표준 라이브러리 기반 검증 도구
- HTML·텍스트·PDF 원문 추출, 발췌문 대조, 문서 해시 기록
- 정규화된 법적 주장 유형과 Evidence 법적 상태의 호환성 검사
- API 없이도 사용 가능한 템플릿·방법론

이 스킬은 법률자문이나 투자 권유를 제공하지 않습니다.

## 설치

저장소 공개 후 Skills CLI로 설치합니다.

```bash
npx skills add junjunny/k-digital-asset-policy-intelligence@k-digital-asset-policy-intelligence
```

또는 이 저장소를 내려받아 `SKILL.md`가 포함된 폴더를 지원되는 에이전트의 skills 디렉터리에 복사합니다.

## 사용 예시

### 리서처

```text
Use $k-digital-asset-policy-intelligence to analyze this overseas tokenized bond,
compare it with Korea's token securities framework as of 2026-11-16,
and produce a Korean report plus an English executive summary.
```

```text
EU DLT Pilot과 한국 토큰증권 제도를 비교하고,
국내 증권사와 핀테크가 준비해야 할 인프라·인가 조건을 분석해줘.
```

### 개발자·검증 담당자

```text
이 Evidence JSON의 공식 URL을 다시 조회해 HTML·PDF 원문과 발췌문을 대조하고,
문서 해시와 검증 상태를 저장한 뒤 규제 주장 유형의 오류를 검사해줘.
```

스킬은 확인된 사실, 사업적 추론, 입법예고, 미검증 항목을 분리합니다. 사용자가 제공한 법률 정보도 공식 원문 없이는 확정 사실로 승격하지 않습니다.

## 결과 검증

Python 3.9 이상이 필요합니다. PDF 원문 추출 기능을 사용하려면 다음 의존성을 설치합니다.

```bash
python3 -m pip install -r requirements.txt
```

```bash
python3 scripts/validate_sources.py examples/tokenization-case-study/evidence.json
python3 scripts/validate_report.py examples/tokenization-case-study/report.json
python3 scripts/verify_evidence.py examples/hong-kong-digital-green-bond/evidence.json --output /tmp/kdapi-verification.json
python3 -m unittest discover -s tests -v
```

실시간 URL 접근까지 확인하려면 다음 옵션을 사용합니다. 공식 사이트가 HEAD 요청이나 자동 접근을 제한하면 수동 검증이 필요할 수 있습니다.

```bash
python3 scripts/validate_sources.py examples/tokenization-case-study/evidence.json --check-urls
```

## 실제 사례

[EIB 디지털 채권과 한국 적용 조건](examples/tokenization-case-study/report-ko.md)은 EIB의 £50m sterling digital bond를 2027년 시행 예정인 한국 토큰증권 제도와 비교합니다. 근거 데이터는 [evidence.json](examples/tokenization-case-study/evidence.json), 영문 요약은 [executive-summary-en.md](examples/tokenization-case-study/executive-summary-en.md)에 있습니다.

[홍콩 다중통화 디지털 녹색채권 사례](examples/hong-kong-digital-green-bond/report-ko.md)는 기존 EIB 보고서와 독립적으로 조사한 재현성 검증 사례입니다. HTML·PDF 원문 대조 결과와 research log를 함께 제공합니다.

## 구조

- `SKILL.md`: 짧은 실행 진입점
- `references/`: 방법론, 근거 정책, 규제 프레임워크, 용어집
- `templates/`: 리서치 브리프와 보고서 템플릿
- `schemas/`: evidence·finding·report JSON Schema
- `scripts/`: 출처·보고서 검증기
- `examples/`: 재현 가능한 사례 분석
- `docs/`: 로드맵, 단계별 기록, 테스트, 인계

## 외부 스킬과의 관계

skills.sh의 일반 research, deep-research, financial research, legal memo 계열을 조사했으나 이 저장소에는 복제하거나 필수 의존성으로 포함하지 않았습니다. K-DAPI는 한국 토큰증권의 시행 상태 구분과 해외 사업모델의 국내 적용 조건에 특화합니다.

## 라이선스와 기여

코드는 MIT License로 공개합니다. 규제 정보는 시간에 따라 바뀌므로 기여 시 분석 기준일, 공식 URL, 시행 상태, Evidence ID를 함께 갱신해 주세요.

