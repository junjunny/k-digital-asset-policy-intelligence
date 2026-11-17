# Test Report

실행일: 2026-11-17 (Asia/Seoul)

## 결과 요약

| 검증 | 결과 |
|---|---|
| Python unittest | 통과: 54건 |
| Phase 7 질문 라우터 | 통과: 17건 — 12개 유형, 응답 깊이, 모호성, 한국 맥락, 투자안전 |
| 부정 테스트 | 통과: 인용 불일치, 다른 문서, 404, 접근 제한, 오프라인, 시행 전 오인, 정책·입법예고 오인, 오래된 자료, 관할권 혼동, 근거 불일치, 사용자 오정보, 악의적 지시문 |
| EIB 저장 Evidence | 통과: 6/6 `CONTENT_VERIFIED`; 최신 live 재조회는 아래 제한 참조 |
| 홍콩 신규 사례 live content verification | 통과: 6/6 `CONTENT_VERIFIED` |
| HTML 추출 | 통과 |
| PDF 추출 | 통과: 홍콩 SFC circular (`pypdf`) |
| Report validator | 통과: EIB 6 findings, 홍콩 7 findings |
| JSON Schema 3종과 사례 2건 | 통과 |
| Skill Creator `quick_validate.py` | 통과 |
| 원격 fresh clone | 통과: commit `9b29d56` |
| Skills CLI 탐지·격리 설치 | 통과: Codex project scope, copy mode |
| GitHub Actions CI | 통과: Phase 6 run `43823538012` (`2305f3d`) |
| Python 문법 컴파일·CI YAML | 통과 |
| 일반적 API 키·개인키 패턴 검색 | 발견 없음 |
| 수동 첨부 진위 분리 | 통과: 발췌 일치 시에도 `MANUAL_REVIEW_REQUIRED` |
| URL·파일 입력 보안 | 통과: localhost, 사설·loopback·link-local, 자격증명, HTTPS downgrade, 리다이렉트 재검증, 디렉터리 탈출 차단 |
| 의미 검토 경계 | 통과: 구조적 claim/Evidence 호환성이 의미 증명이 아니라는 경고 출력 |
| Phase 6 격리 validator | 통과: 임시 venv에서 Skill Creator, Evidence 12건·Report 2건 JSON Schema 검증 |
| Skills CLI 탐지 | 통과: 범용 자연어 설명으로 스킬 1개 탐지 |
| Phase 7 로컬 Skill Creator·Skills CLI | 통과: 새 라우터·네트워크 설명 포함 스킬 1개 탐지 |
| Phase 7 원격 fresh clone·격리 설치 | 통과: commit `9e8f1ab`, copy mode, 설치본 라우터·Skill Creator 검증 |
| Phase 7 GitHub Actions CI | 통과: run `44027593383` (`9e8f1ab`) |

## 실행한 주요 명령

```bash
python3 -m py_compile scripts/*.py
python3 -m unittest discover -s tests -v
python3 scripts/route_question.py "CLARITY Act가 뭐야?"
python3 scripts/route_question.py "이 코인 어떤 거야?"
python3 scripts/validate_sources.py examples/tokenization-case-study/evidence.json
python3 scripts/validate_report.py examples/tokenization-case-study/report.json
python3 scripts/validate_sources.py examples/hong-kong-digital-green-bond/evidence.json
python3 scripts/validate_report.py examples/hong-kong-digital-green-bond/report.json
python3 scripts/verify_evidence.py examples/hong-kong-digital-green-bond/evidence.json --output /tmp/kdapi-hk-live-verification.json --timeout 25
python3 scripts/verify_evidence.py examples/tokenization-case-study/evidence.json --output /tmp/kdapi-eib-live-verification.json --timeout 25
npx skills add . --list
```

## Phase 7 라우터 검증

- CLARITY Act 질문은 `LAW_AND_REGULATION`, 한국 규제 비교는 `REGULATORY_COMPARISON`
- 토큰증권의 간단한 정의는 `CONCEPT_EXPLANATION` + `TOKENIZED_ASSET_OR_RWA`
- 이더리움은 네트워크 평가, USDC는 스테이블코인 평가로 분리
- 대상 없는 코인·네트워크는 `AMBIGUOUS_REQUEST`와 확인 질문
- 백서는 공식 URL·파일·프로젝트명을 요청하되 백서 프레임워크 유지
- 투자 요청은 `INVESTMENT_OR_PRICE_REQUEST`로 분류하고 추천 대신 위험 검토로 전환
- 해외 네트워크 질문에는 한국 맥락을 자동 추가하지 않음
- 단순 질문에는 `DEEP_RESEARCH`를 강제하지 않음

라우터는 질문의 방법론을 선택할 뿐 실제 법안 상태, 프로젝트 안전성, 네트워크 품질을 증명하지 않는다. 이 부분은 Phase 8의 독립 리서치 대상이다.

## Phase 7 fresh installation

GitHub 원격을 `/tmp/kdapi-phase7-fresh-20261117/repo`에 새로 clone하고 별도 venv에 의존성을 설치했다. 54개 테스트, CLARITY Act 라우팅, Skill Creator 검증과 Skills CLI 탐지를 통과했다. 별도 git 프로젝트인 `/tmp/kdapi-phase7-fresh-20261117/consumer`에 copy mode로 설치하고, 설치본의 실행 권한·`SKILL.md`·모호한 코인 확인 질문·Skill Creator 검증을 확인했다.

PDF나 외부 API 키 없이 질문 라우팅은 시작할 수 있다. 다만 실제 최신 법률·프로젝트·네트워크 분석에는 웹 검색 또는 사용자가 제공한 공식 원문이 필요하며, 이것은 이번 Phase에서 독립 수행하지 않았다.

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

## 저장된 연구 산출물 회귀검증

Phase 5의 실제 자연어 요구를 기준으로 홍콩 다중통화 디지털 녹색채권을 조사했고, `tests/test_e2e_workflow.py`는 커밋된 산출물과 Evidence 상태를 재검증한다. 테스트 클래스는 실제 범위를 반영해 `StoredResearchArtifactTests`로 명명했다.

별도 에이전트가 격리 설치본에서 처음 보는 자연어 입력을 받아 출처 탐색부터 보고서 생성까지 실행한 blind E2E는 아니다. 이 독립 평가는 `docs/PHASE_7_TEST_PLAN.md`에만 설계했으며 사용자 승인 전 실행하지 않는다.

## Phase 6 live 확인

- 홍콩 사례: 6/6 `CONTENT_VERIFIED`
- EIB 사례: 5/6 `CONTENT_VERIFIED`; EUR-Lex가 HTTP 200의 AWS WAF challenge를 반환하여 `ACCESS_RESTRICTED`

EUR-Lex 결과는 발췌 불일치로 잘못 분류하지 않고 접근 제한으로 처리하도록 검증기를 보완했다. 저장된 이전 원문 해시·발췌 기록은 삭제하지 않았지만, 이번 조회에서 원문을 재확인하지 못했으므로 사람이 브라우저에서 직접 확인해야 한다.

## 자동 검증할 수 없는 부분

- 인용문의 법률적 의미와 전체 문맥
- 비공개 계약서·법률의견서
- 개별 사업의 최종 인허가·세무·회계·외국환 적법성
- 스캔 PDF OCR, 복잡한 표·각주
- 기존 방식 대비 실제 비용·시간 절감과 사업 수익성
- 향후 공포될 한국 하위법규의 최종 내용

이 항목은 검증 완료로 표시하지 않고 보고서 한계 또는 `NEEDS_REVIEW`로 남겼다.

