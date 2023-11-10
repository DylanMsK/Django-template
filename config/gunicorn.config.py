bind = "0.0.0.0:8000"  # Gunicorn이 바인딩할 주소 및 포트
workers = 1  # Gunicorn 워커 프로세스 수
worker_class = "uvicorn.workers.UvicornWorker"  # Uvicorn 워커 클래스
loglevel = "info"  # 로깅 레벨
