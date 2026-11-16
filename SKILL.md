---
name: k-digital-asset-policy-intelligence
description: 해외 디지털자산·토큰화 사업모델을 공식 근거로 조사하고 한국 법률·정책과 비교해 국내 도입 조건과 금융기관·핀테크 시사점을 국문 보고서 및 영문 요약으로 작성한다. 단순 코인 시세 조회나 투자 추천에는 사용하지 않는다.
---

# K-Digital Asset Policy Intelligence

해외 사업모델을 요약하는 데 그치지 말고 `사업모델 → 규제 비교 → 한국 적용 조건 → 사업 시사점`을 연결한다. 결과는 법률자문이나 투자 권유가 아니다.

## 시작

1. 질문, 분석 기준일, 관할권, 대상 독자, 산출물 언어를 확정한다. 누락값은 합리적으로 정하되 보고서에 가정을 적는다.
2. PDF·공식 URL·사용자 자료를 우선 읽는다. 웹 검색이 가능하면 원문 법령과 감독기관 자료를 확인하고, 불가능하면 제공 자료의 범위와 최신성 한계를 밝힌다.
3. 상세 절차는 [연구 방법론](references/research-methodology.md), 근거 등급과 인용 규칙은 [근거 정책](references/evidence-policy.md)을 따른다.
4. 한국 법률 분석에는 [한국 규제 프레임워크](references/korean-regulatory-framework.md), 해외 비교에는 [국제 규제 프레임워크](references/international-regulatory-framework.md)를 읽는다.
5. 용어 번역이 중요하면 [국·영문 용어집](references/terminology-ko-en.md)을 사용한다.

## 필수 분석 순서

- 연구질문과 범위
- 고객·가치·기초자산·발행·유통·보관·결제·수익·위험을 포함한 사업모델
- 해외 규제의 법적 상태와 운영 조건
- 한국 법률·하위법규·정책의 상태
- 관련 항목만 선별한 규제 격차
- 확인된 사실, 근거 있는 추론, 사업 기회, 실행 제약, 필요 조건, 추가 조사 사항
- 국문 심층 보고서와 요청 시 영문 Executive Summary

## 불변 규칙

- 법률안 발의, 국회 통과, 공포, 시행 예정, 현행 시행, 정책 발표, 입법예고, 행정해석을 구분한다.
- 각 핵심 주장에 Evidence ID를 붙이고 `VERIFIED_FACT`, `SUPPORTED_INFERENCE`, `UNVERIFIED`, `NEEDS_REVIEW` 중 하나로 표시한다.
- 법령은 관할권, 법령명, 관련 조문, 공포일, 시행일, 공식 URL, 조회일, 분석 기준일, 검증 상태를 기록한다.
- 정책 발표를 현행법으로, AI 해석을 기관 입장으로, 유사 용어를 동일 제도로 표현하지 않는다.
- 적법성을 확정하지 않는다. 근거가 부족하거나 원문을 확인하지 못하면 `추가 검토 필요`로 남긴다.
- 출처를 만들거나 추측하지 않는다. 2차 자료는 탐색용으로만 쓰고 주요 법적 주장은 1차 자료로 확인한다.

## 산출물

기본 형식은 [국문 보고서 템플릿](templates/research-report-ko.md)과 [영문 요약 템플릿](templates/executive-summary-en.md)이다. 구조화 데이터가 필요하면 `schemas/`를 따르고 다음 명령으로 점검한다.

```bash
python3 scripts/validate_sources.py evidence.json
python3 scripts/validate_report.py report.json
```

