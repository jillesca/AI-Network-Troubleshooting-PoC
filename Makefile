include .env.local
include .env
export

.PHONY: all build run logs cli

all:	tig-build llm-build

tig-build:
		$(MAKE) clean-tig
		docker-compose up --build --detach telegraf influxdb grafana

llm-build:
		$(MAKE) clean-llm
		docker-compose up --build --detach llm_agent

follow:
		docker-compose logs --follow llm_agent

cli:
		docker-compose exec llm_agent bash

clean-tig:
		-docker-compose down telegraf influxdb grafana

clean-llm:
		-docker-compose down llm_agent
