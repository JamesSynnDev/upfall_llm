# ── 1) 빌드 스테이지: .venv 생성 및 의존성 설치 ──────────
FROM python:3.11-slim AS builder
WORKDIR /app

# 시스템 패키지 필요 시 여기에 추가 (예: git, build-essential 등)
RUN apt-get update && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# 요구사항만 먼저 복사
COPY requirements.txt .

# .venv 생성 및 패키지 설치
RUN python -m venv .venv \
 && .venv/bin/pip install --upgrade pip \
 && .venv/bin/pip install --no-cache-dir -r requirements.txt

# ── 2) 런타임 스테이지: .venv 및 소스 코드 복사 ──────────
FROM python:3.11-slim
WORKDIR /app

# .venv, src/, static/, templates/, logging.ini
COPY --from=builder /app/.venv .venv
COPY src/ src/
COPY static/ static/
COPY templates/ templates/
COPY logging.ini logging.ini
COPY .env .env
COPY gunicorn_conf.py .

# ① 로그 디렉토리 생성
RUN mkdir -p /app/logs \
 && chown -R 1000:1000 /app/logs

# ② (선택) 컨테이너 외부에 로그 마운트하기
VOLUME ["/app/logs"]

# PATH에 .venv/bin 추가
ENV PATH="/app/.venv/bin:$PATH"

# Gunicorn 실행
CMD ["gunicorn", "-c", "gunicorn_conf.py", "src.main:app", "--log-config", "logging.ini", "--access-logfile", "-", "--error-logfile", "-"]

