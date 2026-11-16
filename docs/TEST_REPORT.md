# Test Report

실행일: 2026-11-16 (Asia/Seoul)

## 결과 요약

| 검증 | 결과 |
|---|---|
| Evidence JSON 구조·날짜·상태 | 통과: 6건 |
| Live URL 접근 | 통과: 6건 |
| Report 교차 참조·법적 상태 | 통과: Evidence 6건, Finding 6건 |
| Python unittest | 통과: 11건 |
| Skill Creator `quick_validate.py` | 통과 |
| JSON Schema 3종 메타스키마·사례 검증 | 통과 |
| Skills CLI 로컬 탐지 | 통과: 1개 스킬 |
| 격리된 임시 프로젝트 설치 | 통과: Codex project scope, copy mode |
| Python 문법 컴파일 | 통과 |
| 일반적 API 키·개인키 패턴 검색 | 발견 없음 |

## 실행 명령

```bash
python3 scripts/validate_sources.py examples/tokenization-case-study/evidence.json --check-urls --timeout 15
python3 scripts/validate_report.py examples/tokenization-case-study/report.json
python3 -m unittest discover -s tests -v
python3 -m py_compile scripts/validate_sources.py scripts/validate_report.py
npx skills add . --list
```

Skill Creator validator와 `jsonschema` 검증은 프로젝트 의존성을 늘리지 않기 위해 임시 가상환경에 `PyYAML`, `jsonschema`를 설치해 실행했다. 초기 실행에서는 호스트 Python에 PyYAML이 없어 validator가 시작되지 않았고, 임시 환경에서 재실행해 통과했다. JSON Schema의 `$id`는 오프라인 상대 참조가 가능하도록 파일명 기준으로 조정했다.

Skills CLI 설치는 `/tmp` 아래 격리 프로젝트에서 수행했고, `k-digital-asset-policy-intelligence`가 정상 복사 설치되는 것을 확인했다. 원격 GitHub URL을 이용한 fresh install은 push 전이므로 아직 검증하지 않았다.

## 자동 테스트 항목

- 필수 파일과 frontmatter
- schema JSON 구문
- 정상 사례 보고서
- Evidence 필드 누락·중복 ID
- 미래 시행 법률을 `IN_FORCE`로 표시하는 오류
- 근거 없는 `VERIFIED_FACT`
- 존재하지 않는 Evidence 참조
- 정책 발표로 현행법을 주장하는 오류
- 입법예고안으로 확정 규정을 주장하는 오류

## 수동 검토가 필요한 항목

- 법적 해석과 실제 인허가 적용
- 원문 발췌의 전체 문맥
- 2026-10 입법예고 이후 최종 하위법규
- 사례의 세무·회계·외국환·개인정보 이슈
- EIB 거래 계약서·법률의견서의 비공개 내용

