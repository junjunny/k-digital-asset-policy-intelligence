# Chainlink 프로젝트 vs LINK 토큰 분석 (기준일 2026-11-18, STANDARD 깊이)

한국 규제와 직접 관련된 질문이 아니어서 한국 비교는 붙이지 않았습니다. 투자 판단은 제공하지 않으며, 구조와 위험만 다룹니다.

**확인 한계**
- Swift 보도자료는 접근이 거부되어(403) 원문을 읽지 못했습니다. 검색 요약으로만 확인했고 `UNVERIFIED`입니다.
- Chainlink 블로그(Reserve 발표), CCIP 문서 일부는 404이거나 리다이렉트되어 직접 읽지 못했습니다.
- DTCC 보도자료와 Chainlink 스테이킹·경제 페이지는 원문을 읽었습니다.
- 유통량과 Reserve 잔고는 날짜별로 수치가 달라서 단일 값을 확정하지 않았습니다.

## 1. 한 줄 결론

Chainlink는 **금융기관과 DeFi가 쓰는 오라클·메시징 인프라**입니다. LINK는 그 인프라의 **스테이킹·지급·보상 토큰**입니다. 기관이 인프라를 쓴다는 사실만으로는 LINK 수요가 생기지 않습니다. 수요는 기관이 쓰는 서비스의 요금이 LINK로 전환되는지에 달려 있습니다.

## 2. 프로젝트 층위

**오라클(데이터 피드 등)**
- 외부 데이터를 온체인으로 가져오는 탈중앙 노드망입니다. DeFi 가격 피드가 핵심 사용처입니다.
- 경쟁사 쪽 자료(Pyth 측 Blockworks 리서치)도 Chainlink가 TVS(보호 자산 가치) 기준으로 앞선다는 점은 부정하지 않습니다. 다만 거래량 기준으로는 Pyth가 앞선다고 주장합니다.
- 2차 자료에 따르면 DefiLlama 기준 Chainlink TVS는 약 $33~35B입니다. 날짜와 수치가 일관되지 않아 `NEEDS_REVIEW`입니다.

**CCIP(크로스체인 상호운용)**
- 토큰 이동과 메시지 전달을 위한 프로토콜입니다. Chainlink 측은 별도의 위험관리 네트워크를 포함한 다층 보안 모델을 내세웁니다. 이는 벤더 설명이며 독립 감사로 확인하지 못했습니다.
- 2026년 4월 KelpDAO 익스플로잇(약 $292M)은 LayerZero 검증자 설정과 관련된 사고였습니다. LayerZero 사후보고서와 KelpDAO의 주장이 엇갈립니다. 이후 일부 프로토콜이 CCIP로 이전했다는 보도가 있습니다. 이는 경쟁사의 사고에서 나온 반사 이익이지 CCIP 안전성의 검증이 아닙니다.
- 이번 조사에서 CCIP 자체의 사고나 제3자 감사 보고서는 찾지 못했습니다. "없다"가 아니라 "확인하지 못했다"입니다.

## 3. 채택 사례: 파일럿과 상용 구분

| 사례 | 상대 기관 자료가 말하는 것 | 단계 |
|---|---|---|
| **DTCC Collateral AppChain** (2026-05-12) | DTCC 원문: Chainlink Runtime Environment와 데이터 표준을 통합, 2026년 4분기 가동 "예정". 규제 승인 조건은 언급 없음. LINK·수수료 언급 없음 | 상용 가동 예정이며 **미확인**. 현재 시점(11월)에 실제 가동됐는지는 확인하지 못함 |
| **DTCC Smart NAV (2024)** | 펀드 NAV 데이터 온체인 전송 시험, 다수 자산운용사 참여 | 파일럿 |
| **Swift·UBS AM (2024-11-05)** | 토큰화 펀드 청약·환매를 Swift 네트워크로 결제. 정량 결과(속도·비용) 미공개 | 파일럿. Swift 원문은 읽지 못함 |
| **기업행위 이니셔티브 (24개 기관)** | 참여 기관 목록은 있으나 상용 운영 근거는 확인하지 못함 | 시험·이니셔티브 |
| **ANZ·ADDX (MAS Project Guardian)** | 토큰화 기업어음 생애주기 시험 | 규제 샌드박스 성격의 파일럿 |

DTCC 원문은 파일럿과 상용을 구분해 서술하지 않습니다. "상용 임박"이라는 표현은 Chainlink 공동창립자의 발언에서 나온 것입니다. 상대 기관이 "파트너십", "시험", "협력"이라고만 쓴 곳을 상용 채택으로 읽으면 안 됩니다.

## 4. LINK 토큰의 역할과 가치 포착

**공식 서술(chain.link 경제 페이지, 스테이킹 페이지)**
- 수수료는 법정화폐나 다른 자산으로도 낼 수 있습니다. 사용자에게 LINK 보유가 필수라는 서술은 없습니다.
- 받은 수익은 Payment Abstraction으로 DEX를 통해 LINK로 전환됩니다.
- 전환된 LINK는 Chainlink Reserve에 쌓입니다. Reserve는 2025-08-07 출시되었고 인출은 수년간 계획이 없으며 타임락이 있다고 합니다. 경제 페이지는 약 500만 LINK 보유로 표시합니다. 이 수치는 페이지 표시값이고 날짜가 불명확합니다.
- 스테이킹 v0.2: 캡 4,500만 LINK, 커뮤니티 보상 연 4.5% 하한 중 4%는 노드 위임 몫이라 실효 약 4.32%입니다. 슬래싱은 ETH/USD 피드 노드 운영자(3시간 이상 중단 시 700 LINK)에만 적용되고 커뮤니티 스테이커는 대상이 아닙니다. 이 수치는 2023년 말 기준 페이지이며 현재 풀 충전율은 확인하지 못했습니다.

**가치 포착의 연결고리와 약한 고리**
1. 기관·DeFi가 서비스를 쓴다.
2. 요금을 낸다. 이때 LINK로 내야 하는지는 서비스마다 다릅니다.
3. 요금의 일부가 LINK로 전환되어 Reserve에 쌓인다. 이 비율과 규모는 공식 자료에 없습니다.
4. 쌓인 LINK는 인출되지 않으므로 유통 공급을 줄이는 방향으로 작용합니다. 다만 Reserve가 유통량과 매도 압력에 미치는 순효과는 확인하지 못했습니다.

3단계가 핵심입니다. DTCC 원문에는 LINK나 수수료가 언급되지 않고, 회사 소개란에 일반 모델만 적혀 있습니다. **DTCC가 Chainlink 기술을 쓰더라도 DTCC가 LINK를 사거나 보유한다는 근거는 이 자료에 없습니다.** 이것이 채택과 토큰 수요를 동일시하면 안 되는 이유입니다. 기관 수익이 전환 대상에 포함되는지, 어느 비율인지가 별도 확인 사항입니다.

## 5. 공급

- 총공급 상한 1,000,000,000 LINK. Chainlink 유통량 페이지는 연 7% 릴리스 스케줄을 명시합니다. 이 7% 해석(연간 해제 상한인지 현재 스케줄인지)은 페이지 문구 그대로만 확인했습니다.
- 유통량은 소스마다 약 587M~748M로 갈립니다. 일부는 오래된 값입니다. 공식 페이지는 실시간 값 대신 "Retrieving"만 표시되어 확인하지 못했고, supply.chain.link API로 직접 확인해야 합니다.
- 비유통 지갑의 용도별 배분(노드 인센티브, Labs·재단 보유)은 공식 페이지에서 확인되지 않았습니다. 한 2차 자료는 Chainlink Labs 보유량을 약 273M으로 주장하지만 `UNVERIFIED`입니다.
- "민팅 없음"은 제3자 서술이며 Etherscan 컨트랙트 확인으로 검증하지 못했습니다.

## 6. 보안과 의존성

- **오라클 신뢰 모델**: 노드 운영자 집합과 스테이킹 슬래싱 범위가 제한적입니다(위 4항). 담보 규모 대비 경제적 보안이 충분한지는 별도 분석이 필요합니다.
- **CCIP**: 인프라 업그레이드 권한, 위험관리 네트워크 구성, 거버넌스 구조는 공식 문서를 직접 읽어 확인하지 못했습니다.
- **기관 의존성**: 기관 사례 다수가 Chainlink Labs와의 공동 발표입니다. Labs의 실행력과 서비스 계약에 대한 의존이 있고, 기관 쪽 규제 승인 조건은 DTCC 원문에 없습니다.
- **수익 공개**: 오프체인·기업 수익의 규모와 LINK 전환 비율이 공시되지 않았습니다. 토큰 가치 평가의 가장 큰 공백입니다.

## 7. 경쟁

- **오라클**: Pyth(거래량, 풀 모델), RedStone 등. 지표 선택(TVS vs 거래량)에 따라 우열이 달라지며 각 진영이 유리한 지표를 선택합니다.
- **크로스체인**: LayerZero, Wormhole, Axelar 등과 경쟁합니다. 이번 조사에서는 LayerZero 사고와 이전 보도만 확인했고, 다른 경쟁자의 공식 자료는 직접 보지 못했습니다.
- 기관 시장에서는 기관이 자체 구축하거나 다른 벤더를 쓸 가능성도 있어 독점적 우위로 보기 어렵습니다.

## 8. 요약 판단 틀

| 구분 | 확인된 것 | 확인 안 된 것 |
|---|---|---|
| 기술·채택 | 다수 기관 시험, DTCC 4Q26 가동 예정 | DTCC 실제 가동, 기관 사례의 상용 전환 규모 |
| 토큰 수요 | Payment Abstraction과 Reserve 구조 존재 | 전환 비율, 기관 수익의 LINK 전환 여부 |
| 공급 | 1B 상한, 연 7% 스케줄 | 현재 유통량, 비유통 배분, 민팅 불가 |
| 보안 | 스테이킹·슬래싱 설계 공개 | 슬래싱 범위 충분성, CCIP 독립 감사 |

**추가로 확인할 것**: supply.chain.link 값, reserve.chain.link 잔고와 유입 내역, Etherscan 컨트랙트(민팅 권한), Swift 보도자료 원문, DTCC 가동 공지, Chainlink 수익 공시.

Sources:
- [DTCC 보도자료 (2026-05)](https://www.dtcc.com/press-releases/2026/dtcc-collaborates-with-chainlink-to-advance-24-7-collateral-management)
- [Chainlink 스테이킹 v0.2](https://chain.link/economics/staking)
- [Chainlink 경제 페이지](https://chain.link/economics)
- [Chainlink 유통량 페이지](https://chain.link/circulating-supply)
- [Swift·UBS AM·Chainlink 보도자료](https://www.swift.com/news-events/press-releases/swift-ubs-asset-management-and-chainlink-successfully-complete-innovative-pilot-bridge-tokenized-assets-existing-payment-systems) (원문 미확인)
- [Chainlink Reserve 소개 (The Block 보도)](https://www.theblock.co/news/ecosystems/2025-08-07-chainlink-strategic-link-reserve-365988)
- [Kelp DAO·LayerZero 이전 보도 (The Block)](https://www.theblock.co/news/ecosystems/2026-05-05-kelp-dao-ditches-layerzero-chainlink-cross-chain-infrastructure-292-million-exploit-400131)
- [Cointelegraph: 오라클 TVS·거래량 비교](https://cointelegraph.com/news/oracle-providers-pyth-chainlink-volume-tvs-comparison)
- [Blockworks Research (Pyth Data Association 후원): TTV 논의](https://app.blockworksresearch.com/research/beyond-secured-value-how-ttv-best-reflects-oracle-fundamentals)

이 분석은 법률 자문이나 투자 권유가 아닙니다.
