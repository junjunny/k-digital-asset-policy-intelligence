# 이더리움 네트워크 분석

> 기준일: 2026-11-18 · Ethereum Mainnet 및 이더리움에 정산하는 L2 대상  
> 기술·시장 분석이며 투자 권유가 아니다. 사용량 수치는 제공자별 집계 방식이 다르다.

## 핵심 결론

이더리움은 단순한 고성능 L1이라기보다 **분산된 결제·정산·데이터 가용성 계층 위에 EVM과 다수의 L2를 결합한 플랫폼**으로 보는 편이 정확하다.

- 가장 큰 강점은 검증자 수 하나가 아니라 다중 클라이언트, 오프체인 거버넌스, 풍부한 개발 도구, 높은 유동성, 범용 EVM 표준이 결합된 생태계다.
- 약점은 L1의 상태 증가와 하드웨어 부담, 스테이킹·블록 빌더·RPC의 집중, L2의 중앙화된 시퀀서와 브리지·업그레이드 키, L2 간 유동성·사용자 경험 분절이다.
- 확장 전략은 “모든 거래를 L1에서 처리”하는 방식이 아니다. L1은 보안·정산·데이터 가용성을 제공하고, 대량 실행은 롤업이 맡는 **롤업 중심 로드맵**이다.[E4]
- 2025년 Pectra와 Fusaka까지는 메인넷에 구현됐다. 반면 Glamsterdam은 Sepolia에는 적용됐지만 Hoodi 테스트가 연기됐고, 2026년 11월 18일 현재 메인넷 일정이 없다.[E11]
- 계정 추상화도 완성 상태가 아니다. ERC-4337과 EIP-7702는 실제 사용 중이지만, 번들러 등에 덜 의존하는 프로토콜 내장형 계정 추상화는 계획 단계다.[E9]

## 1. 실행 계층과 합의 계층

이더리움은 두 개의 독립된 체인이 아니라, 한 네트워크를 두 계층의 클라이언트가 함께 처리한다.[E1]

| 구분 | 역할 |
|---|---|
| 실행 계층(EL) | 거래 유효성 검사, 트랜잭션 풀, 계정·컨트랙트 상태 관리, EVM 실행, JSON-RPC 제공 |
| 합의 계층(CL) | PoS 검증자 집합, 블록·어테스테이션 전파, 포크 선택, 정당화·최종성 관리 |
| Engine API | 합의 클라이언트가 실행 클라이언트에 실행 페이로드 검증·생성을 요청하는 로컬 연결 |
| 검증자 클라이언트 | 블록 제안 및 어테스테이션 수행. 일반 비검증 노드에는 필수가 아니지만 스테이킹에는 필요 |

새 블록이 도착하면 합의 클라이언트가 실행 페이로드를 실행 클라이언트에 넘기고, 실행 클라이언트가 모든 거래를 다시 실행해 상태 루트가 맞는지 확인한다. 따라서 “합의에는 성공했지만 EVM 실행 결과가 틀린 블록”은 유효한 이더리움 블록이 될 수 없다.

이 구조는 실행·합의 클라이언트를 독립적으로 개발할 수 있다는 장점이 있지만, 노드 운영자가 두 소프트웨어와 두 P2P 네트워크를 함께 관리해야 한다는 복잡성도 만든다.

## 2. PoS와 보안 구조

이더리움 PoS는 대체로 다음 요소의 결합이다.[E2]

- 최소 32 ETH를 활성화 단위로 예치한다. Pectra 이후 하나의 검증자 유효 잔액을 최대 2,048 ETH로 통합할 수 있지만, 신규 참여의 기본 활성화 단위 자체가 2,048 ETH로 바뀐 것은 아니다.
- 매 슬롯에서 한 검증자가 블록 제안자로 선택되고, 다른 검증자들이 블록에 어테스테이션한다.
- LMD-GHOST 계열 포크 선택이 체인의 머리를 고르고, Casper FFG가 체크포인트를 정당화·최종화한다.
- 정상 참여에는 ETH 보상이 지급되고, 오프라인에는 페널티, 이중 제안·이중 투표 같은 중대한 행위에는 슬래싱이 적용된다.
- 총 지분의 3분의 1 이상이 협조하지 않으면 최종성을 지연시킬 수 있다. 상충하는 최종성을 만들려면 대규모 이중 투표와 그에 따른 슬래싱 위험을 부담해야 한다.

PoS 보안은 단순히 “공격자가 ETH를 많이 사야 한다”는 논리에만 의존하지 않는다. 슬래싱, inactivity leak, 클라이언트의 포크 선택, 그리고 극단적인 경우 어떤 체인을 정통으로 인정할지에 관한 사회적 복구가 함께 작동한다. 사회적 복구는 강력한 최후 수단인 동시에, 완전히 기계적인 거버넌스가 아니라는 한계를 보여준다.

## 3. EVM

EVM은 모든 노드가 같은 바이트코드를 같은 규칙으로 실행하는 결정론적 상태 머신이다.[E3]

- 스마트계약은 Solidity·Vyper 등으로 작성된 뒤 EVM 바이트코드로 컴파일된다.
- 연산, 저장공간 접근, 메모리 사용 등에 gas가 부과된다.
- 계산이 실패해 상태 변경이 되돌려져도 이미 소비한 계산 비용은 대체로 지급해야 한다.
- 전역 상태는 계정 잔액, nonce, 컨트랙트 코드와 저장공간을 포함한다.

EVM의 전략적 가치는 순수 실행 성능보다 **호환성 표준**에 있다. 지갑, Solidity, Foundry·Hardhat, ethers·viem, 감사 도구, RPC, 인덱서와 기존 스마트계약을 여러 EVM 체인과 L2가 재사용할 수 있다.

반대로 순차 실행, 영구 상태 증가, 비교적 비싼 저장공간 접근은 성능상의 제약이다. Glamsterdam에서 검토 중인 블록 단위 접근 목록은 병렬 실행에 필요한 데이터 의존성을 미리 드러내려는 시도이지만 아직 메인넷 기능이 아니다.

## 4. L2와 롤업 중심 확장

이더리움이 공식적으로 L2로 분류하는 핵심 유형은 Ethereum에 데이터와 보안을 의존하는 optimistic rollup과 ZK rollup이다.[E4]

| 유형 | 유효성 방식 | 주요 장점 | 주요 위험·제약 |
|---|---|---|---|
| Optimistic rollup | 기본적으로 유효하다고 보고 이의 제기 시 fault/fraud proof | EVM 호환성이 높고 구현이 비교적 성숙 | 출금 지연, 증명 시스템·감시자 의존, 시퀀서 집중 |
| ZK rollup | L1 컨트랙트가 validity proof 검증 | 빠른 암호학적 최종 확인, 높은 압축 가능성 | 증명기 복잡성, prover 집중, 회로·브리지 위험 |
| Validium·별도 DA | 데이터 일부를 Ethereum 밖에 저장 | 더 낮은 비용 | 데이터 가용성 보안이 Ethereum과 동일하지 않음 |

Dencun의 EIP-4844는 롤업 데이터용 blob과 별도의 blob 수수료 시장을 도입했다. Fusaka의 PeerDAS는 검증자가 모든 blob을 전부 내려받는 대신 샘플링할 수 있게 해 blob 용량 증가의 기반을 마련했다.[E5]

그러나 L2가 L1 보안을 “그대로 복제”하는 것은 아니다. 실제 안전성은 다음을 별도로 확인해야 한다.

- 시퀀서가 단일 운영자인지, 강제 포함 경로가 실제 작동하는지
- fault/validity proof가 무허가·실전 상태인지
- 업그레이드 키와 보안위원회가 즉시 자산 로직을 바꿀 수 있는지
- 정식 브리지와 외부 브리지 중 무엇을 쓰는지
- 거래 데이터가 Ethereum blob/calldata에 게시되는지
- 장애 시 사용자가 독립적으로 자산을 회수할 수 있는지

## 5. 탈중앙화와 거버넌스

### 강점

- 누구나 노드를 운영하고 유효한 거래·블록을 직접 검증할 수 있다.
- 실행·합의 양쪽에 여러 독립 클라이언트 구현이 있다.
- 프로토콜 변경은 ETH 보유량에 의한 단일 온체인 투표가 아니라 EIP, 공개 논의, 다수 클라이언트 구현, 테스트넷, 노드 운영자의 채택을 거친다.[E6]
- 2026년 공개 집계는 약 1만4천 개 수준의 실행 노드를 추적했고, ProbeLab은 11월 16일 약 8,149개 합의 노드에 도달했다. 두 수치는 탐지 방식이 달라 직접 합산할 수 없다.[E7]

### 집중 위험

- 거래소·리퀴드 스테이킹·전문 노드 운영자에 지분과 운영이 집중될 수 있다.
- 특정 실행·합의 클라이언트가 3분의 1 이상을 차지하면 공통 버그의 영향이 커진다. 정확한 클라이언트 점유율은 원격 추정이라 오차도 크다.[E8]
- MEV 블록 빌더·릴레이가 블록 구성을 집중시킬 수 있다.
- 사용자는 자체 노드보다 소수 RPC·지갑·프론트엔드에 의존하는 경우가 많다.
- 상당수 L2가 단일 시퀀서와 제한된 업그레이드 주체를 갖는다.

따라서 이더리움을 “완전히 탈중앙화됐다”거나 “검증자가 많으므로 집중 문제가 없다”고 평가하는 것은 과도하다. 다만 45개 검증자 집합 같은 체인과 비교하면 검증·클라이언트·거버넌스의 권한이 더 여러 층으로 분산돼 있다.

## 6. 수수료와 ETH의 역할

EIP-1559 이후 일반 실행 수수료는 다음과 같다.[E10]

`사용 gas × (base fee + priority fee)`

- base fee: 프로토콜이 혼잡도에 따라 조정하며 소각한다.
- priority fee: 거래 포함 유인을 위해 검증자에게 지급한다.
- blob fee: L2 데이터 공간에 별도로 부과되고 소각된다.
- 합의 보상: 검증·어테스테이션 대가로 새 ETH가 발행된다.

ETH에는 네 가지 핵심 역할이 있다.

1. L1 실행 및 blob 공간의 수수료 자산
2. PoS 담보와 슬래싱 대상
3. 검증자 보상 및 블록 빌더·MEV 결제 자산
4. DeFi·L2에서 담보·유동성·결제 자산

ETH 공급은 고정 상한 방식이 아니다. PoS 보상은 공급을 늘리고 base fee 소각은 줄인다. 네트워크 활동에 따라 순발행 또는 순소각이 될 수 있으므로 “ETH는 항상 디플레이션”이라는 설명은 틀리다.[E10]

2026년 1~10월 메인넷 중간 수수료의 월별 평균은 약 3.5센트로 집계됐지만, 이는 당시 낮은 gas 환경의 결과이지 영구 보장은 아니다. 블록 공간이 포화되면 다시 상승한다.[E7]

## 7. 실제 사용과 개발자 생태계

### 사용

Ethereum Institutional이 외부 데이터 제공자의 수치를 취합한 2026년 11월 보고서에 따르면:[E7]

- 2026년 1~10월 메인넷은 하루 평균 약 217만 건의 거래를 처리했다.
- Ethereum과 47개 L2 집합은 하루 약 2,500만 건을 처리했다.
- 같은 기간 메인넷 스테이블코인 이동액은 약 25.8조 달러로 집계됐다.
- 2026년 10월 31일 약 4,420만 ETH, 공급량의 약 36.1%가 스테이킹돼 있었다.

DefiLlama는 2026년 11월 17일 Ethereum 메인넷에 약 374억 달러의 DeFi TVL과 1,313억 달러의 스테이블코인을 집계했다.[E7]

이는 금융 사용과 경제적 상태가 크다는 증거지만, 거래 건수는 실제 사용자 수와 같지 않으며 스테이블코인 이동액에는 봇·재조정·중복 이동이 포함될 수 있다. TVL도 토큰 가격과 집계 규칙에 민감하다.

### 개발자 생태계

Ethereum의 우위는 다음 층에 걸쳐 있다.

- 다수의 실행·합의 클라이언트 팀
- Solidity·Vyper와 광범위한 EVM 개발 인력
- Foundry, Hardhat, OpenZeppelin, ethers, viem 등 성숙한 도구
- ERC-20·721·1155·4626·4337 등 애플리케이션 표준
- 감사, RPC, 인덱싱, 지갑, 오라클, 커스터디 시장
- L2와 다른 EVM L1로의 코드·인력 이동성

Electric Capital의 공개 방법론은 오픈소스 커밋을 기준으로 생태계를 측정한다. 2024년 자료에서는 Ethereum 계열이 전체 기존 개발자 기반에서 선두였지만 Solana가 신규 개발자 유입에서 앞섰다. 오픈소스 커밋은 비공개 개발과 코드 품질을 반영하지 않으므로 절대적 생태계 순위로 해석해서는 안 된다.[E12]

## 8. 주요 업그레이드: 구현과 계획의 구분

| 업그레이드 | 실제 상태 | 핵심 내용 |
|---|---|---|
| London, 2021 | **메인넷 구현** | EIP-1559 base fee·소각 |
| Beacon Chain, 2020 / Merge, 2022 | **메인넷 구현** | PoS 합의 계층 도입, PoW 종료 |
| Shapella, 2023 | **메인넷 구현** | 스테이킹 출금 |
| Dencun, 2024 | **메인넷 구현** | EIP-4844 blob, 롤업 데이터 비용 절감 |
| Pectra, 2025-05-07 | **메인넷 구현** | EIP-7702, validator 최대 유효 잔액 2,048 ETH, 실행 계층 출금·예치 개선, blob 용량 증가 |
| Fusaka, 2025-12-03 | **메인넷 구현** | PeerDAS, 추가 blob 확장, 실행·합의 효율 개선 |
| Glamsterdam | **Sepolia 적용, Hoodi·메인넷 미적용** | ePBS, block-level access lists, 상태 생성·접근 gas 재가격, L1 확장 |
| Hegotá | **계획·범위 조정 중** | native account abstraction, 검열 저항, 추가 상태·UX 개선 후보 |
| Statelessness·binary tree·zkEVM attestation·양자내성 | **장기 연구·로드맵** | 노드 부담 감소, 증명 기반 검증, 보안 강화 |

Glamsterdam은 특히 주의해야 한다. Sepolia에서는 2026년 10월 6일 활성화됐지만, EIP-8037이 기존 메인넷 스마트계약의 gas 가정과 충돌할 가능성이 발견돼 10월 22일 Hoodi 활성화가 연기됐다. 새 Hoodi·메인넷 일정은 아직 없다.[E11] 따라서 “Glamsterdam의 200M gas, ePBS, 병렬 실행이 현재 메인넷에 구현됐다”는 설명은 사실이 아니다.

## 9. 계정 추상화

계정 추상화의 목표는 사용자가 하나의 ECDSA 개인키와 ETH gas 잔액에만 의존하지 않도록 하는 것이다. 배치 실행, gas 대납, ERC-20 수수료, 세션 키, 패스키, 다중서명, 사회적 복구 등을 가능하게 한다.

### 실제 구현

- **ERC-4337:** 2023년부터 EntryPoint 스마트계약, 별도 UserOperation mempool, bundler·paymaster를 이용한다. 합의 규칙을 바꾸지 않았다. 2026년 6월 공식 페이지 기준 2,600만 개 이상의 스마트 계정과 1억7천만 건 이상의 UserOperation이 집계됐다.[E9]
- **EIP-7702:** Pectra로 메인넷에 적용됐다. 기존 EOA가 스마트계약 코드에 권한을 위임할 수 있다. 배치, gas 대납, 복구 기능의 기반이지만, 위임된 코드는 계정 전체 권한을 가질 수 있어 지갑의 코드 검증이 중요하다.

### 아직 계획

EIP-7702가 EOA를 영구적으로 완전한 네이티브 스마트 계정으로 바꾼 것은 아니다. ERC-4337도 bundler, EntryPoint, paymaster 같은 추가 인프라가 필요하다.

EIP-8141 Frame Transactions 등은 계정 검증·실행 로직을 프로토콜에 더 직접 포함하려는 native AA 후보지만, Hegotá 후보 단계이며 메인넷 구현 사실로 볼 수 없다.

## 10. 경쟁 네트워크

| 경쟁군 | 상대적 강점 | Ethereum 대비 주요 차이 |
|---|---|---|
| Bitcoin | 가장 보수적인 통화·결제 원장, 단순성과 브랜드 | 범용 상태 실행·DeFi 개발 환경은 제한적 |
| Solana | 단일 상태 환경에서 높은 처리량·낮은 수수료·빠른 UX | EVM이 아닌 런타임, 더 높은 노드 성능 요구와 클라이언트·지분 집중 위험 |
| BNB Smart Chain | EVM 호환, 낮은 비용, 거래소 유통력 | 공식 문서상 45개 PoSA 검증자 집합으로 Ethereum보다 좁은 합의 참여층 |
| Avalanche·Sui·Aptos 등 | 서브넷·객체 중심 실행·병렬화 등 차별적 설계 | 유동성, 개발 도구, 표준과 보안 모델이 각각 분산 |
| Cosmos 계열 앱체인 | 애플리케이션별 주권과 맞춤형 실행 | 각 체인이 별도 검증자·경제 보안을 마련해야 할 수 있음 |
| Ethereum L2 | Ethereum 정산을 유지하며 저비용·대량 처리 | 사실상 Ethereum의 확장망인 동시에 사용자·유동성을 두고 서로 경쟁 |

Solana 공식 문서는 현재 기본 수수료를 서명당 5,000 lamports로 설명하고, BNB Chain 공식 문서는 45개 PoSA 검증자 집합을 명시한다.[E13] 다만 TPS나 수수료만 비교하면 검증 비용, 실패 거래, 최종성, 데이터 가용성, 하드웨어 요구량과 경제적 상태의 질적 차이를 놓치게 된다.

## 종합 평가

**확인된 사실:** Ethereum은 PoS·EVM·롤업 중심 구조를 실제 운영하고 있으며, Dencun·Pectra·Fusaka를 통해 L2 데이터 용량과 계정 기능을 확장했다. 금융 자산, 스테이블코인, DeFi, 개발 도구 면에서 여전히 가장 깊은 범용 스마트계약 생태계 중 하나다.

**근거 있는 추론:** Ethereum의 장기 경쟁력은 L1 TPS보다 “고가치 상태를 두는 중립적 정산층 + L2 실행 시장 + EVM 표준”을 얼마나 안정적으로 유지하느냐에 달려 있다.

**핵심 실패 조건:** L2가 장기간 중앙화된 상태에 머무르거나, 브리지·업그레이드 키 사고가 반복되거나, 스테이킹·블록 빌더·클라이언트가 보안 임계치 이상으로 집중되거나, L2 활동 증가가 ETH 보안·수수료 수요와 충분히 연결되지 않는 경우다.

### 주요 근거

- **E1 – 확인된 사실:** [Ethereum 노드 아키텍처](https://ethereum.org/developers/docs/nodes-and-clients/node-architecture/)
- **E2 – 확인된 사실:** [PoS와 최종성](https://ethereum.org/developers/docs/consensus-mechanisms/pos/), [PoS 공격과 방어](https://ethereum.org/developers/docs/consensus-mechanisms/pos/attack-and-defense/)
- **E3 – 확인된 사실:** [Ethereum Virtual Machine](https://ethereum.org/developers/docs/evm/)
- **E4 – 확인된 사실:** [Ethereum 확장 구조](https://ethereum.org/developers/docs/scaling/), [Optimistic rollups](https://ethereum.org/developers/docs/scaling/optimistic-rollups/), [ZK rollups](https://ethereum.org/developers/docs/scaling/zk-rollups/)
- **E5 – 확인된 사실:** [Dencun](https://ethereum.org/roadmap/dencun/), [Fusaka](https://ethereum.org/roadmap/fusaka/)
- **E6 – 확인된 사실:** [Ethereum 거버넌스](https://ethereum.org/governance), [EIP 절차](https://ethereum.org/eips)
- **E7 – 공식·외부 데이터 혼합:** [State of the Ledger, 2026-11-05](https://ethereuminstitutional.org/research/state-of-the-ledger), [DefiLlama Ethereum](https://defillama.com/chain/ethereum)
- **E8 – 확인된 위험:** [클라이언트 다양성](https://ethereum.org/developers/docs/nodes-and-clients/client-diversity/), [위임 스테이킹 위험](https://ethereum.org/staking/saas/)
- **E9 – 확인된 사실:** [계정 추상화 로드맵](https://ethereum.org/roadmap/account-abstraction), [ERC-4337](https://eips.ethereum.org/EIPS/eip-4337), [EIP-7702](https://eips.ethereum.org/EIPS/eip-7702)
- **E10 – 확인된 사실:** [Gas와 수수료](https://ethereum.org/developers/docs/gas/), [ETH 발행·소각](https://ethereum.org/what-is-ether/supply/)
- **E11 – 현재 상태:** [Glamsterdam Hoodi 연기 공지](https://blog.ethereum.org/2026/10/22/glamsterdam-hoodi-delay), [Glamsterdam 설명](https://ethereum.org/roadmap/glamsterdam/)
- **E12 – 외부 연구:** [Electric Capital Developer Report 방법론](https://www.developerreport.com/about)
- **E13 – 경쟁망 공식 문서:** [Solana 수수료](https://solana.com/docs/core/fees), [BNB Smart Chain 개요](https://docs.bnbchain.org/bnb-smart-chain/introduction/)
