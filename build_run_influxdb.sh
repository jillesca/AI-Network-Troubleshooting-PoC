#!/bin/bash
set -eu # Abort the script if a command returns with a non-zero exit code or if
        # a variable name is dereferenced when the variable hasn't been set

source .env.local

docker rm -f influxdb

docker build \
        --file influxdb/dockerfile \
        --build-arg DOCKER_INFLUXDB_INIT_MODE=$INFLUXDB_MODE \
        --build-arg DOCKER_INFLUXDB_INIT_USERNAME=$INFLUXDB_USERNAME \
        --build-arg DOCKER_INFLUXDB_INIT_PASSWORD=$INFLUXDB_PASSWORD \
        --build-arg DOCKER_INFLUXDB_INIT_ORG=$INFLUXDB_ORG \
        --build-arg DOCKER_INFLUXDB_INIT_BUCKET=$INFLUXDB_BUCKET \
        --build-arg DOCKER_INFLUXDB_INIT_ADMIN_TOKEN=$INFLUXDB_ADMIN_TOKEN \
        --tag influxdb:$INFLUXDB_TAG .

docker run -itd -p 8086:8086 --volume influxdb:/var/lib/influxdb2 --name influxdb --add-host host.docker.internal:host-gateway influxdb:$INFLUXDB_TAG 

echo "################################"
echo "To access the container use:"
echo "docker exec -it influxdb bash"
echo "################################"