#!/usr/bin/env bash

docker-compose \
    -f services.docker-compose.yml \
    run -v "$(pwd)":/app \
    mlsploit-api-service $@
