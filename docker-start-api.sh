#!/usr/bin/env bash

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd -P)"

./docker-manage-api.sh makemigrations > /dev/null
./docker-manage-api.sh migrate > /dev/null

docker-compose up
