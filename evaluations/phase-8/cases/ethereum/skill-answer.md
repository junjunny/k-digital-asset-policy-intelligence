# 이더리움 네트워크 평가: 범용 정산층과 롤업 생태계의 강점, 그리고 복잡성의 대가

> 분석 기준일: 2026-11-17 · 질문 유형: `NETWORK_OR_PROTOCOL_REVIEW` · 응답 모드: `STANDARD`  
> 기술·네트워크 평가이며 투자 권유가 아니다. ETH 가격이나 시가총액은 네트워크 품질의 근거로 사용하지 않았다.

## 핵심 결론

이더리움의 가장 큰 특징은 **하나의 고속 체인으로 모든 일을 처리하기보다, 보수적인 L1을 공용 정산·데이터 가용성 층으로 두고 여러 L2 롤업이 실행을 확장하는 구조**라는 점이다. 범용 스마트계약 표준(EVM), 여러 독립 클라이언트, 큰 개발자·도구 생태계, 오랜 운영 이력은 강점이다. 반면 사용자는 L1·L2·브리지의 서로 다른 보안 가정을 이해해야 하고, 스테이킹 사업자·블록 빌더·L2 시퀀서에 집중 위험이 남는다.

따라서 비교 결론은 용도에 따라 달라진다.

- **중립적인 공용 정산, 조합 가능한 스마트계약, 장기적인 생태계 호환성**을 중시하면 이더리움이 강하다.
- **단일 체인에서 매우 짧은 지연과 높은 처리량, 단순한 사용자 경험**을 중시하면 Solana 같은 고성능 L1이 더 직접적이다.
- **가치저장·단순 송금과 최소한의 프로토콜 변화**가 우선이면 Bitcoin이 더 단순하다.
- **맞춤형 독립 체인과 빠른 확정성**이 필요하면 Avalanche L1 구조가 더 유연할 수 있다.

이더리움의 장점은 “모든 지표에서 1등”이 아니라, **탈중앙화·검증 가능성·프로그래머빌리티·확장성 사이의 절충을 L1과 L2로 나눈 것**이다. 그 대가는 아키텍처와 운영 위험이 다른 체인보다 복잡하다는 것이다. [E01][E05][E08]

## 1. 무엇을 위한 네트워크인가

이더리움은 단순 결제 장부가 아니라 누구나 프로그램을 배포하고 실행할 수 있는 범용 상태 머신이다. 계정, 토큰, 거래소, 대출, 스테이블코인, 게임, 신원·조직 도구 등이 동일한 EVM 규칙 아래 상호 호출될 수 있다. 이 “조합 가능성”과 ERC 표준·Solidity 도구의 축적이 네트워크 효과의 핵심이다. 다만 애플리케이션 계약의 안전성과 이더리움 L1 자체의 안전성은 별개다. L1이 정상이어도 취약한 계약, 오라클, 관리자 키, 브리지가 손실을 일으킬 수 있다. [E03][E16]

## 2. PoS, 검증자, 실행층과 합의층

### 작동 구조

- 이더리움은 2022년 9월부터 작업증명 대신 지분증명(PoS)을 쓴다.
- 노드는 **실행 클라이언트(EL)**와 **합의 클라이언트(CL)**를 함께 실행한다. EL은 거래·EVM 상태변경을 실행하고, CL은 블록 제안, attestation, fork choice와 finality를 처리한다. “Eth1/Eth2”라는 두 네트워크가 따로 존재하는 것이 아니다. [E01][E02]
- 시간은 **12초 슬롯**, 32슬롯(약 6.4분) 에폭으로 나뉜다. 슬롯마다 한 제안자가 선택되고 검증자 위원회가 투표한다. Casper FFG와 LMD-GHOST를 합친 Gasper가 fork choice와 finality를 제공한다. 보통 연속된 두 checkpoint가 총 지분의 3분의 2 이상 지지를 얻어 finalized 된다. 프로토콜상 정상 finality는 대략 두 에폭 규모이지 “12초 즉시 확정”이 아니다. [E01]
- 직접 검증자의 최소 활성화 지분은 32 ETH다. 2025년 Pectra 이후 선택형 compounding validator는 유효 잔액을 최대 2,048 ETH까지 합칠 수 있다. 따라서 **검증자 인덱스 수를 독립 운영자 수로 세면 안 된다**. 한 사업자가 많은 검증자 키를, 또는 하나의 통합 검증자를 운용할 수 있다. [E04]
- 부정한 이중 제안·모순된 투표는 slashing 대상이고, 단순 오프라인은 보상 손실·비활성 패널티를 받는다. 총 지분 약 3분의 1은 finality를 방해할 수 있고, 3분의 2는 잘못된 checkpoint를 finalize할 위험 경계다. finalized history를 되돌리려면 최소 약 3분의 1 지분이 소각될 수 있다는 경제적 억제가 핵심이다. [E01]

2026년 10월 31일에는 44.2M ETH, 당시 유통량의 36.1%가 스테이킹되어 있었다는 집계가 있다. 이는 경제적 담보 규모를 보여주지만 **그 지분을 누가 운용하는지**와는 다른 지표다. 2026년 11월 17일 조회한 Rated 공개 분류에서는 Lido 21.14%, SSV 16.04%, Binance 7.90%, Kraken 6.74%, Coinbase 4.69%였다. 이 분류는 pool/entity 귀속 추정이며 서로 다른 측정법과 시간창에 따라 값이 달라질 수 있다. Lido의 562개 entity 표시는 단일 중앙 서버와 동일하지도, 완전히 독립적인 지분과 동일하지도 않다. [E09][E10]

## 3. 성능과 확장: 설계상 수치와 관측치를 분리해서 봐야 한다

### L1

이더리움 L1은 거래별 복잡도가 달라 단일 “TPS”만으로 정확히 비교하기 어렵다. 단순 송금과 복잡한 DeFi 호출의 gas 사용량이 다르기 때문이다. 2026년 11월 17일 growthepie의 최근 완료일 데이터는 L1에서 **2.06M건/일**과 **2.53 Mgas/s**를 관측했다. 단순히 하루 거래를 86,400초로 나누면 약 23.8건/초지만, 이는 거래 구성에 종속된 관측 평균이지 프로토콜의 고정 최대 TPS가 아니다. [E06]

2026년 1~10월 평균은 L1 **2.17M건/일**, 일별 median transaction fee를 다시 평균한 값은 **$0.035**였다. 2026년 11월 16일 growthepie의 최신 일별 L1 median fee는 **$0.08**이었다. 수수료는 ETH 가격, gas 수요, 거래 유형에 따라 달라지므로 이 두 수치는 서로 다른 기간·방법론의 결과다. EIP-1559에서 수수료는 gas 사용량×가격이며 base fee는 소각되고 priority fee는 제안자에게 간다. 낮은 최근 수수료는 사용자에게 유리하지만, 영구적으로 보장된 값은 아니다. [E07][E11]

### L2 롤업 중심 확장

Dencun(2024)은 blob을, Fusaka(2025)는 PeerDAS를 도입해 롤업 데이터 게시 비용과 노드의 데이터 부담을 낮췄다. 롤업은 거래를 L2에서 실행·묶고 결과·증명·데이터를 이더리움에 게시한다. 이는 “L1 자체 TPS가 수천으로 늘었다”는 뜻이 아니다. [E05][E12]

2026년 11월 17일 최근 완료일 기준 growthepie는 추적 대상 이더리움 L2를 합쳐 **21.40M건/일**, L1은 **2.06M건/일**로 집계했다. 즉 해당 데이터셋에서 L2 거래가 L1의 10.4배였고, 생태계 일일 거래의 약 91%가 L2였다. 2026년 10월의 체인별 월간 median fee를 다시 중앙값 낸 L2 fee는 **0.19센트($0.0019)**였다. 그러나 이는 “모든 L2 거래가 그 가격”이라는 뜻이 아니다. [E06][E13]

ETHBEAT는 2026년 11월 16일 기준 rollup TVS를 **$26.79B**로 집계했다. TVS는 예치액·네이티브 발행·외부 브리지 자산을 포함하는 보안 노출액이지 처리 성능이나 무위험 자산 규모가 아니다. 또한 롤업마다 fraud/validity proof, 데이터 가용성, 업그레이드 키, 강제 출금, 시퀀서가 다르다. ETHBEAT의 개별 위험 분석처럼 중앙 시퀀서가 검열·중단·MEV 위험을 만들고 즉시 업그레이드 키가 자금 위험을 만들 수 있다. “이더리움 L2”라는 이름만으로 L1과 같은 신뢰 모델을 가정하면 안 된다. [E08]

향후 full Danksharding의 “100,000 TPS 이상”은 ethereum.org가 제시하는 **장기 설계 목표**이지 2026년 11월 L1 실측값이 아니다. [E12]

## 4. 탈중앙화를 어떻게 평가해야 하는가

검증자 개수 하나로는 부족하다. 최소한 다음을 함께 봐야 한다.

1. **지분 소유·위임 집중도**: 1/3과 2/3 경계, 상위 사업자·LST 프로토콜 비중
2. **실제 노드 운영자 수**: 여러 검증자 키가 같은 조직·클라우드·데이터센터에 있는지
3. **클라이언트 다양성**: 같은 버그가 지분의 1/3을 넘으면 finality 정지, 2/3을 넘으면 잘못된 finalization 위험
4. **지리·호스팅·관할권 분포**: 클라우드·통신·제재·정전의 공통 실패 가능성
5. **블록 생산 공급망**: proposer, builder, relay와 MEV 인프라 집중도
6. **사용자 검증 가능성**: 일반인이 full node를 운영할 하드웨어·대역폭 부담
7. **거버넌스와 업그레이드 권한**: 누가 사양을 정하고, 누가 소프트웨어를 배포하고, 누가 최종 채택을 거부할 수 있는지
8. **L2의 별도 통제점**: sequencer, prover, challenger, admin multisig와 탈출 경로

이더리움의 장점은 실행·합의 양쪽에 여러 독립 구현이 있다는 점이다. 반면 2026년 공식 권장 validator 장비는 대략 4TB NVMe, 64GB RAM, 50Mbps down/25Mbps up으로, 소비자 장비로 가능하지만 가볍지는 않다. 32 ETH 자본 장벽도 solo staking을 제한해 풀·거래소 이용을 유도한다. [E14][E15]

## 5. 개발 생태계와 거버넌스

EVM·Solidity·ERC 표준, 지갑, 인덱서, 감사 도구, 라이브러리, L2의 폭은 이더리움의 가장 강한 방어선이다. Electric Capital의 가장 최근 공개 연례 보고서는 2024년 자료다. 그 집계에서 Ethereum 생태계는 전체 개발자 점유에서 1위였지만, **2024년 신규 개발자**는 Solana 7,625명, Ethereum 6,456명으로 Solana가 앞섰다. 공개 GitHub 활동 기반이며 비공개 저장소를 포착하지 못하고 “개발자 수=제품 품질”도 아니므로, 생태계의 방향성을 보는 보조지표로 사용해야 한다. [E17]

프로토콜 거버넌스는 ETH 보유량에 따른 온체인 투표가 아니다. 누구나 EIP를 제안할 수 있고, 연구자·클라이언트 팀·앱 개발자·검증자·노드 운영자가 오프체인 토론과 구현으로 합의를 형성한다. 최종적으로 노드 운영자가 새 소프트웨어를 채택해야 하므로 재단이나 core developer가 법적·기술적으로 단독 강제하는 구조는 아니다. 장점은 단순 지분 과두제를 피하고 숙고할 수 있다는 것이고, 단점은 비공식 영향력, 높은 기술 장벽, 책임 소재와 일정의 불명확성이다. [E18]

최신 상태를 계획과 구분해야 한다. Pectra(2025년 5월)와 Fusaka(2025년 12월)는 메인넷 구현 완료다. 그러나 2026년 11월 17일 현재 다음 업그레이드 Glamsterdam은 Sepolia에서 시험됐을 뿐이다. EIP-8037/8038의 기존 계약 호환성 문제가 발견되어 Hoodi 활성화가 연기됐고, 메인넷 날짜도 없다. ePBS, block-level access lists, 200M gas 목표를 현재 메인넷 기능으로 표현하면 잘못이다. [E19]

## 6. 보안·운영·집중 위험

### 강점

- 2015년 genesis 이후 공식 기록상 전체 체인이 완전히 멈춘 사례는 없었다. 2023년 5월 두 차례 finality가 약 25분과 64분 지연됐지만 블록과 거래 처리는 계속됐고 자동 회복했다. 이는 다중 클라이언트의 복원력을 보여준다. [E20]
- PoS의 slashing·inactivity leak, 여러 EL/CL 구현, 공개 사양과 광범위한 감사·버그바운티는 방어층을 겹친다.
- L1에서 앱이나 토큰 발행 허가는 필요 없다. 검증 노드는 자신이 직접 규칙을 확인할 수 있다.

### 주요 위험

- **스테이킹 집중**: 풀·거래소·custodian, 공통 클라우드가 검열이나 동시 장애의 경로가 될 수 있다. 지분 토큰화·restaking은 상관 위험을 늘릴 수 있다.
- **클라이언트 버그**: 2023 finality 지연은 “서로 다른 구현”이 필요함을 입증했지만 동시에 소프트웨어 버그가 결제 최종성을 늦출 수 있음을 보여줬다. [E20][E21]
- **MEV와 블록 빌더 집중**: off-protocol proposer-builder separation은 효율을 높이는 대신 builder/relay 집중과 검열 위험을 만든다. ePBS·inclusion list는 아직 메인넷 완료 기능이 아니다. [E22]
- **L2·브리지 위험**: L2가 싸고 빠르더라도 중앙 시퀀서, 증명 지연, admin key, 브리지 계약이 L1에 없는 추가 실패 지점이다. 사용자는 체인별 출금·강제 포함 경로를 확인해야 한다. [E08]
- **상태 성장과 노드 부담**: L1 처리량을 올릴수록 SSD·RAM·대역폭 요구가 커져 자가 검증 참여를 약화시킬 수 있다. Ethereum이 gas limit을 신중히 올리는 이유다. [E14]
- **거버넌스·업그레이드 위험**: 지속적 hard fork는 개선 속도를 주지만, 계약 호환성·클라이언트 업데이트·사회적 합의 실패 가능성을 동반한다. Glamsterdam 지연이 현재 사례다. [E19]
- **애플리케이션 의존성**: 오라클·스테이블코인 발행자·관리자 키·프런트엔드가 검열되거나 실패해도 L1 합의가 이를 자동으로 해결하지 않는다.

## 7. 다른 네트워크와의 비교

| 항목 | Ethereum | Bitcoin | Solana | Avalanche C-Chain / L1 |
|---|---|---|---|---|
| 주목적 | 범용 스마트계약과 공용 정산·DA, L2 생태계 | 검열 저항적 가치 이전·희소 자산 | 단일 고성능 상태 머신과 빠른 앱 실행 | 빠른 EVM C-Chain + 맞춤형 독립 L1 |
| 합의·최종성 | PoS Gasper; 12초 슬롯, 정상 finality는 대략 두 에폭 규모 | PoW; 평균 약 10분/블록, 확정은 누적 confirmation에 따른 확률적 신뢰 | PoS; 2026년 Alpenglow/Votor 전환 상태, 공식 설명상 약 150ms 목표/구현 | Snowman 계열 반복 샘플링; 공식 문서상 C-Chain sub-second 확률적 finality |
| 확장 방식 | L1 용량 증가 + rollup/L2 + blobs/PeerDAS | 보수적 L1 + Lightning 등 | 높은 단일 L1 실행 성능·병렬화 | C-Chain 및 여러 독립 L1로 수평 확장 |
| 개발 환경 | 가장 넓은 EVM·Solidity 도구 및 표준, 다수 L2 | Script는 의도적으로 제한적 | SVM/Rust 중심, 빠른 신규 개발자 성장 | EVM 호환, Solidity 이식성 + 맞춤 VM |
| 주요 장점 | 조합성, 도구·유동성, 다중 클라이언트, 정산 중립성 | 단순한 목적, 고정 21M 공급, 보수적 변경, 광범위한 full-node 검증 | 낮은 지연·높은 실측 처리량, 단일 체인 UX | 빠른 finality, 앱별 체인·validator·gas 구성 가능 |
| 주요 단점 | L1/L2/브리지 복잡성, finality 지연, stake·MEV·L2 운영자 집중 | 느린 확정, 제한된 온체인 프로그래밍, mining pool·에너지 집중 | 고성능 장비·네트워크 요구, stake·호스팅 집중과 과거 중단 이력 | 체인별 validator·보안이 분절될 수 있고 Primary Network minimum 2,000 AVAX 진입장벽 |

비교 수치는 같은 정의가 아니다. Bitcoin의 “10분”은 평균 블록 간격이고 최종성 보장이 아니다. Solana 공식 2026년 11월 snapshot은 650 consensus validators, Nakamoto coefficient 18, 73% stake를 제시하지만 재단 분류·측정법에 따른다. 2026년 9월 성능 보고는 200ms target slot, 2024년 2월 이후 100% uptime을 주장한다. Avalanche의 sub-second finality 역시 자체 프로토콜 조건과 확률적 안전성에서 나온다. 이 수치를 이더리움의 12초 슬롯이나 checkpoint finality와 일대일 TPS/latency 순위로 만들면 오해가 생긴다. [E23][E24][E25]

또한 2026년 11월 Solana의 공식 문서는 Alpenglow의 Votor가 Tower BFT+PoH의 합의 투표 계층을 대체했다고 설명하지만 Rotor는 아직 계획 단계라고 구분한다. 네트워크 간 비교는 빠르게 바뀌므로 해당 날짜의 구현 상태를 다시 확인해야 한다. [E24]

## 8. ETH는 네트워크에서 무엇을 하는가

ETH는 단순 “주식”도, 프로토콜 거버넌스 표도 아니다.

1. **gas 자산**: L1 거래와 계약 실행의 base/priority fee를 지불한다.
2. **보안 담보**: 검증자가 ETH를 예치하고 보상·패널티·slashing을 받는다.
3. **결제·회계·담보 자산**: 앱과 DeFi에서 결제, 담보, 유동성 자산으로 쓰인다. 이는 앱 수준 사용이며 프로토콜이 무위험성을 보증하지 않는다.
4. **L2 자산**: 많은 rollup이 ETH를 gas 또는 브리지 자산으로 쓰지만 모든 L2가 반드시 ETH만 gas로 쓰는 것은 아니다.
5. **가치 포착**: EIP-1559 base fee와 blob fee 소각은 사용 수요를 ETH 공급에 연결하고, priority fee·issuance는 검증자 보상으로 간다.

ETH 공급은 Bitcoin처럼 고정 상한이 없다. PoS 보상 발행은 공급을 늘리고 base fee 소각은 줄인다. 따라서 시기별로 순인플레이션 또는 순디플레이션이 될 수 있다. L2 거래 증가가 L1 blob 수요와 ETH 소각으로 얼마나 이어지는지는 blob 가격·용량·수요에 달려 있으며 자동적인 가격 상승 관계가 아니다. [E11][E26]

## 9. 종합 장단점

### 장점

- 성숙한 범용 스마트계약 플랫폼과 가장 넓은 EVM 도구·표준 호환성
- L1의 보수적 정산과 L2의 저비용 실행을 분리한 확장 전략
- 여러 독립 실행·합의 클라이언트가 주는 소프트웨어 복원력
- PoS의 명시적 finality와 경제적 slashing
- 누구나 앱·노드·EIP에 참여할 수 있고 단일 온체인 지분투표가 아닌 다중 이해관계자 거버넌스
- 실사용과 수수료가 ETH gas·staking·소각에 연결되는 명확한 네이티브 토큰 기능

### 단점

- L1, 수십 개 L2, 브리지, 지갑 네트워크 선택이 만드는 사용자·개발자 복잡성
- 고성능 단일 L1보다 느린 L1 확정과 제한된 직접 처리량
- solo validator의 32 ETH 및 장비 부담, 스테이킹 풀·사업자 집중
- builder/relay, RPC, 오라클, 스테이블코인, L2 sequencer 등 프로토콜 밖 집중점
- 업그레이드가 잦고 복잡해 계약 호환성과 운영 리스크가 지속됨
- L2가 커질수록 사용자 활동과 L1 수수료·ETH 소각 사이의 경제적 연결이 단순하지 않음

## 10. 확인된 사실·추론·미확인

### 확인된 사실 (`VERIFIED_FACT`)

- EL/CL 분리, 12초 슬롯·32슬롯 에폭, 32 ETH 최소, 2/3 finality 규칙 [E01][E02]
- Pectra 이후 선택형 validator 최대 유효 잔액 2,048 ETH [E04]
- 2026-10-31 44.2M ETH(유통량 36.1%) 스테이킹이라는 명시된 집계 [E09]
- 2026-11-17 데이터셋상 L1 2.06M tx/day, L2 21.40M tx/day [E06]
- 2026-11-16 ETHBEAT rollup TVS $26.79B [E08]
- Glamsterdam Hoodi·mainnet 미활성화 및 호환성 검토로 지연 [E19]

### 근거 있는 추론 (`SUPPORTED_INFERENCE`)

- 이더리움은 단일 체인 속도보다 공용 정산·검증 가능성과 생태계 호환성을 우선하는 설계다.
- 거래 대부분이 L2로 이동할수록 사용성은 좋아지지만, 보안 가정과 유동성·UX가 체인별로 분절된다.
- 검증자 키 수 증가만으로 탈중앙화가 좋아졌다고 결론 낼 수 없다. 사업자·클라우드·클라이언트 집중을 함께 봐야 한다.
- 낮은 수수료는 사용자 효율을 높이지만 fee burn과 검증자 수익을 줄일 수 있어 ETH 가치 포착은 수요·용량·발행의 함수다.

### 미확인·추가 조사 (`UNVERIFIED` / `NEEDS_REVIEW`)

- 2026-11-17 시점의 정확한 독립 node operator 수와 지리·클라우드 분포: 검증자 주소와 운영 실체의 일대일 대응이 없고 공개 대시보드가 추정한다.
- 각 staking pool의 최종 수익 소유자·운영 통제권과 실질 Nakamoto coefficient: entity tagging 방법론에 민감하다.
- “모든 이더리움 L2”의 통합 TPS·수수료: L2 포함 기준, failed/internal operation 처리, UOPS/TPS 정의가 데이터 제공자마다 다르다.
- Glamsterdam의 최종 EIP 구성과 메인넷 일정: 2026-11-19 ACDE 이후 변경될 수 있어 기준일 현재 확정할 수 없다.

## 11. 한계

- 네트워크 상태·수수료·stake share는 계속 변하며 이 보고서는 2026-11-17 snapshot이다.
- Ethereum Foundation/ethereum.org, Solana Foundation, Avalanche 문서는 각 네트워크의 구조와 공식 상태를 확인하는 1차 자료지만 자기 네트워크의 성능·안전성에 대한 독립 검증은 아니다.
- growthepie, ETHBEAT, Rated, Electric Capital은 공개 방법론의 독립 데이터 제공자지만 인덱싱·entity tagging·체인 분류 한계가 있다.
- 거래 수는 사용자 수, 경제적 거래 수, 결제 건수와 같지 않으며 wash/bot/batch/internal operation을 완전히 구분하지 않는다.
- 한국 법률·규제는 질문과 직접 관련이 없어 억지로 연결하지 않았다.

---

## 근거 목록 및 접근 기록

검색·조회 시간: **2026-11-17 07:31~07:39 UTC (16:31~16:39 KST)**. 검색 결과 요약은 후보 탐색에만 썼고, 아래 URL의 본문을 열거나 검색 도구가 추출한 해당 본문을 확인했다. 별도 PDF·JSON Evidence 파일은 만들지 않았으며, 이 문서의 발췌는 모두 의역했다.

- **[E01]** Ethereum.org, [Proof-of-stake](https://ethereum.org/developers/docs/consensus-mechanisms/pos/) — 공식 기술문서; 32 ETH, 슬롯·에폭, attestation, 2/3 finality, slashing. 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E02]** Ethereum.org, [Node architecture](https://ethereum.org/developers/docs/nodes-and-clients/node-architecture/) 및 [Validator FAQ](https://launchpad.ethereum.org/en/faq) — EL/CL/validator 역할과 단일 Ethereum 구조. 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E03]** Ethereum.org, [Why build on Ethereum](https://ethereum.org/latest/why-build-on-ethereum) — 범용 정산·개발 특성 및 운영 이력에 대한 프로젝트 측 설명. 조회 2026-11-17. `CONTENT_VERIFIED`; 독립 성능 검증 아님.
- **[E04]** EIP-7251, [Increase the MAX_EFFECTIVE_BALANCE](https://eips.ethereum.org/EIPS/eip-7251) 및 Ethereum.org [Pectra MaxEB](https://ethereum.org/roadmap/pectra/maxeb/) — 32 ETH minimum, 2,048 ETH maximum과 consolidation. 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E05]** Ethereum.org, [Scaling Ethereum](https://ethereum.org/roadmap/scaling/) — rollup, blob, DAS와 중앙 sequencer의 한계. 페이지 최종 갱신 2026-10-22; 조회 2026-11-17. `CONTENT_VERIFIED`; 미래 수치는 로드맵 목표.
- **[E06]** growthepie, [Is Ethereum scaling through L2s?](https://www.growthepie.com/answers/is-ethereum-scaling-through-l2s) — 2026-11-17 UTC 최신 완료일 데이터, L1/L2 거래 및 Mgas/s, 공개 timeseries 방법론. 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E07]** Ethereum Institutional, [State of the Ledger](https://www.ethereuminstitutional.org/research/state-of-the-ledger) — Token Terminal read 2026-11-05, 2026년 1~10월 평균 거래·median fee 방법론. 조회 2026-11-17. `CONTENT_VERIFIED`; Ethereum 생태계 발행 2차 분석.
- **[E08]** ETHBEAT, [Value Secured](https://ethbeat.org/layer2s/tvs) 및 [Activity](https://ethbeat.org/layer2s/activity), [Linea risk analysis](https://ethbeat.org/layer2s/projects/linea) — 2026-11-16 TVS와 L2 위험 분류. 조회 2026-11-17. `CONTENT_VERIFIED`; 프로젝트별 위험은 개별 확인 필요.
- **[E09]** Ethereum Institutional, [State of the Ledger](https://www.ethereuminstitutional.org/research/state-of-the-ledger) — 2026-10-31 44.2M ETH, 36.1% staked. 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E10]** Rated Network, [Ethereum Mainnet pool explorer](https://explorer.rated.network/?network=mainnet&page=1&pageSize=15&poolType=all&timeWindow=all&view=pool) — pool/entity attribution shares. 조회 2026-11-17. `CONTENT_VERIFIED`; attribution 추정치.
- **[E11]** Ethereum.org, [Gas and fees](https://ethereum.org/developers/docs/gas/) 및 [EIP-1559](https://eips.ethereum.org/EIPS/eip-1559) — gas 산식, base fee burn, priority fee. 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E12]** Ethereum.org, [Danksharding](https://ethereum.org/roadmap/danksharding/) — EIP-4844와 full Danksharding의 100,000+ TPS 목표. 최종 갱신 2026-10-22; 조회 2026-11-17. `CONTENT_VERIFIED`; `SUPPORTED_INFERENCE/PROJECT_ROADMAP` for future performance.
- **[E13]** growthepie, [Are Ethereum L2 fees getting cheaper?](https://www.growthepie.com/answers/are-ethereum-l2-fees-getting-cheaper) 및 [Transaction costs](https://www.growthepie.com/fundamentals/transaction-costs) — 2026-10 cross-L2 monthly median 0.19¢, 2026-11-16 L1 daily median $0.08. 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E14]** EIP-7870, [Hardware and Bandwidth Recommendations](https://eips.ethereum.org/EIPS/eip-7870) 및 Ethereum.org [Run a node](https://ethereum.org/developers/docs/nodes-and-clients/run-a-node/) — 노드·validator 권장 사양. 조회 2026-11-17. `CONTENT_VERIFIED`; 권고이지 합의 규칙 아님.
- **[E15]** Ethereum.org, [Client diversity](https://ethereum.org/developers/docs/nodes-and-clients/client-diversity) — 1/3·2/3 client bug 위험. 페이지 최종 갱신 2026-02-23; 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E16]** Ethereum.org, [Smart contract security](https://ethereum.org/developers/docs/smart-contracts/security) — 앱·관리자·거버넌스 계약 위험. 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E17]** Electric Capital, [Developer Report](https://www.developerreport.com/developer-report) 및 2024 report를 인용한 [The Block 보도](https://www.theblock.co/news/business/2024-12-12-electric-capital-report-shows-solana-as-the-top-ecosystem-for-new-developers-in-2024-330627) — 2024년 공개 개발자 방법론·순위. 조회 2026-11-17. `CONTENT_VERIFIED`; 2024 snapshot, 일부 수치는 2차 교차확인.
- **[E18]** Ethereum.org, [Ethereum Governance](https://ethereum.org/governance/) 및 [EIPs](https://ethereum.org/eips) — 오프체인 거버넌스와 이해관계자·채택 절차. 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E19]** Ethereum Foundation Blog, [Glamsterdam EIP-8037/EIP-8038 update](https://blog.ethereum.org/en/2026/11/06/glamsterdam-8037-8038) 및 [Hoodi postponed](https://blog.ethereum.org/2026/10/22/glamsterdam-hoodi-delay) — 2026-11-09 update까지 반영, Hoodi 연기·mainnet 미정. 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E20]** Ethereum.org, [Why build on Ethereum](https://ethereum.org/latest/why-build-on-ethereum) — 2015 이후 full halt 없음, 2023년 약 25·64분 finality 지연. 조회 2026-11-17. `CONTENT_VERIFIED`; 공식 생태계 자료.
- **[E21]** Ethereum.org, [Client diversity](https://ethereum.org/developers/docs/nodes-and-clients/client-diversity) — 다중 구현의 장애 격리 효과. 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E22]** Ethereum.org, [A more secure Ethereum](https://ethereum.org/roadmap/security/) — off-protocol PBS 집중 위험, ePBS·FOCIL 진행 상태. 조회 2026-11-17. `CONTENT_VERIFIED`; 일정은 추정.
- **[E23]** Bitcoin.org, [How Bitcoin works](https://bitcoin.org/en/how-it-works) 및 Bitcoin Developer Guide, [Payment processing](https://developer.bitcoin.org/devguide/payment_processing.html) — PoW, 평균 10분 confirmation과 확률적 누적 신뢰. 조회 2026-11-17. `CONTENT_VERIFIED`.
- **[E24]** Solana, [Network Research](https://solana.com/research), [Validators](https://solana.com/validators), [Consensus comparison](https://solana.com/uk/developers/migrate-to-solana/consensus) — 2026-09/11 snapshot, 650 validators, Nakamoto 18, 73% stake, Alpenglow/Votor 및 Rotor 미구현 구분. 조회 2026-11-17. `CONTENT_VERIFIED`; Solana 측 성능 주장.
- **[E25]** Avalanche Builder Hub, [Consensus protocols](https://docs.avax.network/docs/nodes/architecture/consensus), [Primary Network](https://docs.avax.network/docs/primary-network), [Performance](https://docs.avax.network/solutions/performance) — Snowman, C-Chain EVM, 2,000 AVAX, sub-second 공식 주장. 조회 2026-11-17. `CONTENT_VERIFIED`; 프로젝트 측 성능 주장.
- **[E26]** Ethereum.org, [ETH supply and issuance](https://ethereum.org/what-is-ether/supply/) 및 [What is Ether](https://ethereum.org/what-is-ether) — gas, staking, issuance·burn, 비고정 공급. 조회 2026-11-17. `CONTENT_VERIFIED`.

### 접근 제한·재현 메모

- Beaconcha.in API `/api/v1/epoch/latest`와 `/api/v1/ethstore/latest`는 2026-11-17 07:37:53 UTC에 API key 없이 호출했으나 `Unauthorized`를 반환했다. 따라서 그 API의 실시간 validator count를 인용하지 않았다 (`ACCESS_RESTRICTED`).
- Publicnode Beacon API의 finality checkpoint는 2026-11-17 07:38:01 UTC에 응답했지만, 단일 시점 checkpoint는 본 평가의 비교 결론에 필요하지 않아 수치 본문에서 제외했다.
- 기존 L2BEAT URL은 조회 도구에서 ETHBEAT로 리디렉션되었고 직접 fetch가 실패했다. 검색을 통해 현재 ETHBEAT 공식 페이지를 확인했다. 데이터 제공자의 명칭·방법론 변경 가능성을 한계로 남겼다.
- 실시간 대시보드 값은 재조회 시 변할 수 있다. 재현 시 URL, UTC 기준 완료일, 체인 포함 기준, median/mean, transaction/UOPS/TPS 정의를 함께 고정해야 한다.
