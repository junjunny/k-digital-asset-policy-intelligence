# Phase 9 Human Review Data

이 폴더는 사람이 로컬 평가 화면에서 직접 입력한 기록만 저장한다.

- `reviews.json`: 현재 평가 상태와 최신 입력
- `revision-history.jsonl`: 저장할 때마다 누적되는 수정 이력
- `backups/`: UI에서 생성한 로컬 백업
- `finalized-analysis.json`: 120개 완료 후 명시적 확정 명령으로만 생성

서버는 git 명령을 실행하지 않는다. 진행 중 파일은 자동 commit·push되지 않으며, 최종 검토 후 사용자가 직접 반영한다. 자동 평가 결과와 이 폴더의 인간 평가는 합치지 않는다.
