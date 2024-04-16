#!/bin/bash
set -eu # Abort the script if a command returns with a non-zero exit code or if
        # a variable name is dereferenced when the variable hasn't been set

source .env
source .env.local

docker rm -f grafana

docker build --file grafana/dockerfile \
        --build-arg LLM_HTTP_PORT=$LLM_HTTP_PORT \
        --build-arg GRAFANA_TOKEN=$GRAFANA_TOKEN \
        --build-arg WEBEX_ROOM_ID=$WEBEX_ROOM_ID \
        --build-arg GRAFANA_WEB_HOOK=$GRAFANA_WEB_HOOK \
        --build-arg WEBEX_TEAMS_ACCESS_TOKEN=$WEBEX_TEAMS_ACCESS_TOKEN \
        --tag grafana:$GRAFANA_TAG .

docker run -itd -p 3000:3000 --name grafana --add-host host.docker.internal:host-gateway grafana:$GRAFANA_TAG 

echo "################################"
echo "To access the container use:"
echo "docker exec -it grafana bash"
echo "################################"