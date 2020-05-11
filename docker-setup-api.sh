#!/usr/bin/env bash

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd -P)"

if [[ ! -f .env ]]; then
    cp .env.example .env
fi

set -a && . .env && set +a

function log() {
    echo -e "\033[34m\033[1m[docker-setup-api]\033[0m $@"
}

function usage() {
    echo "usage: bash docker-setup-api.sh [-aph]"
    echo
    echo "options:"
    echo "    a    Automatically generate and set an API secret key if it doesn't exist."
    echo "         This will also create a password-less admin user."
    echo "         To set the admin password, run './docker-manage-api.sh changepassword admin'."
    echo "    p    Setup in production mode (disables Django DEBUG flag)."
    echo "    t    Create a test user (username: testuser, password: testpassword)"
    echo "    h    Show this message."
    echo
    echo "This is a helper script to set up the MLsploit REST API Docker service."
}

function update_env() {
    KEY="$1"; VAL="$2"; LINE_NUM=$(grep -nm 1 "^${KEY}=" .env | cut -f1 -d:)
    (sed "${LINE_NUM}s/.*/${KEY}=${VAL}/" .env > .env.tmp) && mv .env.tmp .env
}

function createadminuser() {
    NOINPUT=$1
    if [[ $NOINPUT == "true" ]]; then
        ./docker-manage-api.sh createsuperuser \
            --username admin \
            --email admin@example.com \
            --no-input
    else
        ./docker-manage-api.sh createsuperuser --username admin
    fi
}

AUTO_MODE="false"
SET_PROD="false"
CREATE_TESTUSER="false"
while getopts ":apth" OPTKEY; do
    case $OPTKEY in
        a )
            AUTO_MODE="true"
            ;;
        p )
            SET_PROD="true"
            ;;
        t )
            CREATE_TESTUSER="true"
            ;;
        h )
            usage
            exit 0
            ;;
        \? )
            echo "invalid option: -$OPTARG" 1>&2
            echo
            usage
            exit 1
            ;;
    esac
done

if [[ -z "${MLSPLOIT_API_SECRET_KEY}" ]]; then
    log "MLSPLOIT_API_SECRET_KEY is not set!"
    if [[ $AUTO_MODE == "true" ]]; then
        ./env-set-secret.sh -a
        log "MLSPLOIT_API_SECRET_KEY set automatically"
    else
        ./env-set-secret.sh
    fi
fi

log "Building Docker images..."
docker-compose build || exit 1

log "Setting up Django models..."
./docker-manage-api.sh makemigrations || exit 1
./docker-manage-api.sh migrate || exit 1

log "Creating user 'admin'..."
./docker-manage-api.sh checkuserexists admin \
    && log "User 'admin' already exists!" \
    || createadminuser $AUTO_MODE

log "Generating token for user 'admin'..."
./docker-manage-api.sh drf_create_token admin

if [[ $SET_PROD == "true" ]]; then
    update_env MLSPLOIT_API_DEBUG_MODE "false"
    log "Disabled debug mode"
fi

if [[ $CREATE_TESTUSER == "true" ]]; then
    log "Creating test user"
    ./docker-manage-api.sh createuser
fi
