# Architecture

```text
User question / PDF / official URL
              ↓
        SKILL.md router
              ↓
  methodology + jurisdiction references
              ↓
  Evidence records → Findings → Report
              ↓           ↓         ↓
 validate_sources   cross-links   KO report + EN summary
              └──── validate_report ────┘
```

에이전트의 판단이 필요한 분석과 결정적인 구조 검증을 분리한다. 스키마는 교환 계약이고 Python 스크립트는 외부 패키지 없이 핵심 불변조건을 검사한다. URL live check는 네트워크 제한과 공식 사이트의 자동 접근 차단 때문에 선택 기능이다.

