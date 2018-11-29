#!/bin/bash

echo 'Sets env vars to allow running python scripts inside galaxy container'
echo 'Example commands:'
echo '$DOCKER_COMPOSE exec galaxy $VENV_BIN/python ./manage.py makemigrations main --empty'
echo '$DOCKER_COMPOSE exec galaxy $VENV_BIN/python ./manage.py recompute_quality --count --scored-all'

export VENV_BIN=/var/lib/galaxy/venv/bin
export DOCKER_COMPOSE='docker-compose -p galaxy -f ./scripts/docker/dev/compose.yml'
