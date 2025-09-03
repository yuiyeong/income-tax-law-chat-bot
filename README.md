# Tax Chat Bot

세금 관련 질의응답을 제공하는 간단한 대화형 챗봇입니다.
Streamlit 기반의 웹 UI로 빠르게 실행할 수 있으며, 모듈식 에이전트/상태 관리 구조로 확장과 유지보수가 용이합니다.

## 주요 기능

- Streamlit 웹 앱으로 손쉬운 실행과 배포
- 에이전트/상태/데이터 모듈 분리로 구조적 확장성
- 로컬 실행 및 패키지 설치 지원
- 개발 편의를 위한 ruff, pre-commit 구성

## 프로젝트 구조

- src/tax_bot
    - app.py: Streamlit 앱 엔트리 포인트
    - main.py: CLI/모듈 실행 진입점
    - agent.py: 챗봇 에이전트 로직
    - state_manager.py: 대화 상태 관리
    - data.py: 데이터 액세스/유틸리티
    - __init__.py: 패키지 초기화
- pyproject.toml: 의존성 및 빌드 설정
- poetry.lock: 잠금 파일(빌드 메타)
- .pre-commit-config.yaml: pre-commit 훅 설정
- ruff.toml: ruff 설정

참고: 실제 구현 세부는 각 소스 파일을 확인하세요.

## 요구 사항

- Python 3.12 이상 (권장: 3.12.11)
- pyenv로 Python 버전 관리
- OS: macOS/Linux/Windows

## 설치 및 실행

아래 예시는 pyenv를 사용하여 로컬 환경을 구성하는 방법입니다.

1) Python 버전 설치 및 지정

- pyenv 설치는 공식 문서 참고
- 프로젝트 루트에서 다음 실행:
    - pyenv install 3.12.11
    - pyenv local 3.12.11
    - python -m venv .venv
    - source .venv/bin/activate  (Windows: .venv\Scripts\activate)

2) 패키지 설치

- 최신 pip로 업데이트:
    - python -m pip install -U pip
- 프로젝트 설치(런타임 의존성 포함):
    - pip install -e .
- 개발 도구 포함 설치(선택):
    - pip install -e ".[dev]"

3) 애플리케이션 실행

- Streamlit 웹 앱:
    - streamlit run src/tax_bot/app.py
- 모듈로 실행(필요 시):
    - python -m tax_bot.main

4) 접속

- 기본적으로 Streamlit이 http://localhost:8501 에서 서비스됩니다.

## 환경 변수/설정

- 기본 실행에는 추가 설정이 필요 없도록 설계되었습니다.
- 외부 API 키나 프록시 등 환경 의존 설정이 필요한 경우, 다음과 같이 .env 또는 셸 환경변수로 주입해 사용하세요.
    - export YOUR_KEY=...
- 실제 사용 변수는 구현에 따라 다를 수 있으니 관련 코드와 문서를 참고하세요.

## 개발 가이드

- 코드 스타일/정적 분석: ruff
    - ruff 실행:
        - ruff check .
    - 자동 수정:
        - ruff check . --fix
- 커밋 훅: pre-commit
    - 초기화:
        - pre-commit install
    - 수동 실행:
        - pre-commit run --all-files

권장 워크플로

- 기능 개발 전 브랜치 생성
- ruff/테스트 통과 확인
- pre-commit 훅 통과 후 PR 생성
