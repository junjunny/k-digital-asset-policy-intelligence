# Research Log

분석 기준일: 2026-11-16

## 사용 도구와 단계

1. 공식 웹 검색으로 HKMA, 홍콩 SFC, 국가법령정보센터, 금융위원회 자료를 탐색했다.
2. 검색 결과는 후보 탐색에만 사용하고 공식 원문 URL을 Evidence에 기록했다.
3. `scripts/verify_evidence.py`가 HTML과 PDF를 직접 내려받아 텍스트를 추출했다.
4. `relevant_excerpt`를 정규화한 원문과 대조하고, 응답 코드·콘텐츠 유형·최종 URL·문서 SHA-256·추출문 SHA-256·조회시각을 기록했다.
5. `scripts/validate_report.py`로 claim type, legal status, analysis date, 관할권, Evidence 연결을 검증했다.

## 독립성

기존 EIB 보고서의 문장을 복사해 사례를 바꾸지 않았다. 해외 사례와 해외 규제 자료는 홍콩 정부의 2024년 디지털 녹색채권, 홍콩 SFC circular, 2026년 HKMA 정책 발표를 새로 조사했다. 한국 비교 자료만 동일한 공식 법률·정책 원문을 재사용했다.

## 검증 한계

자동 검증은 문서 접근·텍스트 추출·발췌문 포함 여부를 확인한다. 발췌문의 법적 의미, 계약 전체, 규제 적용의 최종 판단은 자동화하지 않았다.

