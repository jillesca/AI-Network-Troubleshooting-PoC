#!/bin/bash
set -eu # Abort the script if a command returns with a non-zero exit code or if
        # a variable name is dereferenced when the variable hasn't been set

source .env.local

docker rm -f telegraf 

docker build \
        --target telegraf \
        --build-arg TELEGRAF_ORG=$TELEGRAF_ORG \
        --build-arg TELEGRAF_TOKEN=$TELEGRAF_TOKEN \
        --build-arg TELEGRAF_BUCKET=$TELEGRAF_BUCKET \
        --file telegraf/dockerfile \
        --tag telegraf:$TELEGRAF_TAG .

docker run -itd -p 57500:57500 --name telegraf \
        --add-host host.docker.internal:host-gateway telegraf:$TELEGRAF_TAG
        # -v ${PWD}/netconf_client:/opt/netconf_client/ \

echo "################################"
echo "To access the container use:"
echo "docker exec -it telegraf bash"
echo "################################"