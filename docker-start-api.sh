#!/usr/bin/env bash

set -a && . .env && set +a

docker-compose -f services.docker-compose.yml up
