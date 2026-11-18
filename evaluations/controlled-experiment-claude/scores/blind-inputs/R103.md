# USDC 안전성 분석 (기준일: 2026-11-18)

**결론부터:** USDC는 공식 자료상 준비자산 구조와 공개 수준이 비교적 높은 편입니다. 그래도 안전을 보장하지 않고, 아래 위험이 남습니다.

## 0. 검증 수준과 한계

- 이 보고서는 웹 검색과 페이지 조회로 만들었습니다. 자동 조회 도구의 요약에 의존했고, 원문 PDF 대조(`verify_evidence.py`)는 하지 않았습니다.
- 그래서 핵심 주장은 대부분 `VERIFIED_FACT`가 아니라 `NEEDS_REVIEW`입니다. 투자나 운용 결정 전에 원문을 직접 확인하세요.
- Circle 투명성 페이지에서는 USDC 유통량 수치가 읽히지 않았습니다. 그래서 준비금 규모와 유통량을 비교한 숫자는 제시하지 않습니다.
- 검색 결과에는 날짜가 어긋나는 2차 자료가 섞여 있었습니다. 예를 들어 2025년 2월 수치와 날짜 불명의 $34.5B 수치가 있었는데, 이 둘은 인용하지 않습니다.

## 1. 발행사와 법적 구조

| 항목 | 내용 | 근거 / 상태 |
|---|---|---|
| 주 발행 주체 | Circle Internet Financial, LLC | [USDC Terms](https://www.circle.com/legal/usdc-terms), 2026-10-15 개정판 / 발행사 자료 |
| 유럽 | Circle Internet Financial Europe SAS가 "dual issuer"로 명시. 유럽경제지역(EEA) 보유자는 MiCA 백서를 따름 | 같은 문서 |
| 싱가포르 | Circle Internet Singapore Pte. Ltd.가 계약 상대방 | 같은 문서 |
| 미국 신탁은행 | OCC가 2026-07-10 First National Digital Currency Bank, N.A.(Circle National Trust)를 최종 승인 | [Fintech Global](https://fintech.global/2026/07/10/circle-wins-occ-approval-for-national-trust-bank/) 등 2차 보도 |

- 최종 승인된 신탁은행의 초기 업무는 Circle 및 계열사를 위한 수탁입니다. 준비금 운용은 향후 과제로 보도됐습니다.
- 이 신탁은행이 USDC 발행사가 된 것은 아니라는 보도가 있습니다.
- OCC 1차 문서는 확인하지 못했습니다.

## 2. 준비자산, 보관, 상환, 발행·소각

**준비자산**
- 약관은 USDC가 미국 달러 표시 자산으로 "fully backed"이고, 규제 대상 미국 기관에서 Circle 고유 자금과 분리된 계좌에 보관된다고 밝힙니다.
- [Circle 투명성 페이지](https://www.circle.com/transparency)에 따르면 준비자산 대부분은 BlackRock이 운용하는 Circle Reserve Fund(USDXX)입니다. 이는 단기 미국 국채와 익일물 국채 환매조건부(repo)를 담는 2a-7 정부 MMF입니다.
- 나머지는 현금이고, 주로 대형 은행에 예치돼 있습니다.
- 준비자산 구성표 기준일은 2026-11-16으로 표시됩니다.
- 수탁기관과 은행 이름은 해당 페이지에서 확인되지 않았습니다.

**상환**
- Circle(또는 지정 계열사)은 1 USDC를 1 USD로 상환하겠다고 약속합니다. 단, 약관, 법령, 수수료 조건이 붙습니다.
- 직접 상환은 Circle Mint 계정 보유자(User Type A)만 할 수 있습니다. 일반 보유자는 거래소 같은 중개자를 거치거나 계정을 개설해야 합니다.
- 규제당국이나 법원의 제한이 있으면 상환이 제한될 수 있습니다.
- 의심 거래로 판단되면 상환이 지연될 수 있습니다.
- 약관에 고정된 정산 기한은 없습니다.
- **핵심 유의점:** "1:1 상환 약속"은 모든 보유자가 언제든 직접 현금화할 수 있다는 뜻이 아닙니다.

**발행·소각**
- 약관은 USD를 USDC로 토큰화하고 상환하는 흐름을 설명합니다.
- 온체인 mint/burn 구조는 약관에 설명돼 있지 않습니다.
- 컨트랙트의 minter 권한은 masterMinter가 관리합니다(3절 참고).

**파산·도산 시 처리**
- 약관은 도산 시 처리를 직접 다루지 않습니다.
- 계정 분리 문구와 뉴욕 고지 문구(보증 또는 신탁 계좌가 모든 손실을 충당하지 못할 수 있다는 내용)가 있을 뿐입니다.
- 도산 시 보유자의 법적 순위는 추가 법률 검토 사항(`NEEDS_REVIEW`)입니다.

## 3. 스마트계약과 동결 권한

[circlefin/stablecoin-evm README](https://github.com/circlefin/stablecoin-evm) 기준입니다. 체인마다 배포 상태가 다를 수 있습니다.

- **구조:** FiatTokenV2_2 로직 컨트랙트와 FiatTokenProxy를 쓰는 업그레이드 가능 프록시 구조입니다. 업그레이드 권한은 `proxyOwner`에게 있습니다.
- **blacklister:** 지정한 주소가 토큰을 보내거나 받지 못하게 막을 수 있습니다.
- **pauser:** 컨트랙트 전체의 전송을 중지할 수 있습니다.
- **masterMinter:** minter 목록과 발행 한도를 관리합니다.
- **owner:** blacklister, pauser, masterMinter 같은 역할 주소를 변경할 수 있습니다. `proxyOwner`는 바꿀 수 없다고 README는 설명합니다.
- **약관상 권한:** Circle은 의심되는 불법 활동이 있으면 주소를 차단하고, Circle이 수탁하는 주소는 일시 또는 영구 동결할 수 있습니다. 법적 명령이 있으면 동결하고 관련 USD를 제출할 수 있습니다.
- **마이그레이션:** Circle은 다른 블록체인이나 프로토콜로 USDC를 이전할 권리를 가집니다. 포크가 발생하면 지원 여부를 Circle이 결정합니다.
- **한계:** README에는 감사 보고서가 나열돼 있지 않습니다. 컨트랙트 감사 이력은 별도로 확인해야 합니다.

즉 USDC는 탈중앙·검열 불가 자산이 아니라 중앙 통제형 자산입니다. 키 탈취, 내부 오류, 법적 명령, 오탐 차단이 모두 실제 위험입니다.

## 4. Attestation과 audit 구분

[Circle 설명](https://www.circle.com/blog/how-to-build-trust-usdc-audits-and-attestations) 기준입니다.

| | Attestation(증명) | Audit(감사) |
|---|---|---|
| 주기 | 월간 | 연간 |
| 수행 | 회계법인 | 회계법인(Circle 재무제표 감사) |
| 확인 대상 | 준비금 계좌 잔액과 온체인 USDC 총량. 준비금이 유통량 이상인지 확인 | 재무제표 전체와 재무보고 내부통제 테스트 |
| 의미 | 특정 시점의 한정된 확인 | 더 넓은 범위 |

- Circle 스스로 attestation은 full audit이 아니라고 밝힙니다.
- 투명성 페이지의 최신 월간 보고서는 2026년 9월분(보고서 날짜 2026-09-26)입니다. 10~12월분은 아직 링크되지 않았습니다.
- 그 페이지는 월간 보증 제공자를 "Big Four"라고만 적고 이름은 밝히지 않았습니다.
- Deloitte가 Circle의 재무제표 감사인이라는 점은 확인됐지만, 월간 attestation 수행자가 Deloitte인지는 이번 조회에서 확인하지 못했습니다.
- attestation이나 audit이 있다고 해서 시장 위험, 은행 위험, 운영 위험이 없다는 뜻은 아닙니다.

## 5. 위험 요인

| 위험 | 내용 |
|---|---|
| 디페깅 | 준비자산이 양호해도 상환 접근성이 제한된 사용자는 2차 시장 가격에 의존합니다. 은행 위기나 도산 우려가 나오면 가격이 일시적으로 1달러 밑으로 갈 수 있습니다. 2023년 3월 SVB 사태가 이런 사례입니다. 이 사례는 일반 지식이며 이번 조회에서 재검증하지 않았습니다. |
| 유동성 | 준비금 대부분이 MMF와 현금성 자산이라 비교적 유동적입니다. 다만 대규모 동시 상환 시 은행 송금 마감 시간과 은행 영업일의 제약이 있습니다. |
| 신용·거래상대방 | 은행 예치금, BlackRock MMF, repo 거래상대방, 수탁기관이 모두 신용 위험입니다. |
| 운영 | 키 관리, 프록시 업그레이드 권한, 블록체인별 브리지 문제, 발행사 시스템 장애가 있습니다. |
| 법적·제재 | 동결, 차단, 상환 제한이 있을 수 있습니다. 도산 시 보유자 순위는 불명확합니다. |
| 정책 | 아래 6절의 규제 변화에 따라 구조와 권리가 바뀔 수 있습니다. |

## 6. 규제 상태

**미국 (GENIUS Act)**
- 검색된 보도에 따르면 OCC가 2026-10-21 GENIUS Act 시행 최종 규칙을 발표했고, 시행일은 2027-01-18입니다.
- 자본금 하한 $5M, 이자 지급 금지, 보상 프로그램 처리 등이 보도됩니다.
- 재무부와 OCC의 합동 BSA/AML/OFAC 규칙은 아직 미확정이라는 보도가 있습니다.
- 법정 규칙 기한(7월 18일)은 넘겼지만 시행일은 그대로라고 보도됩니다.
- 이 내용은 모두 2차 보도입니다. 연방관보와 OCC 원문 확인이 필요합니다(`NEEDS_REVIEW`).
- USDC가 새 체제의 허가 대상 지급 스테이블코인 발행사 요건을 어떻게 충족할지는 이번 조회에서 확인하지 못했습니다.
- 시행일 전에는 "법 제정(공포) 상태이고 일부 규칙이 확정된 단계"로 이해해야 하며, 현행 시행 완료로 보면 안 됩니다.

**EU**
- 약관에 따르면 Circle Internet Financial Europe SAS가 dual issuer이고, EEA 보유자는 MiCA 백서를 따릅니다.
- MiCA 인가와 e-money 지위 자체는 이번 조회에서 1차 확인하지 못했습니다.

## 7. 한국 이용자 유의사항

- **한국 법적 지위:** 이번 조회에서 USDC에 대한 한국 법령상 구체 규정은 확인하지 못했습니다. 한국 스테이블코인 발행 규제(디지털자산기본법 2단계)는 금융위와 한국은행의 이견으로 지연되고 있다는 보도만 있습니다. 법안 상태는 국회 의안정보시스템과 금융위 자료로 확인해야 합니다.
- **상환 접근성:** 한국 개인이 Circle Mint로 직접 상환할 수 있는지는 약관과 Circle의 지역 제한 정책을 확인해야 합니다. 국내 거래소 입출금과 원화 환전 경로에는 거래소 정책이 더해집니다.
- **외환·자금세탁방지:** 해외 송금, 해외 거래소 이용, 트래블룰, 외국환거래법상 신고 의무가 관련될 수 있습니다. 이 부분은 개별 사안 검토가 필요합니다.
- **세금:** 가상자산 과세 규정은 시행 시기와 요건이 바뀌어 왔습니다. 현재 상태는 이번 조회에서 확인하지 못했습니다.
- **동결 위험:** 제재나 사법 명령과 연결된 주소의 USDC가 동결되면 이용자가 구제받기 어려울 수 있습니다.
- **원화 스테이블코인 논의:** 한국의 법·제도 상황이 바뀌면 USDC 이용 환경도 바뀔 수 있습니다.

## 8. 실무 체크리스트

1. Circle 투명성 페이지에서 최신 월간 attestation PDF와 기준일, 수행 회계법인 이름을 직접 확인하세요.
2. USDC 약관의 최신 개정판과 지역별 제한을 확인하세요.
3. 사용하는 체인에서 공식 컨트랙트 주소와 blacklist, pause 정책을 확인하세요.
4. 거래소 입출금 정책과 상환 경로, 수수료를 확인하세요.
5. 대량 보유나 법인 사용이라면 변호사, 회계사, 세무사의 검토를 받으세요.
6. 한 스테이블코인, 한 체인, 한 거래소에 집중하지 않는 것이 위험 관리의 기본입니다.

## 9. 미확인 사항

- Circle 투명성 페이지의 USDC 유통량 수치
- 월간 attestation 수행 법인의 이름
- 한국 법령상 USDC의 구체적 지위와 현재 입법 상태
- 도산 시 보유자 순위
- OCC와 GENIUS Act 1차 문서
- MiCA 인가 상태

이 보고서는 정보 제공이며 법률 자문이나 투자 권유가 아닙니다.

Sources:
- [Circle USDC Terms](https://www.circle.com/legal/usdc-terms)
- [Circle 투명성 페이지](https://www.circle.com/transparency)
- [Circle: USDC 감사와 attestation](https://www.circle.com/blog/how-to-build-trust-usdc-audits-and-attestations)
- [circlefin/stablecoin-evm](https://github.com/circlefin/stablecoin-evm)
- [Fintech Global: Circle OCC 승인](https://fintech.global/2026/07/10/circle-wins-occ-approval-for-national-trust-bank/)
- [The Block: OCC GENIUS Act 최종 규칙](https://theblock.co/news/regulation/2026-10-21-occ-final-rule-implementing-trump-signed-genius-act-421470)
- [Circle: GENIUS Act readiness](https://www.circle.com/blog/circle-genius-act-readiness-and-path-forward)
