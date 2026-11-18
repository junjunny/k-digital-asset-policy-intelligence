# CLAUDE.md

이 저장소의 작업 규칙은 `AGENTS.md`가 유일한 기준이다. 세션 시작·종료 절차와 품질 규칙은 그 파일을 따르고 여기에 복제하지 않는다.

Claude Code 전용 사항만 둔다.

- Phase 9 통제 실험은 코호트별로 분리한다. Codex 코호트는 `evaluations/controlled-experiment/`(보존, 수정 금지), Claude 코호트는 `evaluations/controlled-experiment-claude/`다. 실행·재개 명령은 `evaluations/controlled-experiment-claude/reproduce.md`.
- 실험 응답 생성은 반드시 격리된 `claude -p` 새 세션으로만 한다. 현재 대화(이 세션)나 서브에이전트로 대신 생성하지 않는다. 실행하지 못했으면 결과를 만들지 않는다.
- 인증·사용량 한도로 막히면 `BLOCKED`로 남기고 재개 명령을 안내한다. 한도를 우회하거나 로그인 자격증명을 다루지 않는다.
- 전체 테스트: `python3 -m unittest discover -s tests`
