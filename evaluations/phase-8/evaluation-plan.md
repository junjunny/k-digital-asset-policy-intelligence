# Evaluation Plan

## 고정 기준선

- Git commit: `ba7734ed6e6b3b0483313d0564b12374b1d273f4`
- 설치 소스: GitHub `junjunny/k-digital-asset-policy-intelligence`
- 실행일: 2026-11-17 (Asia/Seoul)
- Agent: Codex 독립 서브에이전트 세션
- 모델: 현재 Codex 세션에서 상속한 동일 모델. 구체적인 API 모델 식별자와 샘플링 설정은 실행 환경에서 노출되지 않아 기록 불가
- 웹 검색: 가능
- 파일 접근: A그룹은 K-DAPI 미사용, B그룹은 격리 소비자 프로젝트의 설치본만 지시로 제공
- 스크립트 접근: B그룹은 설치본 스크립트 사용 가능, A그룹은 프로젝트 스크립트 미사용
- fresh clone: `/tmp` 격리 디렉터리에서 기준선 SHA 일치 확인(공개 산출물에는 절대 경로를 기록하지 않음)
- 실제 설치 명령: `npx --yes skills add junjunny/k-digital-asset-policy-intelligence@k-digital-asset-policy-intelligence --agent codex --copy -y`
- 설치 결과: 소비자 프로젝트의 `.agents/skills/k-digital-asset-policy-intelligence`에 copy mode 설치 성공
- 평가 시작 시각: 2026-11-17 16시대 KST. 각 답변의 상세 검색 시각은 사례 원문에 기록

## 비교 설계

- Group A: K-DAPI 미설치·미사용, 별도 K-DAPI 지침 없음
- Group B: 같은 모델 계열·같은 질문·같은 웹 조건, fresh clone에서 Skills CLI로 설치한 K-DAPI 명시 호출
- 각 필수 사례는 새로운 A/B 에이전트 세션에서 실행
- 개발 프롬프트, 기존 사례 결론, 평가 정답과 점수를 제공하지 않음
- 실제 답변, 공식 출처, 검색 시각, 한계와 실행 불가 항목을 보존

자동 암묵 활성화는 현재 서브에이전트 실행 환경에서 관측 가능한 UI 이벤트가 없으므로 완료로 주장하지 않는다. 명시적 설치본 경로 제공과 `$k-digital-asset-policy-intelligence` 사용은 별도로 검증한다.

## 질문 목록

1. 미국 CLARITY Act와 한국 규제·국내 금융회사·거래소 의미
2. Chainlink·LINK의 실제 사용, 토큰 필요성, 장점과 위험
3. Ethereum 네트워크의 구조, 장단점과 경쟁 네트워크 차이
4. USDC의 페그, 준비자산, 위험과 한국 이용자 유의점
5. 일반 사용자 질문 10개
6. 다중 턴 대화 3개
7. 오프라인 최신 법안 상태 질문

## 변경 통제

평가 실패가 관찰된 경우에만 최소 수정한다. 실패 질문은 삭제하지 않고 `failure-log.md`에 남긴다. 수정 후에는 기존 질문과 별도 holdout 질문으로 재검증한다.

