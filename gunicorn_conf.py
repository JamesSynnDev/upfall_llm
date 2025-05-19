# Gunicorn 설정
bind = "0.0.0.0:8000"
workers = 1                  # CPU 코어 수 기반으로 조정
worker_class = "uvicorn.workers.UvicornWorker"
timeout = 120               # 타임아웃(초)
accesslog = "/app/logs/access.log"
errorlog  = "/app/logs/error.log"
loglevel  = "info"