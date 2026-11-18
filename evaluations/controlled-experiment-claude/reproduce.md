# Claude Code 코호트 — 재현·재개

이 코호트는 Codex 코호트(`../controlled-experiment/`)와 **합산·인과 비교하지 않는다**. 동결 프롬프트(`../controlled-experiment/prompts/`)·rubric·120슬롯 설계는 공유하고 모델·런타임만 Claude Code다.

## 확인된 런타임 (2026-11-18, 실제 실행으로 확인)

- Claude Code 2.1.318, `claude -p --output-format stream-json --verbose`(비대화형·구조화 출력), `--no-session-persistence`, `--effort`, `--allowedTools`, `--setting-sources`, `--json-schema`, `--max-budget-usd` 지원 확인(`claude --help`).
- 사용량: stream-json 최종 `result` 이벤트의 `usage`(input/output/cache_read/cache_creation)와 `modelUsage`. 구독 인증에서 `total_cost_usd`가 실제 청구액인지 미확인 → 비용은 N/A. 관측되지 않는 reasoning 토큰은 N/A.
- 웹 검색: 내장 `WebSearch`/`WebFetch`를 A~D 동일하게 허용.
- Skill 설치 경로: `npx skills add ... --agent claude-code` → 프로젝트 `./.claude/skills/<slug>` (원격 설치 실제 성공, SKILL.md SHA-256 `0f5115da…b2e9`, 로컬 HEAD와 일치, `results/claude-install.json`).
- 활성화 판정: `Skill` 도구 호출 또는 설치된 `SKILL.md` Read가 관측될 때만 CONFIRMED. 답변이 비슷한 것은 근거가 아니다. 명시 호출 진단은 본 120과 별도 cohort.

## 현재 상태: BLOCKED (AUTH_REQUIRED)

이 환경의 `claude -p`는 `OAuth session expired and could not be refreshed`/`Not logged in`으로 실패했다(`results/failure-log.jsonl`의 `clarity_act-C-01`). 생성된 답변은 0개이며 어떤 결과도 만들지 않았다.

## 재개 절차

1. 격리 홈에 각각 한 번 로그인한다(유료 API 키 불필요, 구독 로그인 사용):
   ```bash
   B=/tmp/kd_claude_env; mkdir -p $B/home-control $B/home-skill
   CLAUDE_CONFIG_DIR=$B/home-control claude /login
   CLAUDE_CONFIG_DIR=$B/home-skill claude /login
   ```
2. 워크디렉터리·원격 설치(A/B는 Skill 없음, C/D는 원격 npx 설치; 설치본의 과거 답변 폴더는 제거 후 로그 기록):
   ```bash
   export K_DARI_EXP_DIR="$PWD/evaluations/controlled-experiment-claude"
   python3 scripts/controlled_experiment.py setup-claude --base $B
   ```
3. 실행(순차, 새 독립 세션, 완료 슬롯은 건너뜀, 한도·인증 문제 시 `BLOCKED`로 저장하고 중단):
   ```bash
   python3 scripts/controlled_experiment.py run --all --runtime claude \
     --control-workdir $B/control --skill-workdir $B/skill \
     --control-home $B/home-control --skill-home $B/home-skill
   ```
   같은 명령을 다시 실행하면 `BLOCKED(AUTH_REQUIRED/USAGE_LIMIT)`·`RUNNING` 슬롯부터 이어서 진행한다. 결과가 마음에 들지 않는다는 이유의 재시도는 금지.
4. 완료 후 `blind` → 평가 → `aggregate`(둘 다 `K_DARI_EXP_DIR` 유지).

## 격리 점검 메모

- `CLAUDE_CONFIG_DIR`로 사용자 전역 스킬(약 135개)·플러그인·훅(예: ponytail)·메모리를 차단하고 `--setting-sources project`만 사용한다.
- A/B 작업폴더에 `.claude/`가 없음을 `setup-claude`가 기록한다. A/B에서 K-DARI 읽기가 관측되면 자동으로 `BLOCKED`(contaminated).
- 한계: 이 개발 세션 자체나 서브에이전트로 응답을 생성하면 도구·훅·전역 스킬이 달라 통제 실험이 아니므로 사용하지 않는다.
