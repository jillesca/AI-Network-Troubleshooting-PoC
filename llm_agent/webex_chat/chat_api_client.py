"""
This module contains the function to send a message to the chat API.
"""

import time
import logging
import requests

from llm_agent.config.global_settings import (
    HOST_URL,
    LLM_HTTP_PORT,
)
from llm_agent.config.global_settings import LOGGER_NAME


FASTAPI_REST_PATH = "chat"
MAX_NUMBER_OF_TRIES_TO_CONNECT = 11

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
    for retries in range(MAX_NUMBER_OF_TRIES_TO_CONNECT):
        logger.debug("Attempting to connect: %s", retries)
        try:
            response = requests.post(url, json=data, timeout=120)
            if response.status_code == 200:
                return response.json()
            else:
                logger.error(
                    "send_message_to_chat_api: Error connecting to fastAPI: http status code: %s, http response: %s, url: %s",
                    response.status_code,
                    response.text,
                    url,
                )
        except requests.exceptions.RequestException as e:
            logger.error("send_message_to_chat_api: Error from fastAPI: %s", e)
        time.sleep(0.5)

    return (
        "Ouch, I got an error from fastAPI server, can't connect to the LLM."
    )
