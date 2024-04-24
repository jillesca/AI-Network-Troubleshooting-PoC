"""
This module contains the function to send a message to the chat API.
"""

import logging
import requests

from llm_agent.config.global_settings import (
    HOST_URL,
    LLM_HTTP_PORT,
)
from llm_agent.config.global_settings import LOGGER_NAME


FASTAPI_REST_PATH = "chat"
MAX_NUMBER_OF_TRIES_TO_CONNECT = 10

logger = logging.getLogger(LOGGER_NAME)


def send_message_to_chat_api(message: str) -> str:
    """
    Sends a message to the chat API and returns the response.

    Args:
        message (str): The message to send.

    Returns:
        str: The response from the API, or an error message if the request failed.
    """
    url = f"http://{HOST_URL}:{LLM_HTTP_PORT}/{FASTAPI_REST_PATH}"
    data = {"message": message}
    for _ in range(MAX_NUMBER_OF_TRIES_TO_CONNECT):
        try:
            response = requests.post(url, json=data, timeout=120)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    "Error from fastAPI for send_message_to_chat_api: http status code: %s, http response: %s, url: %s",
                    response.status_code,
                    response.text,
                    url,
                )
        except requests.exceptions.RequestException as e:
            logger.error(
                "Error from fastAPI for send_message_to_chat_api: %s", e
            )
        return f"Ouch, I got a {response.status_code} from fastAPI, can't connect to the LLM."
