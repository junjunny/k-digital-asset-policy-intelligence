# Phase 9 — K-DARI Controlled Evaluation & Portfolio Validation

## 범위

Phase 9는 공개 명칭을 K-DARI로 정리하면서 기존 설치 슬러그와 저장소 주소를 보존하고, 6개 주제·4개 조건·5회 반복의 120개 통제 실험을 실행한다. 외부 네이버 사례 E군, 포트폴리오 문서, 자동 보조평가와 인간 검토를 서로 분리한다.

## 상태

| 구성요소 | 상태 |
|---|---|
| K-DARI 공개명·기존 슬러그 호환 | COMPLETE |
| 프로토콜·프롬프트·rubric·manifest 동결 | COMPLETE |
| GitHub 원격 fresh install | COMPLETE |
| 120개 생성 실행 | IN_PROGRESS |
| condition-blind 자동 근거 검증·평가 | PENDING |
| 결과 집계·통계 | PENDING |
| 네이버 외부 E군 공식 근거 대조 | PARTIAL |
| Corporate 포트폴리오 | PENDING |
| 인간 검토 | HUMAN_REVIEW_PENDING |

실험 완료 전에는 “120개 비교 검증 완료”라고 표현하지 않는다. Phase 10은 사용자 별도 승인 전 시작하지 않는다.

## 격리 문제와 조치

초기 파일럿에서 사용자 전역에 설치된 스킬이 대조군에 유입될 수 있음을 실제 로그로 발견했다. 해당 시도는 삭제하지 않고 `GLOBAL_SKILL_CONTAMINATION_OR_PRE_ISOLATION_PILOT`로 분석 제외했다. 이후 조건별 임시 `HOME`·`CODEX_HOME`과 작업 디렉터리를 분리하고, 대조군에 스킬 읽기가 관측되면 자동으로 `BLOCKED` 처리하도록 수정했다.
