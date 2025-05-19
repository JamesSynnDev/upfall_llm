## Makefile for Python Project Automation
# 기본 가상환경, 패키지 설치, 의존성 추출 등을 자동화합니다.

# 기본 Python 인터프리터 (poetry 사용 시 'poetry run python')
PYTHON ?= python3
# Poetry 사용 여부 (yes/no)
USE_POETRY ?= no

# 패키지 설치
install:
ifeq ($(USE_POETRY),yes)
	poetry install
else
	$(PYTHON) -m pip install -r requirements.txt
endif

# 현재 환경의 패키지 리스트 생성 (pip freeze)
freeze:
	$(PYTHON) -m pip freeze > requirements.txt

# Poetry 의존성 내보내기 (requirements.txt)
export-deps:
	poetry export -f requirements.txt --output requirements.txt --without-hashes

# 개발 의존성 포함 내보내기
export-dev:
	poetry export -f requirements.txt --output requirements.txt --without-hashes --dev

# FastAPI 서버 실행 (개발용)
serve:
ifeq ($(USE_POETRY),yes)
	poetry run uvicorn main:app --reload
else
	$(PYTHON) -m uvicorn main:app --reload
endif

# 테스트 실행 예시 (pytest)
test:
ifeq ($(USE_POETRY),yes)
	poetry run pytest
else
	$(PYTHON) -m pytest
endif

# 전체 초기화 (의존성 설치 + export)
setup: install export-deps

.PHONY: install freeze export-deps export-dev serve test setup
