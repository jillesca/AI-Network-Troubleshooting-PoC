include .env.local
include .env
export

build-tig:
		$(MAKE) clean-tig
		docker compose up --build --detach telegraf influxdb grafana

run-tig:
		$(MAKE) clean-tig
		docker compose up --detach telegraf influxdb grafana

build-llm:
		$(MAKE) clean-llm
		docker compose up --build --detach llm_agent

run-llm:
		$(MAKE) clean-llm
		docker compose up --detach llm_agent
		$(MAKE) follow

follow:
		docker compose logs --follow llm_agent

cli:
		docker compose exec llm_agent bash

clean-tig:
		-docker compose down telegraf influxdb grafana
		-docker compose rm -f telegraf influxdb grafana

clean-llm:
		-docker compose down llm_agent
		-docker compose rm -f llm_agent
