# Post-fix Usability Results

기준일: 2026-11-17. 수정 전 실제 결과와 독립 평가 의견은 `skill-evaluation-before-fix.md`에 보존했다.

| 질문 | 수정 후 주 유형 | 보조·행동 | 판정 |
|---|---|---|---|
| 토큰증권이 뭐야? | `CONCEPT_EXPLANATION` | `TOKENIZED_ASSET_OR_RWA`, `QUICK` | 통과 |
| 한국에서 토큰증권 지금 발행할 수 있어? | `TOKENIZED_ASSET_OR_RWA` | `LAW_AND_REGULATION`, 최신 검증 | 통과 |
| 이 코인 어떤 거야? | `AMBIGUOUS_REQUEST` | 이름·티커·네트워크 확인 | 통과 |
| 이 코인 사도 돼? | `INVESTMENT_OR_PRICE_REQUEST` | 추천 대신 위험검토, 대상 확인 | 통과 |
| 솔라나 백서 검토해 줘. | `WHITEPAPER_REVIEW` | 불필요한 대상 재질문 없음 | 통과 |
| 업비트에서 거래되는 솔라나 네트워크 평가 | `NETWORK_OR_PROTOCOL_REVIEW` | 한국 맥락 신호만 유지 | 통과 |
| USDC 관련 미국 법률 설명 | `LAW_AND_REGULATION` | `STABLECOIN_REVIEW` | 통과 |
| 클래리티법 알려줘. | `LAW_AND_REGULATION` | `QUICK`, 최신 검증 | 통과 |
| 한국에서 이더리움과 솔라나 차이 | `NETWORK_OR_PROTOCOL_REVIEW` | 규제 비교 강제 없음 | 통과 |
| CLARITY Act와 한국 규제 비교 | `REGULATORY_COMPARISON` | 한국 맥락·최신 검증 | 통과 |

평가에 사용하지 않은 holdout인 “미국 클래러티 법안 핵심 알려줘”, “업비트 솔라나 네트워크 장단점”, “미국 스테이블 코인 규제법을 핵심만 설명해줘”도 각각 법률, 네트워크, 법률 유형으로 통과했다.

이 결과는 결정적 분류 검증이며 실제 답변의 사실 정확성을 증명하지 않는다. 라우터 출력과 대화 문맥이 충돌하면 에이전트가 문맥을 우선하고 변경 이유를 평가 로그에 남긴다.

