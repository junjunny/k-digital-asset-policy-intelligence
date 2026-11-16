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

