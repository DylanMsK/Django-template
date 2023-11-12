FROM python:3.9.18-slim-bullseye as builder
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*


RUN pip install poetry==1.7.0

# Configuring poetry
RUN poetry config virtualenvs.create false

# Copying requirements of a project
COPY pyproject.toml poetry.lock /app/src/
WORKDIR /app/src

# Installing requirements
RUN poetry install --only main

# Removing gcc
RUN apt-get purge -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copying actuall application
COPY . /app/src/
RUN poetry install --only main

CMD ["gunicorn", "-c", "config/gunicorn.config.py", "config.asgi:application" ]

FROM builder as dev
RUN poetry install
