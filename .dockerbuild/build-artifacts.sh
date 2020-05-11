#!/usr/bin/env bash

cd "$(cd "$(dirname "${BASH_SOURCE[0]}")" > /dev/null && pwd -P)"

declare -r IMAGE_NAME="$(basename "$(cd .. && pwd -P)")-build"

docker build -t ${IMAGE_NAME} -f ./Dockerfile.build ..
docker run --rm -v "${PWD}":/host ${IMAGE_NAME}
docker rmi ${IMAGE_NAME}
