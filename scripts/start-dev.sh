#!/usr/bin/env bash

if command -v docker-compose > /dev/null 2>&1 ; then
    docker-compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
else
    # docker-compose 명령을 사용할 수 없는 경우, docker compose 명령을 시도합니다
    if command -v docker compose > /dev/null 2>&1 ; then
        docker compose -f deploy/docker-compose.yml -f deploy/docker-compose.dev.yml --project-directory . up --build
    else
        echo "오류: 이 시스템에서는 'docker-compose'와 'docker compose' 명령어 중 어느 하나도 사용할 수 없습니다."
        exit 1
    fi
fi