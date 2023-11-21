FROM python:3.9.18-slim-bullseye as production
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

ARG DJANGO_ENV
ENV DJANGO_ENV=${DJANGO_ENV}

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
RUN echo 'DJANGO_ENV: ${DJANGO_ENV}'
RUN ls -al envs
RUN cat envs/.env.${DJANGO_ENV}


RUN python manage.py migrate

CMD ["gunicorn", "-c", "config/gunicorn.config.py", "config.asgi:application" ]


FROM production as development
RUN poetry install
