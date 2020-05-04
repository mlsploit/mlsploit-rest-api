#!/usr/bin/env bash

set -a && . .env && set +a

if [[ -z "${MLSPLOIT_API_SECRET_KEY}" ]]
then
    echo "[ERROR] MLSPLOIT_API_SECRET_KEY is not set"
    exit 1
fi

if [[ $# -eq 0 ]]
  then
    python manage.py runserver 0.0.0.0:8000
  else
    python manage.py $@
fi
