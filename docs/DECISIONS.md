# Decisions

## D-001 Skill-first

웹사이트나 별도 백엔드를 필수로 만들지 않는다. 핵심 산출물은 설치 가능한 폴더형 Agent Skill이다.

## D-002 Progressive disclosure

`SKILL.md`에는 라우팅과 규제 정확성 규칙만 두고, 상세 방법론·관할권·용어는 references로 분리한다.

## D-003 Dependency-light validation

기본 검증기는 Python 표준 라이브러리만 사용한다. JSON Schema는 상호운용을 위해 제공하되 실행에 `jsonschema`를 강제하지 않는다.

## D-004 Legal status as data

법률/정책의 차이를 서술 규칙에만 맡기지 않고 `legal_status` 필드와 시간 검증으로 표현한다.

## D-005 First case

공식 발행인 자료가 있고 한국 정책의 초기 사모사채 범위와 비교하기 좋은 EIB sterling digital bond를 선택했다. EU DLT Pilot 적용 사례라고 오인하지 않도록 발행일과 적용일을 분리했다.

## D-006 MIT

재사용과 공개 배포 목적에 맞춰 MIT License를 채택했다. 보고서의 제3자 원문은 복제하지 않고 짧은 발췌와 링크만 저장한다.

## D-007 Evidence v2

URL 접근과 내용 검증을 분리한다. 원문 추출과 발췌문 일치가 확인된 경우에만 `CONTENT_VERIFIED`를 부여하고, 문서와 추출문 해시를 기록한다. 동적 웹페이지는 문서 전체 해시가 바뀔 수 있으므로 해시만으로 의미 동일성을 단정하지 않는다.

## D-008 Normalized claims

한국어 키워드 대신 `claim_type`과 `legal_status` 호환성, `analysis_date`, 관할권, 공식 출처 유형을 검증한다. 의미적·법률적 정당성 전체를 자동화했다고 주장하지 않는다.

## D-009 Untrusted sources

다운로드한 HTML·PDF·텍스트는 신뢰하지 않는 데이터다. 스크립트·매크로·문서 속 명령을 실행하지 않고, 지시문 패턴은 경고만 기록한다. 접근 제한을 우회하지 않는다.

## D-010 Independent case

EIB와 다른 홍콩 정부 다중통화 디지털 녹색채권을 신규 연구질문으로 선택했다. 한국 공식 자료는 비교 기준으로 재사용하되 해외 사례·규제·분석은 새로 조사했다.

