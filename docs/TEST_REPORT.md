# Test Report

실행일: 2026-11-16 (Asia/Seoul)

## 결과 요약

| 검증 | 결과 |
|---|---|
| Python unittest | 통과: 27건 |
| 부정 테스트 | 통과: 인용 불일치, 다른 문서, 404, 접근 제한, 오프라인, 시행 전 오인, 정책·입법예고 오인, 오래된 자료, 관할권 혼동, 근거 불일치, 사용자 오정보, 악의적 지시문 |
| EIB Evidence live content verification | 통과: 6/6 `CONTENT_VERIFIED` |
| 홍콩 신규 사례 live content verification | 통과: 6/6 `CONTENT_VERIFIED` |
| HTML 추출 | 통과 |
| PDF 추출 | 통과: 홍콩 SFC circular (`pypdf`) |
| Report validator | 통과: EIB 6 findings, 홍콩 7 findings |
| JSON Schema 3종과 사례 2건 | 통과 |
| Skill Creator `quick_validate.py` | 통과 |
| 원격 fresh clone | 통과: commit `9b29d56` |
| Skills CLI 탐지·격리 설치 | 통과: Codex project scope, copy mode |
| GitHub Actions CI | 통과: run `43820183166` |
| Python 문법 컴파일·CI YAML | 통과 |
| 일반적 API 키·개인키 패턴 검색 | 발견 없음 |

## 실행한 주요 명령

```bash
python3 -m py_compile scripts/*.py
python3 -m unittest discover -s tests -v
python3 scripts/validate_sources.py examples/tokenization-case-study/evidence.json
python3 scripts/validate_report.py examples/tokenization-case-study/report.json
python3 scripts/validate_sources.py examples/hong-kong-digital-green-bond/evidence.json
python3 scripts/validate_report.py examples/hong-kong-digital-green-bond/report.json
python3 scripts/verify_evidence.py examples/hong-kong-digital-green-bond/evidence.json --output /tmp/kdapi-hk-live-verification.json --timeout 25
python3 scripts/verify_evidence.py examples/tokenization-case-study/evidence.json --output /tmp/kdapi-eib-live-verification.json --timeout 25
npx skills add . --list
```

## Evidence 원문 검증

`verify_evidence.py`는 응답 코드·콘텐츠 유형·최종 URL·조회시각·문서 SHA-256·추출문 SHA-256을 기록하고, 정규화된 `relevant_excerpt`가 추출 원문에 포함되는지 확인했다.

실제 검증한 출처:

- EIB sterling digital bond 발표
- EUR-Lex Regulation (EU) 2022/858
- ESMA DLT Pilot Regime
- 국가법령정보센터 개정 전자증권법
- 금융위원회 2026-09 토큰증권 정책방향
- 금융위원회 2026-10 하위법규 입법예고
- HKMA 2024 multi-currency digital green bond 발표
- 홍콩 SFC tokenised securities circular PDF
- HKMA 2026 Tokenised Bond Expert Group 발표

같은 동적 웹페이지도 조회 시점에 HTML 전체 해시가 달라질 수 있다. 따라서 해시 변경만으로 의미 변경을 단정하지 않고 발췌문 일치·발행기관·날짜·법적 상태를 함께 본다.

## Fresh installation

GitHub 원격을 `/tmp/kdapi-fresh.ZWUF4g/repo`에 새로 clone하고 별도 venv에 의존성을 설치했다. 27개 테스트와 홍콩 보고서 검증을 통과한 뒤, Skills CLI가 1개 스킬을 탐지했고 `/tmp` 격리 프로젝트의 `.agents/skills/k-digital-asset-policy-intelligence`에 copy mode로 설치했다. 설치본에 대해 Skill Creator validator와 사례 파일 존재를 확인했다.

## 자연어 리서치 E2E

Phase 5의 실제 자연어 요구를 기준으로 기존 EIB 문서를 복제하지 않고 홍콩 다중통화 디지털 녹색채권을 새로 조사했다. 범위 정의, 공식 검색, 해외 모델·규제, 한국 법률·정책, Evidence v2, 국문 보고서, 영문 요약, 자동 검증과 한계 표기를 완료했다. `tests/test_e2e_workflow.py`는 이 산출물과 Evidence 상태를 재검증한다.

다만 별도의 두 번째 LLM 인스턴스를 실행해 동일 자연어 요청을 blind evaluation한 것은 아니다. fresh installation은 스킬 인식·설치·결정적 검증까지 확인했고, 자연어 분석 품질은 이 Phase의 실제 수행 결과로 확인했다.

## 자동 검증할 수 없는 부분

- 인용문의 법률적 의미와 전체 문맥
- 비공개 계약서·법률의견서
- 개별 사업의 최종 인허가·세무·회계·외국환 적법성
- 스캔 PDF OCR, 복잡한 표·각주
- 기존 방식 대비 실제 비용·시간 절감과 사업 수익성
- 향후 공포될 한국 하위법규의 최종 내용

이 항목은 검증 완료로 표시하지 않고 보고서 한계 또는 `NEEDS_REVIEW`로 남겼다.

