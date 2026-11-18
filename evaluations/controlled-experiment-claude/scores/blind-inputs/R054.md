# USDC 안전성 분석 (기준일: 2026-11-18)

**결론부터 말하면, USDC가 안전하다고 보장할 수 없습니다.** 아래는 확인된 사실과 확인하지 못한 부분을 나눈 위험 요소 정리이며, 투자·보관 판단용 조언이 아닙니다.

## 0. 자료 한계

- Circle 투명성 페이지(준비자산 구성 기준일 **2026-11-16**)는 구성 항목만 확인됐고 금액 수치는 추출되지 않았습니다.
- 계약 구조, 한국 규제, 3분기 실적은 2차 자료에 의존했습니다. 공식 원문은 직접 확인하지 못했습니다.
- 3분기 실적 수치가 매체마다 달랐습니다. 분기말 유통량은 한 곳에서 "전년 동기와 같은 $73.9B", 다른 곳에서 "108% 증가 $73.7B"라고 했습니다. 어느 쪽이 맞는지 확정하지 못했습니다.
- Circle 개발자 페이지에는 에이전트에게 도구 설치를 지시하는 문구가 있었습니다. 이는 페이지 내용일 뿐이라 따르지 않았습니다.

## 1. 발행사와 법적 구조

- 발행 주체는 지역별로 나뉩니다. 이 부분은 Circle 약관과 MiCA 관련 자료로 확인했습니다.
  - **EEA 외 이용자**: Circle 약관(최종 수정 2026-10-15) 적용
  - **EEA 이용자**: MiCA 백서 적용
  - **싱가포르 이용자**: Circle Internet Singapore Pte. Ltd.와 계약
- 유럽에서는 프랑스 ACPR의 전자화폐기관(EMI) 인가로 MiCA 하에 USDC를 발행합니다. AMF 등록부에는 2026-04-23자 MiCA 인가가 표시된다고 합니다(2차 보도, 직접 확인 필요).
- 모회사 Circle Internet Group은 상장사(CRCL)입니다. 따라서 연간 감사 재무제표와 분기 공시가 존재합니다. 이 점은 제 기존 지식이며 이번에 재확인하지 않았습니다.
- USDC는 은행 예금이 아닙니다. 약관상 예금보험 대상이 아니고 이자도 없습니다.

## 2. 준비자산·보관·상환·발행·소각

- **구성**: 투명성 페이지 기준으로 대부분이 BlackRock이 운용하는 머니마켓펀드 **Circle Reserve Fund(USDXX)**에 있습니다. 나머지는 "세계 최대 은행 몇 곳"의 현금입니다. 세부 항목은 만기 3개월 미만 국채, 익일물 역레포, 은행 예금입니다.
- **분리 보관**: 약관은 준비금을 Circle 법인 자금과 분리된 계정에 이용자를 위해 보관한다고 명시합니다. 다만 **파산 시 처리 방식은 약관에 없습니다.** New York 관련 고지는 신탁이나 보증 계정이 모든 손실을 커버하지 못할 수 있다고 경고합니다.
- **발행·소각**: 발행과 소각은 Circle Mint 계정 기반이며, 발행 시 USDC가 생기고 상환 시 소각된다는 것이 일반적 구조입니다. 이번 조사에서는 이 절차의 공식 원문을 직접 확인하지 못했습니다.
- **상환**: 약관 기준은 다음과 같습니다.
  - 1 USDC당 1 USD로 상환하며 "해당되는 경우 수수료 제외"입니다.
  - **직접 상환은 Circle Mint 계정 보유자(자격 요건 충족자)만 가능합니다.** 일반 지갑 보유자는 거래소 등을 거쳐야 합니다.
  - 계정이 "정상 상태"여야 하고, 약관 위반이나 규제·법원 조치가 없어야 합니다.
  - 상환 소요 시간은 명시되어 있지 않습니다.
  - 의심 거래나 블록체인 포크·보안 사고 시 Circle이 상환을 지연하거나 중단할 수 있습니다.

## 3. Attestation과 Audit의 구분

| 구분 | 내용 | 한계 |
|---|---|---|
| **월간 준비금 attestation** | Circle 페이지는 Big Four 회계법인이 "준비자산 가치가 유통량보다 크다"는 점에 월간 제3자 확인을 제공한다고 합니다. 법인명은 페이지 추출본에 없고 보도상 Deloitte입니다. | 특정 기준일 시점의 주장(assertion)에 대한 제한적 확인입니다. 준비금 **전체에 대한 감사의견이 아니며**, 내부통제나 지속적 안전을 보증하지 않습니다. |
| **연간 재무제표 audit** | Circle 자체 재무제표에 대한 감사입니다. Deloitte가 FY2022부터 감사인이라고 Circle 페이지에 적혀 있습니다. | 회사 전체 재무에 대한 것이며 USDC 준비금 월별 구성을 대신하지 않습니다. |

최신 월간 보고서는 2026년 9월분까지 링크되어 있었습니다. 공개까지 시차가 있으므로 "오늘의 담보 상태"가 아니라 "과거 기준일의 상태"입니다.

## 4. 위험 요소

- **디페깅**: 2023년 3월 SVB 사태 때 준비금 일부가 묶이며 USDC가 1달러 아래로 크게 이탈했습니다(제 기존 지식). 은행 예금 비중이 있는 한 같은 유형의 위험은 남습니다.
- **유동성**: 대량 상환이 몰리면 MMF 환매와 은행 현금 인출 속도가 제약이 됩니다. 직접 상환 자격이 제한된 점도 위기 시 영향을 줍니다.
- **신용·거래상대방**: 은행 예금과 MMF 운용사에 대한 노출이 있습니다. 대부분을 한 MMF에 두는 구조는 집중도 위험이기도 합니다.
- **운영**: 상환 중단 조항이 약관에 있습니다. 3분기에 5% 인력 감축도 공시됐습니다(2차 보도). 수익은 금리에 민감합니다. 준비금 수익률이 3.5%로 하락해 준비금 수익이 8% 줄었다고 보도됐습니다.

## 5. 스마트계약과 동결 권한

- **확인된 것**: Circle 약관은 Circle이 주소를 차단하고 USDC를 동결할 수 있다고 명시합니다. 정부 명령이 있으면 동결하고 연계된 준비금 USD를 넘길 수 있습니다. 따라서 **USDC는 검열 저항적이지 않습니다.**
- **확인하지 못한 것**: 개발자 문서 페이지에는 프록시 업그레이드, 블랙리스트, 일시정지, 민터 권한 정보가 없었습니다. 일반적으로 USDC는 업그레이드 가능한 프록시와 블랙리스트·일시정지 기능을 가진 것으로 알려져 있으나, 이번에 검증하지 않았습니다. 각 체인 탐색기의 검증된 소스에서 직접 확인하세요.
- **브리지 토큰**: 체인별 주소가 다릅니다. 예를 들어 X Layer의 `USDC.e`는 Circle이 발행하지도 보증하지도 않는 브리지 표현입니다. 공식 주소표와 대조하세요.

## 6. 규제

- **EU**: MiCA 하에서 EMI 인가 발행입니다.
- **미국**: GENIUS Act 시행 규칙 제정이 진행 중입니다. Circle은 "전면 준수로 가는 경로"라고 설명합니다. 이는 Circle의 입장이며 최종 준수 여부는 확인하지 못했습니다. OCC와 재무부 규칙을 확인하세요.
- **제한 지역**: 쿠바, 이란, 북한 등 일부 지역은 약관상 제한됩니다.

## 7. 한국 이용자 유의사항

- **규제 미확정**: 디지털자산기본법은 2026년 4월 시점에 원화 스테이블코인 발행 주체(은행 51% 지분 논쟁) 때문에 지연됐다는 보도가 마지막이었습니다. 이후 상황은 확인하지 못했습니다. 외국 발행 스테이블코인은 국내 인가와 지점·법인이 요구될 수 있다는 초안이 있었고, 현재의 자유로운 유통이 바뀔 수 있다는 전망이 있습니다. 모두 2차 자료이며 금융위원회와 국회 자료로 재확인이 필요합니다.
- **상환 접근성**: 일반 개인이 Circle과 직접 상환 계약을 맺기는 현실적으로 어려울 수 있습니다. 대부분 거래소를 경유하므로 거래소 위험이 추가됩니다. 거래소의 상장 폐지나 입출금 중단은 USDC 자체와 별개 위험입니다.
- **세금·신고**: 가상자산 과세와 외환·해외 이체 신고는 시행 시기와 요건이 바뀌어 왔습니다. 이번에 확인하지 않았으니 세무 전문가나 국세청 자료로 확인하세요.
- **자기 보관 시**: 주소가 동결되면 복구가 어렵습니다. 전송 체인과 컨트랙트 주소를 잘못 선택해도 손실이 납니다.

## 8. 직접 확인할 항목

1. Circle 투명성 페이지의 최신 attestation PDF: 기준일, 법인명, 확인 범위 문구
2. SEC EDGAR의 Circle 10-Q·10-K: 유통량과 위험요인
3. 사용 체인의 USDC 컨트랙트 탐색기: 관리자 권한과 블랙리스트 기능
4. 금융위원회·국회의 디지털자산 관련 법안 최신 상태

## Sources

- [Circle Transparency](https://www.circle.com/transparency)
- [Circle USDC Terms](https://www.circle.com/legal/usdc-terms)
- [Circle USDC contract addresses](https://developers.circle.com/stablecoins/usdc-contract-addresses)
- [Circle: Transparency & stability](https://www.circle.com/blog/greater-transparency-for-usdc-reserves)
- [Circle: GENIUS Act readiness](https://www.circle.com/blog/circle-genius-act-readiness-and-path-forward)
- [Circle: One year of MiCA](https://www.circle.com/blog/one-year-of-mica-momentum-confidence-and-the-road-to-global-alignment)
- [Circle Q3 2026 results (Finviz)](https://finviz.com/news/415158/circle-reports-third-quarter-2026-results)
- [The Block: Circle Q3 2026](https://theblock.co/news/business/2026-11-04-circle-reports-865-million-in-q3-revenue-and-reserve-income-discloses-5-workforce-reduction-432671)
- [Blockworks: Circle taps Deloitte](https://www.blockworks.com/news/circle-taps-deloitte-as-new-auditor-doubles-down-on-proof-of-reserves)
- [Chakwon: Korea Digital Asset Basic Act delay](https://blog.chakwon.com/2026/04/17/korea-digital-asset-basic-act-stablecoin-sto-split/)
- [Seoulz: Korea stablecoin foreign entry](https://www.seoulz.com/korea-stablecoin-foreign-entry-2026/)
