FROM python:3.11.6-slim-bullseye AS builder
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

EXPOSE 8000
WORKDIR /app 
COPY requirements.txt /app
RUN pip3 install -r requirements.txt --no-cache-dir
COPY . /app 
ENTRYPOINT ["python3"] 
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

FROM builder as prod
CMD ["manage.py", "runserver", "0.0.0.0:8000"]

FROM builder as dev
CMD ["manage.py", "runserver", "0.0.0.0:8000"]