#!/usr/bin/env bash

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd -P)"

if [[ ! -f .env ]]; then
    cp .env.example .env
fi

function usage() {
    echo "usage: bash env-set-secret.sh [-ah]"
    echo
    echo "options:"
    echo "    a    Automatically generate and set a secret key."
    echo "    h    Show this message."
    echo
    echo "This is a helper script to set the MLSPLOIT_API_SECRET_KEY variable in the .env file."
}

function update_env() {
    KEY="$1"; VAL="$2"; LINE_NUM=$(grep -nm 1 "^${KEY}=" .env | cut -f1 -d:)
    (sed "${LINE_NUM}s/.*/${KEY}=${VAL}/" .env > .env.tmp) && mv .env.tmp .env
}

AUTO_MODE="false"
while getopts ":ah" OPTKEY; do
    case $OPTKEY in
        a )
            AUTO_MODE="true"
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

if [[ $AUTO_MODE == "false" ]]; then
    read -sp \
        "Enter a new secret key (or press ENTER to accept a randomly generated key): " ENTERED_SECRET_KEY \
            && echo
fi

SUGGESTED_SECRET_KEY=$(LC_CTYPE=C < /dev/urandom tr -dc _A-Z-a-z-0-9 | head -c50; echo;)
ENTERED_SECRET_KEY=${ENTERED_SECRET_KEY:-$SUGGESTED_SECRET_KEY}

update_env MLSPLOIT_API_SECRET_KEY "$ENTERED_SECRET_KEY"
