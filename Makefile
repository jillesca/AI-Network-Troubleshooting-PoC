.PHONY: all build run logs cli

all: build-grafana build-influxdb build-telegraf

build-%:
    -docker-compose rm -f $*
    docker-compose build $*
    docker-compose up -d $*

run-%:
    docker-compose up -d $*

logs-%:
    docker-compose logs -f $*

cli-%:
    docker-compose exec $* bash