# Handoff

## 다음 시작점

1. `git status`, `docs/TEST_REPORT.md`, `docs/INDEPENDENT_EVALUATION.md`를 확인한다.
2. 사용자는 `docs/PHASE_8_HUMAN_REVIEW.md`에서 A/B 답변과 주요 주장을 직접 검토한다.
3. CLARITY 공식 입법기록, Chainlink 동적 지표, Ethereum 대시보드 방법론, USDC 주간 수치를 재확인한다.
4. Phase 8 승인과 Phase 9 착수 여부를 사용자가 별도로 결정한다.
5. 기존 EIB·홍콩 사례 검토는 `HUMAN_REVIEW_GUIDE.md`와 `ANALYST_REVIEW.md`를 계속 사용한다.

## 사용자 작업

- MIT License의 저작권자 표기 확인
- 실제 포트폴리오 제출 전 사례의 전문가 검토
- 최종 하위법규 공포 후 규제 상태·수치 재검증
- `OPEN_QUESTIONS.md`의 평가 관련 항목 결정
- Phase 8 인간 채점표 작성 및 승인 여부 결정
- Phase 9 Corporate 리서치 포트폴리오의 대상 기관·산업 범위 승인

## 주의

2026-10-01 금융위원회 자료는 입법예고다. 예고 내용의 숫자와 요건을 확정 규정으로 바꾸지 않는다. EIB sterling bond는 EU DLT Pilot 적용 전 발행이다.

`CONTENT_VERIFIED`는 원격 원문 접근과 발췌문 일치를 뜻하며 출처의 실질적 진위, 법률 해석, 주장의 의미상 충분성, 사업 적법성을 검증했다는 의미가 아니다. 수동 첨부는 발췌가 일치해도 공식 출처 확인 완료로 처리하지 않는다. validator의 claim/Evidence 호환성도 구조 검사일 뿐 의미 증명이 아니다.

Phase 8에서 자연어 입력부터 최신 공식자료 탐색과 답변 생성까지 네 사례를 독립 실행했다. 다만 각 A/B는 1회 표본이고 구체 모델 설정·토큰·실행시간은 노출되지 않았다. 모델 보조점수는 인간 승인이나 전문가 법률·회계·기술 검토가 아니다. 라우터 통과, 설치 성공, Evidence 발췌 일치도 실제 리서치 정확성과 각각 구분한다. skills.sh 등록·릴리스·홍보는 계속 제외한다.

프로젝트는 Phase 10에서 신규 기능 개발을 종료한다. Phase 9는 자동으로 시작하지 않는다.



## Phase 9 재개 (Claude Code)

1. 사용자가 터미널에서 `CLAUDE_CONFIG_DIR=/tmp/kd_claude_env/home-control claude /login` 및 `home-skill`에 각각 로그인한다(자격증명은 Claude가 다루지 않음).
2. `evaluations/controlled-experiment-claude/reproduce.md`의 setup/run 명령을 실행한다. 한도에 닿으면 자동 중단·BLOCKED 저장되며 같은 명령으로 재개한다.
3. 이후 blind 평가, 공식 근거 대조, aggregate. Codex 코호트와 합산하지 않는다. Phase 10은 별도 승인 전 시작하지 않는다.
