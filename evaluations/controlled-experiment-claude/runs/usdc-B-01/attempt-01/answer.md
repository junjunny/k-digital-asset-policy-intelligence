# USDC 안전성 분석 (기준일: 2026-11-18)

**결론부터:** USDC는 규제된 발행사, 단기 국채·현금 중심 준비자산, 월별 제3자 확인(attestation)을 갖춘 편입니다. 그래도 **안전을 보장하지 않습니다.** 아래에 "이번 조회에서 직접 확인한 것"과 "확인하지 못했거나 제 배경지식인 것"을 나누어 적었습니다.

## 1. 발행사와 법적 구조
- 약관상 발행 주체는 **Circle Internet Financial, LLC**입니다. EEA 밖 이용자에게 적용되는 약관이며, **Circle Internet Financial Europe SAS**는 2024-07-01부터 "dual issuer"입니다. EEA 이용자는 별도의 USDC 백서가 적용됩니다. ([USDC 약관](https://www.circle.com/legal/usdc-terms))
- 준비자산은 Circle 법인 자금과 분리된 계좌에 보관한다고 약관에 적혀 있습니다.
- **약관에는 파산·청산 절차가 설명되어 있지 않습니다.** 보유자가 파산 시 준비자산에 어떤 우선권을 갖는지는 약관만으로 확인되지 않습니다.
- FDIC, SIPC 같은 예금자보호는 **없습니다**.
- 준거법은 델라웨어주법과 미국 연방법입니다.

## 2. 준비자산·보관·상환·발행·소각
- **구성:** Circle은 "현금 및 현금성 자산 100%"라고 밝힙니다. 대부분은 **Circle Reserve Fund(USDXX)**에 있습니다. SEC에 등록된 2a-7 국채 머니마켓펀드로, BlackRock이 운용하고 BNY가 수탁합니다. 나머지는 은행 현금이며 은행 이름은 공개 페이지에 없었습니다. ([Circle USDC](https://www.circle.com/usdc), [Transparency](https://www.circle.com/transparency))
- **집중도:** FY2025 10-K 발췌 기준 2025-12-31 현재 약 88%가 USDXX였습니다. 2차 출처 인용이라 원문 확인이 필요합니다. ([sec-api.io 요약](https://sec-api.io/insights/circle-crcl-q3-2026-earnings-usdc-reserve-income-lower-rates-and-the-arc-token-presale), [검색 결과](https://insights4vc.substack.com/p/inside-circles-stablecoin-economics))
- **상환:** 1 USDC = 1 USD를 약속하지만, 직접 상환은 **Circle Mint 계정 보유자(기관)만** 가능합니다. 개인은 거래소나 제휴 서비스를 거치며, 이때 가격은 시장 가격입니다.
  - 약관은 Circle이 시장가 $1을 보장하지 않는다고 명시합니다.
  - 상환은 규제·수사·법원 조치로 제한되거나, 사기 의심 시 지연될 수 있습니다.
- **발행·소각:** 발행은 USD 입금에 대응하고 소각은 상환에 대응하는 구조입니다. 이 부분은 약관 요약에 일반 원칙만 있고, 온체인 수치 검증은 하지 않았습니다.
- **유통량:** Circle 페이지는 2026-11-16 기준 약 $68.0B이라고 표시했습니다. 준비자산 금액 칸은 비어 있었습니다. 2차 출처의 다른 날짜 수치(5월 약 $76.5B 등)와 다르므로 최신 값은 직접 확인하세요.

## 3. Attestation과 Audit의 구분
| 구분 | 대상 | 내용 |
|---|---|---|
| **Attestation(확인/assurance)** | USDC 준비자산 | 월별, 빅4 회계법인, AICPA 확인 기준. "준비자산 가치가 유통량보다 크다"는 제3자 확인입니다. |
| **Audit(감사)** | Circle 재무제표 | Deloitte & Touche LLP가 FY2022부터 수행합니다. 이전에는 Grant Thornton이었습니다. |

- 준비자산 보고서는 **감사(audit)가 아닙니다.** Circle 페이지도 "audit"이라는 말을 재무제표 감사에만 씁니다.
- Circle 페이지는 준비자산 확인 법인을 "빅4 중 한 곳"이라고만 적었습니다. 2차 출처들은 Deloitte라고 하지만, 이번 조회에서 보고서 원문으로 확인하지 못했습니다.
- 링크가 열리는 최신 보고서는 **2026년 9월분**이었습니다. 보고 시점과 현재 사이에 공백이 있습니다.
- 일반적으로 attestation은 특정 시점의 잔액·유통량 비교 확인입니다. 내부통제의 전반적 유효성이나 보관 은행 건전성을 보증하지 않습니다.

## 4. 위험 요인
- **디페깅:** 2023년 3월 SVB 사태에서 USDC가 크게 이탈했습니다. 당시 준비자산 일부가 SVB에 있었고, 이후 정상화되었습니다. 이 내용은 제 배경지식이며 이번 조회에서 재확인하지 못했습니다. 현재 구조는 SVB 사태 이후 국채·MMF 중심으로 바뀌었지만, **이탈 위험이 사라졌다는 뜻은 아닙니다.**
- **유동성:** 대규모 동시 상환 시 MMF 환매와 은행 송금 속도가 상환 속도를 좌우합니다. 한국은행도 원화 스테이블코인과 관련해 준비자산 유동화 시점과 상환 요구 시점의 불일치(코인런)를 점검 대상으로 꼽았습니다. ([디지털데일리](https://www.ddaily.co.kr/page/view/2026071416154311294))
- **신용·집중:** 단일 펀드·운용사·수탁은행에 몰려 있고, 현금은 소수 대형 은행에 있습니다. 상대방 위험이 있습니다.
- **운영·사업:** 배급사(Coinbase 등)에 대한 수익 의존이 10-K에 위험요인으로 나옵니다. 비율은 출처마다 달라(56% vs 63%) 원문 확인이 필요합니다.
- **약관상 위험:** 온체인 전송은 되돌릴 수 없고, 잘못 보낸 USDC는 복구되지 않을 수 있습니다. 포크나 보안 문제 시 Circle이 중단(Downtime)하거나 다른 체인으로 이전할 수 있습니다.

## 5. 스마트계약과 동결 권한
- 약관상 Circle은 **주소 블록리스트와 동결**을 할 수 있습니다. 불법 의심 시 재량으로, 정부의 유효한 명령 시에는 의무적으로 할 수 있습니다. 거래 지연·중단 권한도 있습니다. ([USDC 약관](https://www.circle.com/legal/usdc-terms))
- 즉 **탈중앙 자산이 아니라 발행사 통제형 자산**입니다. 법적 요청이나 제재에 따라 내 지갑 잔액도 동결될 수 있습니다.
- 이더리움 USDC 주소는 `0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48`입니다. ([Circle 개발자 문서](https://developers.circle.com/stablecoins/usdc-contract-addresses))
- 업그레이드 가능 프록시, pause, 블록리스트, 발행·소각 권한은 제 배경지식입니다. 이번 조회에서 문서로 확인하지 못했으니 Etherscan의 컨트랙트와 Circle 개발자 문서에서 직접 확인하세요.
- 네이티브 발행 체인은 38개(2026-09-16 기준)입니다. 체인이 많을수록 브리지·체인별 운영 위험도 늘어납니다. 브리지 토큰은 네이티브 USDC와 위험이 다릅니다.

## 6. 규제
- **미국:** GENIUS Act가 2025-07 서명되었습니다. OCC가 2026-02-25 제안 규칙을 냈고 의견 마감은 2026-05-01이었습니다. 최종 규칙 확정과 시행일은 출처마다 달라 확인하지 못했습니다. Circle의 구체적 적용 상태도 확인하지 못했습니다. 2차 출처가 Circle National Trust의 OCC 승인(2026-07-10)을 언급하지만 독립 확인은 못 했습니다.
- **EU:** Circle France(EMI)가 MiCA 하에서 USDC·EURC를 발행합니다. 인가 시점은 출처마다 2024년과 2025년으로 엇갈립니다. 2026-07-01에 MiCA 경과기간이 끝났다는 보도가 있습니다.

## 7. 한국 이용자 유의사항
- 이번 조회에서 **해외 스테이블코인(USDC)의 국내 취급 요건을 직접 규율한 확정 법령은 확인하지 못했습니다.**
- 확인된 것은 입법 진행 상황입니다. 정부가 2026년 하반기에 '디지털자산기본법'을 추진하고 있고, 국경 간 스테이블코인 거래 규율은 2단계 입법과 연계하겠다고 했습니다. 11월 18일 현재 국회 심사 상황은 확인하지 못했습니다. ([데일리 기사](https://www.ddaily.co.kr/page/view/2026071416154311294), [비즈워치](https://news.bizwatch.co.kr/article/finance/2026/11/02/0050))
- 2024-07 시행된 가상자산이용자보호법은 최소 장치로 평가됩니다.
- 실무상 점검할 점:
  - **개인은 Circle에 직접 상환할 수 없는 경우가 많습니다.** 거래소나 제휴 서비스에 의존하므로 그 업체의 신뢰도가 별도 위험입니다.
  - 원화 환전 시 거래소 호가 이탈, 해외 송금 한도·신고, 트래블룰이 적용될 수 있습니다.
  - 세금과 외환 신고 의무는 별도로 확인해야 합니다. 이 답변은 법률·세무 자문이 아닙니다.

## 이번 조회의 한계
- 준비자산 보고서 원문, Reserve Fund 팩트시트, 10-K 원문, 금융위 보도자료는 직접 열람하지 못했습니다.
- 일부 수치는 신뢰도가 낮은 2차 사이트에서 왔고, 서로 어긋나는 부분은 위에 표시했습니다.
- 투자 전에는 Circle 투명성 페이지, 최신 attestation 원문, SEC 공시, 금융당국 자료를 직접 대조하세요.

Sources:
- [Circle USDC](https://www.circle.com/usdc)
- [Circle Transparency](https://www.circle.com/transparency)
- [USDC Terms](https://www.circle.com/legal/usdc-terms)
- [Circle 개발자 문서: 컨트랙트 주소](https://developers.circle.com/stablecoins/usdc-contract-addresses)
- [sec-api.io: Circle Q3 2026](https://sec-api.io/insights/circle-crcl-q3-2026-earnings-usdc-reserve-income-lower-rates-and-the-arc-token-presale)
- [Inside Circle's Stablecoin Economics](https://insights4vc.substack.com/p/inside-circles-stablecoin-economics)
- [디지털데일리](https://www.ddaily.co.kr/page/view/2026071416154311294)
- [비즈워치](https://news.bizwatch.co.kr/article/finance/2026/11/02/0050)
- [Circle MiCA 발표(BusinessWire)](https://www.businesswire.com/news/home/20240701820713/en/Circle-is-First-Global-Stablecoin-Issuer-to-Comply-with-MiCA-EU’s-Landmark-Crypto-Law)
- [Circle: MiCA 1년](https://www.circle.com/es/blog/one-year-of-mica-momentum-confidence-and-the-road-to-global-alignment)
