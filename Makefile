include .env.local
include .env
export

.PHONY: all build run logs cli

all:	build-all

build-all:
		-docker-compose down
		docker-compose up --build --detach

build-%:
		-docker-compose rm -f $*
		docker-compose up --build --detach $*

logs-%:
		docker-compose logs -f $*

cli-%:
		docker-compose exec $* bash