# 체인링크(Chainlink) 프로젝트 vs LINK 토큰 분석

**기준일: 2026-11-18 / 깊이: STANDARD**

일부 근거는 공식 페이지를 직접 열어 확인했습니다. 나머지는 검색 결과 요약이라 아래에 표시했습니다. 투자 권유나 가격 판단은 포함하지 않습니다.

## 0. 핵심 결론

- 체인링크는 오라클·크로스체인·오프체인 실행을 묶은 **미들웨어 프로젝트**입니다. LINK는 그중 **일부 경로에서만** 수요와 연결되는 토큰입니다.
- 상대방 기관(DTCC, UBS, Swift) 자료를 보면, 이들이 쓰는 것은 **기술 표준과 실행 환경**입니다. 확인한 범위에서 LINK 사용이나 수수료 구조를 명시한 기관 문서는 없었습니다.
- 채택 → LINK 수요로 이어지는 구조는 **Payment Abstraction**(수수료를 LINK로 전환), **Reserve**(전환된 LINK 적립), **Staking**입니다. 이 구조는 프로젝트 측이 설계·공개한 것이고, 실제 전환 규모는 검증하지 못했습니다.

## 1. 프로젝트 층: 무엇을 하는가

| 구성 | 공식 설명 | 상태 |
|---|---|---|
| 오라클(Data Feeds 등) | 온체인 가격·데이터 제공 | 상용 운영. 스테이킹 문서에도 Ethereum ETH/USD 피드 보호가 명시됨 |
| CCIP | 크로스체인 메시지·토큰 전송 | 운영 중. 2.0 출시는 2차 자료에 따른 것이라 원문 확인 필요 |
| CRE(Runtime Environment), DTA 표준 | 오프체인 시스템과 스마트컨트랙트를 연결하는 오케스트레이션 | 사례별로 단계가 다름 (아래 2절) |

## 2. 활용 사례: 파일럿 vs 상용 vs 계획

기관 측 원문 기준으로 분리했습니다.

| 사례 | 상대방 기관 표현 | 구분 |
|---|---|---|
| **Swift·UBS AM·Chainlink** (2024-11-05, MAS Project Guardian) | Swift 보도자료가 "successfully complete pilot"라고 표현. 현금 결제는 Swift 망이 오프체인으로 처리 | **파일럿(완료)**. 결제 단계에 LINK 개입 근거 없음 |
| **UBS uMINT 토큰화 펀드** (2025-11-04) | UBS가 "live, in-production" 거래로 표현. 규모는 비공개. UBS는 Chainlink를 DTA **기술 표준** 제공자로 서술 | **제한적 실거래**. 단건 최초 거래 수준 |
| **DTCC Collateral AppChain** (2026-05-12) | "publicly unveiled", "expected to go live in Q4 2026". 상용/파일럿 구분 없음. 계약·수수료·LINK 언급 **없음** | **계획·예정**. 조건부 표현 (expected, designed to, will leverage) |
| 기업행동(corporate actions) 24개 기관 이니셔티브 | Chainlink 블로그와 2차 자료의 설명. Swift·Euroclear 원문은 이번에 직접 확인하지 못함 | 개념검증(PoC) 성격, `NEEDS_REVIEW` |

DeFi 쪽 사용(Aave SVR 등)은 Chainlink 문서 기준으로 메인넷 상용입니다. 다만 이 경우에도 상대방은 Aave 거버넌스 자료로 따로 확인해야 합니다.

## 3. LINK 토큰 층

**역할 (공식 자료 확인분)**
- 노드 운영자 보상 및 서비스 수수료 결제 수단
- 스테이킹 담보. v0.2는 한도 4,500만 LINK, 커뮤니티 기본 하한 보상 연 4.5%(위임 후 실효 4.32%), 주소당 상한 15,000 LINK. 슬래싱은 **노드 운영자에게만** 적용(700 LINK/건). 보호 대상은 출시 시점에 ETH/USD 피드 하나입니다.
- Reserve: 2025-08-07 발표. Payment Abstraction으로 오프체인·온체인 매출을 LINK로 전환해 적립합니다. 다일 타임락이 있고 "수년간 인출을 예상하지 않는다"고 했으나, 이는 약속이 아니라 **기대 표명**입니다.

**가치 포착의 실제 경로와 한계**
1. 수수료가 LINK로 전환되려면 Uniswap V3 등 온체인 유동성에서 **매수**가 일어납니다. 초기 대상은 Aave SVR의 Chainlink 몫으로, 문서가 전환 규모를 "예측하기 어렵다"고 직접 밝혔습니다.
2. CCIP 수수료는 LINK 외에 네이티브 토큰이나 스테이블로도 낼 수 있다는 것이 일반적인 이해입니다. 이번에 CCIP 문서 페이지가 404여서 **직접 확인하지 못했습니다**. 확인되면 기관이 CCIP를 써도 LINK 직접 수요가 아닐 수 있습니다.
3. 기관이 비용을 법정화폐 계약(오프체인 매출)으로 낸다면, 그 LINK 전환 여부와 비율은 공개 근거가 부족합니다. Reserve 잔고는 2차 자료상 약 142만 LINK(날짜 불명)이고, 현재값은 reserve.chain.link에서 확인해야 합니다.

## 4. 공급

- 최대 공급 10억 LINK는 복수 2차 자료가 일치합니다. 배분은 공개 판매 35%, 노드·생태계 35%, 회사 30%입니다.
- 유통량은 출처마다 5.87억~7.48억으로 **충돌**합니다(CoinGecko, DefiLlama 등). 공식 유통량 페이지(chain.link/circulating-supply)를 직접 열어 확인하지 못해 `UNVERIFIED`입니다.
- 회사 보유분의 해제 일정이 고정 공개인지도 자료가 상충합니다. 잠금 해제와 Reserve 적립은 방향이 반대인 요인이므로 함께 봐야 합니다.

## 5. 보안·의존성

- CCIP는 Risk Management Network(별도 구현·별도 노드 집합)를 방어 계층으로 설계했습니다. 다만 Decrypt가 인용한 문서에는 **"RMN의 자동 오프체인 역할이 현재 배포에서는 비활성"**이라는 내용이 있습니다. 이는 2차 보도라 `NEEDS_REVIEW`이며, 오래된 마케팅 자료는 활성처럼 기술한 경우가 있어 주의해야 합니다. CCIP 2.0은 기관이 자체 검증자를 두는 방식을 허용한다고 보도됐습니다. 이 경우 Chainlink 노드 집합에 대한 의존이 줄어드는 만큼 토큰 담보 논리도 약해질 수 있습니다.
- 감사: Code4rena 콘테스트(2024-11, 상금 $235K)는 확인했으나, 그 외 감사 범위는 확인하지 못했습니다.
- 의존성: 스테이킹 보호가 사실상 소수 피드에 한정되어 있고, 스왑 경로가 Uniswap V3와 가격 피드에 의존합니다. 기관 프로젝트는 Chainlink 외에도 Swift·DTCC·UBS 같은 상대방의 일정과 정책에 묶여 있습니다.

## 6. 경쟁

Pyth, LayerZero, Wormhole, Chronicle, RedStone 등이 경쟁하지만, **이번에 이들의 공식 자료는 조사하지 않았습니다.** 일반 지식 수준의 `UNVERIFIED`입니다. 비교하려면 지원 체인 수, 보안 모델, 수수료 토큰, 실사용 금액을 각 공식 문서에서 따로 확인해야 합니다.

## 7. 채택 ≠ 토큰 수요: 점검 틀

| 질문 | 현재 확인 결과 |
|---|---|
| 기관이 LINK를 사거나 보유하는가? | 확인한 기관 문서에는 없음 |
| 수수료가 LINK로 전환되는가? | 구조는 공개됨. 규모는 미확인 |
| LINK가 보안(스테이킹)에 필수인가? | 현재는 소수 피드에 한정 |
| 대체 결제 수단이 있는가? | CCIP 문서 확인 필요 |
| 상대방이 계약·수수료를 공개했는가? | DTCC·UBS 발표문에는 없음 |

## 8. 남은 확인 과제

1. CCIP 공식 수수료 문서와 RMN 현재 상태의 원문 확인
2. 공식 유통량·잠금 해제 일정 대조
3. Euroclear·Swift의 기업행동 이니셔티브 원문, Aave 거버넌스의 SVR 정산 자료
4. reserve.chain.link의 현재 잔고
5. 경쟁 프로젝트 1차 자료

한계로, DTCC·UBS·Swift 자료는 검색·요약을 거쳤고 전문 대조(`CONTENT_VERIFIED`)는 아직 아닙니다. 이 보고서의 핵심 주장은 대부분 `SUPPORTED_INFERENCE`로 보는 것이 안전합니다.

Sources:
- [DTCC–Chainlink 보도자료 (2026-05-12)](https://www.dtcc.com/news/2026/may/12/dtcc-collaborates-with-chainlink-to-advance-24-7-collateral-management)
- [UBS: live tokenized fund transaction (2025-11-04)](https://www.ubs.com/global/en/media/display-page-ndp/en-20251104-chainlink.html)
- [Swift·UBS AM·Chainlink 파일럿 완료](https://www.swift.com/news-events/migrated-news/press-releases/swift-ubs-asset-management-and-chainlink-successfully-complete-innovative-pilot-bridge-tokenized-assets-existing-payment-systems)
- [Chainlink Staking](https://chain.link/economics/staking)
- [Chainlink Reserve 발표](https://chain.link/blog/chainlink-reserve-strategic-link-reserve)
- [Payment Abstraction](https://chain.link/blog/payment-abstraction-svr-fee-conversion)
- [CCIP Risk Management Network 문서](https://docs.chain.link/ccip/concepts/architecture/offchain/risk-management-network)
- [Decrypt: RMN 상태 보도 (2차)](https://decrypt.co/379463/chainlink-institutions-add-bridge-checks-kelp-hack)
- [DefiLlama LINK 언락 (2차)](https://defillama.com/unlocks/chainlink)
