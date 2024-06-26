FROM python:3.12.2 as base

COPY llm_agent.requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip && \
    pip install -r /tmp/requirements.txt

FROM base AS app

EXPOSE 5001

ARG OPENAI_API_KEY \
    GRAFANA_WEB_HOOK \
    LANGCHAIN_API_KEY \
    LANGCHAIN_PROJECT \
    WEBEX_ROOM_ID \
    WEBEX_TEAMS_ACCESS_TOKEN \
    WEBEX_APPROVED_USERS_MAIL

ENV OPENAI_API_KEY=${OPENAI_API_KEY} \
    LANGCHAIN_API_KEY=${LANGCHAIN_API_KEY} \
    LANGCHAIN_PROJECT=${LANGCHAIN_PROJECT} \
    GRAFANA_WEB_HOOK=${GRAFANA_WEB_HOOK} \
    WEBEX_ROOM_ID=${WEBEX_ROOM_ID} \
    PYTHONPATH=:/llm_agent \
    WEBEX_TEAMS_ACCESS_TOKEN=${WEBEX_TEAMS_ACCESS_TOKEN} \
    WEBEX_APPROVED_USERS_MAIL=${WEBEX_APPROVED_USERS_MAIL}

COPY llm_agent /llm_agent

ENTRYPOINT [ "python", "-u", "/llm_agent/app.py" ]
# ENTRYPOINT ["sh", "-c", "while :; do sleep 1; done"]