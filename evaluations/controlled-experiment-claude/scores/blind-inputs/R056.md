자료 수집은 끝났고, 지금부터 정리해서 답변합니다. 확인하지 못한 부분은 그렇게 표시했습니다.

# Chainlink(프로젝트)와 LINK(토큰) 분석

기준일은 2026-11-18입니다. 공식 자료는 Chainlink 자체 자료와 상대방 기관 자료로 나눠 적었습니다. 별도 표시가 없는 수치는 Chainlink가 직접 발표한 것입니다.

## 1. 결론

- **프로젝트 채택은 강한 편입니다.** 오라클 시장 점유율이 높고, DTCC·Swift 같은 기관과 협업이 이어지고 있습니다.
- **LINK 수요로 이어지는 경로는 간접적이고 대부분 검증이 덜 됐습니다.** 상대방 기관 자료에는 LINK나 수수료 구조 언급이 없습니다.
- 가장 직접적인 토큰 수요는 스테이킹과 Chainlink Reserve입니다. 이 둘은 규모가 제한적입니다.

## 2. 프로젝트: 무엇을 하는가

**오라클(Data Feeds 등)**
- 외부 데이터를 온체인에 공급합니다. 점유율은 출처마다 달라서 하나의 값으로 적기 어렵습니다.
  - DefiLlama 스냅샷(날짜 미확인): Chainlink 약 $35.8B, RedStone 약 $3.9B, Pyth 약 $3.2B.
  - 2차 출처: 63~84%. 기준일과 방식이 제각각입니다.
- Messari는 TVS(보호 자산 규모)가 시장 점유율을 왜곡한다고 지적합니다. 거래 가치(TTV) 기준이 더 낫다는 입장입니다.
- Pyth는 거래 활동과 파생상품 분야에서 앞선다는 보도가 있습니다. Chainlink는 대출 분야 TVS에서 앞선다고 합니다.

**CCIP(크로스체인 상호운용)**
- Chainlink 발표로는 누적 크로스체인 토큰 가치가 $850억 이상, EVM 레인이 1,040개 이상입니다. "가치"의 산정 방식은 정의돼 있지 않습니다.
- 올해 기존 브리지에서 CCIP로 옮겨온 가치가 $150억 이상이라고 합니다. BitGo의 WBTC $77억 이상 이전이 대표 사례입니다. 이 숫자도 Chainlink 요약입니다.
- LayerZero·Wormhole와의 정량 비교 자료는 찾지 못했습니다.

**CRE(Runtime Environment)와 데이터 표준**
- 여러 서비스를 엮는 워크플로 계층입니다. 기관 협업은 주로 이 계층을 중심으로 발표됩니다.

## 3. 실제 활용 사례: 파일럿과 상용 운영 구분

| 사례 | 상대방 자료가 말하는 것 | 단계 |
|---|---|---|
| Swift 2023 실험 | Swift는 Chainlink를 Swift 네트워크와 Ethereum Sepolia를 잇는 중간 계층으로 썼다고 밝혔습니다. 모의 토큰 자산 전송이었고, DTCC가 테스트용 BondToken을 발행했습니다. 관련 기술 보고서를 인용한 것입니다. | **실험(테스트넷)** |
| Swift·UBS AM·Chainlink 2024 | 토큰화 펀드 청약·환매를 Swift 네트워크로 처리했습니다. 결제는 오프체인에서 이뤄졌습니다. Swift 보도자료 제목이 "pilot"입니다. | **파일럿** |
| 기업 이벤트(corporate actions) 2025 | Swift는 "proof of concept"라고 표현했습니다. Euroclear 독립 보도자료는 찾지 못했고, Chainlink 임원 발언을 인용한 Euroclear 기사만 확인했습니다. "거의 100% 합의"는 Chainlink가 보고한 수치입니다. | **개념 증명** |
| DTCC Collateral AppChain (2026-05-12) | 보도자료는 상용·파일럿 여부를 명시하지 않았습니다. 2026년 4분기 출시 예정이고, 문구는 "will leverage", "is expected to" 같은 미래형입니다. Chainlink 공동창업자도 "프로덕션에 가까워지는 중"이라고 말했습니다. 오늘 기준 출시 여부는 확인하지 못했습니다. | **출시 전** |
| 크립토 네이티브(BitGo WBTC, Coinbase 토큰화 주식, Wyoming FRNT 등) | 상당 부분 Chainlink 요약에 의존합니다. 일부는 파트너 발표입니다. | **상용 운영으로 보이나 개별 확인 필요** |

핵심은 이렇습니다. 전통금융 사례는 대부분 실험이나 출시 전이고, 상용 운영에 가까운 쪽은 크립토 네이티브 영역입니다.

## 4. 토큰: LINK의 역할과 가치 포착

**공식 설계상의 역할**
- 노드 운영자에게 보상을 주고 담보로 쓰이는 토큰입니다. 스테이킹 v0.2의 담보이기도 합니다.

**스테이킹 v0.2 (공식 staking 페이지)**
- 총 한도는 45,000,000 LINK입니다. 커뮤니티 풀은 40,875,000 LINK입니다.
- 기본 보상은 연 4.5%이고, 노드 운영자 위임 보상을 뺀 실질 4.32%입니다. 가변 보상입니다.
- 언스테이킹은 28일 쿨다운 뒤 7일 청구 기간입니다.
- 슬래싱은 노드 운영자만 대상입니다. 출시 시점에 ETH/USD 피드 운영자는 유효한 경고 한 건당 700 LINK를 잃습니다. 커뮤니티 스테이커는 대상이 아닙니다.
- 한도가 약 4,500만 LINK라서, 스테이킹으로 잠기는 물량에는 상한이 있습니다.

**Chainlink Reserve**
- 오프체인·온체인 수익을 Payment Abstraction으로 LINK로 환전해 쌓는 이더리움 컨트랙트입니다. 환전에는 Uniswap V3 등 DEX 인프라를 쓰는 것으로 보입니다. 출금 전 몇 일간의 타임락이 있고, 몇 년간 출금 계획이 없다고 합니다.
- 2026 Q3 말 보유량은 6,047,498 LINK입니다(Q3 증가분 1,543,330 LINK). 실시간 값은 reserve.chain.link에서 확인할 수 있습니다.
- 스테이킹 기반 SVR 수수료의 50%가 Reserve로 돌아가도록 계획돼 있습니다.
- 공식 글에 소각 언급은 없어서, 소각이 아니라 비축으로 이해하는 것이 맞습니다. 매입한 LINK는 시중에서 빠질 뿐 공급량이 줄지는 않습니다.

**가치 포착의 한계**
- 고객이 달러나 다른 자산으로 결제하면, 그 수익이 LINK 수요로 이어지는 구간은 Reserve 환전뿐입니다.
- 기관 파일럿에서 LINK가 쓰인다는 상대방 자료는 확인하지 못했습니다. DTCC 보도자료에도 LINK나 수수료 언급이 없었습니다.
- Chainlink 자체 Q3 자료에는 Reserve 규모와 ETF 보유량이 나옵니다. ETF(Grayscale GLNK, Bitwise CLNK)는 합계 16,650,795 LINK, 시가총액의 2.24%라고 합니다. 이는 투자 수요이지 네트워크 사용 수요가 아닙니다.
- Reserve 6.0M LINK와 스테이킹 한도 45M LINK를 합쳐도 총공급량에서 차지하는 비중은 크지 않습니다. 정확한 비율에는 현재 유통량 확인이 필요합니다.

## 5. 공급

- 총 공급은 10억 LINK로 알려져 있습니다. 이 값은 이번 조사에서 공식 페이지로 확인하지 못했고, 기억에 근거한 서술입니다.
- 현재 유통량과 노드 운영자·개발 측 보유분의 잠금·해제 일정은 이번에 확인하지 못했습니다. 공식 circulating supply 페이지에서 직접 확인하길 권합니다.
- Chainlink 경제 페이지 URL(`chain.link/economics/link-token`)은 404였습니다. 그래서 토큰 경제 항목은 이번에 공식 원문으로 검증하지 못했습니다.

## 6. 보안

- 보안 모델은 스테이킹 담보와 슬래싱, 그리고 CCIP의 별도 위험 관리 계층으로 구성됩니다. CCIP 구조 문서는 이번에 열람하지 못했습니다(404).
- v0.2의 커뮤니티 스테이킹은 슬래싱 위험이 없습니다. 이는 위험이 낮다는 뜻이지만, 동시에 커뮤니티 스테이킹이 오라클 오류에 대한 경제적 담보 역할을 하지 않는다는 뜻이기도 합니다.
- 슬래싱 700 LINK는 출시 기준 수치입니다. 피드가 보호하는 가치와 비교하면 작고, 더 큰 담보 설계(v0.3)는 설계 단계라는 2차 출처 설명이 있지만 공식 확인은 못 했습니다.

## 7. 의존성

- **데이터·인프라:** 노드 운영자 집단과 거래소 등 외부 데이터 소스에 의존합니다.
- **기관 프로젝트:** DTCC·Swift 모두 자체 일정과 규제 조건에 달려 있습니다. DTCC 보도자료에는 위험이나 재무 조건 언급이 없습니다.
- **Swift의 별도 행보:** Swift는 자체 블록체인 원장(17개 은행, 토큰화 예금)을 발표했습니다. Chainlink 사용 여부는 해당 자료에서 확인하지 못했습니다. 이 점은 장기적으로 기관 채널이 Chainlink를 필수로 쓰지 않을 수 있다는 신호일 수 있습니다.
- **자체 수치:** TVE $36조 이상, CCIP $850억 이상 등은 정의가 공개되지 않은 자체 지표입니다. 다른 업체와 직접 비교할 수 없습니다.

## 8. 경쟁

- **오라클:** Pyth(저지연·파생상품), RedStone(LST/LRT 가격), Chronicle, API3 등이 있습니다. 점유율은 Chainlink가 앞서지만, 활동량 기준으로는 Pyth가 앞선다는 보도가 있습니다.
- **크로스체인:** LayerZero, Wormhole와의 점유율 비교는 이번에 확인하지 못했습니다.
- **기관 시장:** Swift 자체 원장, Canton 등 다른 기관용 인프라와도 경쟁하거나 병행합니다. 이 부분은 이번에 조사하지 않았습니다.

## 9. 채택과 토큰 수요를 구분하는 체크리스트

1. 협업 발표인가, 상용 운영인가?
2. 수수료는 누가 어떤 자산으로 내는가? LINK인가, 달러인가?
3. 그 수익이 Reserve로 가는가? 가는 비율은 얼마인가?
4. 스테이킹은 한도가 차 있는가? 보상률은 어떻게 변하는가?
5. 수요가 ETF나 거래소 상장 같은 투자 수요가 아닌가?

현재 근거로는 1번의 일부(크립토 네이티브)와 3번의 일부(Reserve 증가)만 확인됩니다. 기관 협업과 LINK 수요의 연결은 아직 입증되지 않았습니다.

## 10. 한계

- 공식 Chainlink 경제·CCIP 문서 일부(404)와 Swift 보도자료 원문(403)은 열람하지 못했고, 검색 요약에 의존했습니다.
- Euroclear 독립 공식 발표는 찾지 못했습니다.
- 유통량, 총공급 잠금 일정, 시가총액 대비 Reserve 비율은 확인하지 못했습니다.
- 투자 판단이 아니라 정보 정리입니다.

Sources:
- [DTCC: Chainlink 24/7 담보 관리 (2026-05-12)](https://www.dtcc.com/news/2026/may/12/dtcc-collaborates-with-chainlink-to-advance-24-7-collateral-management)
- [DTCC: Collateral AppChain 실험에서 프로덕션으로](https://www.dtcc.com/dtcc-connection/articles/2026/may/15/the-dtcc-collateral-appchain-from-experiment-to-production-infrastructure)
- [Swift: 블록체인 실험 보도자료 (2023)](https://www.swift.com/news-events/press-releases/swift-unlocks-potential-tokenisation-successful-blockchain-experiments)
- [Swift·UBS AM·Chainlink 파일럿](https://www.swift.com/news-events/migrated-news/press-releases/swift-ubs-asset-management-and-chainlink-successfully-complete-innovative-pilot-bridge-tokenized-assets-existing-payment-systems)
- [Swift: 기업 이벤트 현대화](https://www.swift.com/insights/news/modernising-corporate-actions-through-technology-and-collaboration)
- [Euroclear: 펀드 업계 기술 기사](https://www.euroclear.com/newsandinsights/en/Format/Articles/how-technology-is-reshaping-the-funds-world.html)
- [Chainlink: Q3 2026 분기 리뷰](https://chain.link/blog/quarterly-review-q3-2026)
- [Chainlink: Reserve 소개](https://chain.link/blog/chainlink-reserve-strategic-link-reserve)
- [Chainlink: 스테이킹 v0.2](https://chain.link/economics/staking)
- [Chainlink 블로그: 은행·자본시장 협업](https://blog.chain.link/chainlink-banking-capital-markets-announcements/)
- [CoinDesk: 기업 이벤트 이니셔티브](https://www.coindesk.com/business/2025/09/29/chainlink-teams-with-major-financial-institutions-to-fix-usd58b-corporate-actions-problem)
- [DefiLlama Oracles](https://defillama.com/oracles?staking=false)
- [Messari: TTV 보고서](https://messari.io/report/beyond-secured-value-how-ttv-best-reflects-oracle-fundamentals)
- [Cointelegraph: Pyth 대 Chainlink](https://cointelegraph.com/news/chainlink-faces-rising-competition-pyth-grows-tvs)
