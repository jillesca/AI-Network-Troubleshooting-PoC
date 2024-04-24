"""
This module defines the FastAPI application and the endpoints for the chat API.

It imports necessary modules and functions, sets up logging, 
loads global settings, and initializes the chat agent and the Webex bot manager.

It defines a Pydantic model for the message data and two POST endpoints:
one for sending messages to the chat agent and another for processing alerts.
"""

import threading
import uvicorn
from fastapi import FastAPI

from llm_agent.logging_config.logging_setup import logger
from llm_agent.config.global_settings import (
    HOST_URL,
    LLM_HTTP_PORT,
)
from llm_agent.llm.agent import LLMChatAgent
from llm_agent.webex_chat.bot import WebexBotManager
from llm_agent.fastAPI.models import Message, GrafanaWebhookMessage


app = FastAPI()
chat_agent = LLMChatAgent()
webex_bot_manager = WebexBotManager()


@app.post("/chat")
def chat_to_llm(message: Message) -> str:
    """
    Process the given message and return a response from the chat agent.

    Args:
      message (Message): The message to be processed.

    Returns:
      str: The response from the chat agent.
    """
    logger.info("WEBEX_MESSAGE_SENT_TO_LLM: %s", message.message)
    return chat_agent.chat(message.message)


@app.post("/alert")
async def alert(message: GrafanaWebhookMessage) -> dict:
    """
    This function receives a webhook alert and starts processing it.
    Grafana sends a webhook empty as a keepalive.
    'Firing' is used to identify a real alert.
    """
    logger.info("WEBHOOK_MESSAGE_RECEIVED: %s", message)
    if message.status.lower() == "firing":
        process_alert(message)
    return {"status": "success"}


def process_alert(message: Message) -> None:
    """
    This function sends the alert to the LLM
    and sends the result of the initial analysis to the Webex room.
    """
    notification = chat_agent.notification(message)
    notify(notification)


def notify(notification: str) -> None:
    """
    Sends a notification message.
    """
    logger.info("SENDING_NOTIFICATON_TO_WEBEX: %s", notification)
    webex_bot_manager.send_notification(notification)


if __name__ == "__main__":
    threading.Thread(
        target=uvicorn.run,
        args=("app:app",),
        kwargs={"host": HOST_URL, "port": LLM_HTTP_PORT},
    ).start()
    webex_bot_manager.run()
