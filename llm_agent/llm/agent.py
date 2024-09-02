""" 
The LLMChatAgent class is responsible for handling the chat interactions with the LLM.
"""

import logging
from pydantic import ValidationError
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import (
    format_to_openai_function_messages,
)
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.utils.function_calling import convert_to_openai_function

from unicon.core.errors import ConnectionError

from llm_agent.llm.prompts import SYSTEM_PROMPT
from llm_agent.log_config.logger_setup import logger
from llm_agent.langchain_tools.lc_tools_list import tools
from llm_agent.utils.text_utils import remove_white_spaces, output_to_json
from llm_agent.fastAPI.models import GrafanaWebhookMessage

httpx_logger = logging.getLogger("httpx")
httpx_logger.setLevel(logging.ERROR)

NOTIFICATION_PROMPT = """
This is a network alert, not a user message.
"""

MEMORY_KEY = "chat_history"

LLM_MODEL = "chatgpt-4o-latest"


class LLMChatAgent:
    def __init__(self) -> None:
        self._create_agent()

    def _create_agent(self) -> None:
        prompt = ChatPromptTemplate.from_messages(
            [
                (
                    "system",
                    remove_white_spaces(string=SYSTEM_PROMPT),
                ),
                MessagesPlaceholder(variable_name=MEMORY_KEY),
                ("user", "{input}"),
                MessagesPlaceholder(variable_name="agent_scratchpad"),
            ]
        )

        llm = ChatOpenAI(model=LLM_MODEL, temperature=0)
        llm_with_tools = llm.bind(
            functions=[convert_to_openai_function(t) for t in tools]
        )

        agent = (
            {
                "input": lambda x: x["input"],
                "agent_scratchpad": lambda x: format_to_openai_function_messages(
                    x["intermediate_steps"]
                ),
                "chat_history": lambda x: x["chat_history"],
            }
            | prompt
            | llm_with_tools
            | OpenAIFunctionsAgentOutputParser()
        )

        memory = ConversationBufferMemory(
            memory_key="chat_history", return_messages=True
        )
        self.agent_executor = AgentExecutor(
            agent=agent, tools=tools, verbose=True, memory=memory
        )

    def _agent_executor(self, message: str) -> str:
        return self.agent_executor.invoke({"input": message})["output"]

    def chat(self, message: str, attempts: int = 0) -> str:
        """
        TODO: There a potential loop here. If agent is not able to connect to the device,
        the agent will try to connect again to the device. This can go on forever.
        The agent stoppped at 3 attempts to connect to the device.
        """
        logger.debug("CHAT_SENT_TO_LLM: %s", message)
        try:
            return self._agent_executor(message)
        except (ValidationError, ConnectionError, KeyError) as e:
            if attempts < 2:
                if isinstance(e, ValidationError):
                    msg = f"ERROR: You missed a parameter invoking the function, See for the information missing: {e}"
                elif isinstance(e, ConnectionError):
                    msg = f"ERROR: Unable to connect. {e}"
                else:  # KeyError
                    msg = f"ERROR: You provided an empty value or a device that doesn't exists. {e}"
                logger.error(msg)
                return self.chat(msg, attempts + 1)
            else:
                logger.error("Uncatched error: %s", e)
                return f"ERROR: {e}"

    def notification(self, message: GrafanaWebhookMessage) -> str:
        """
        Sends a notification to the LLM agent.

        Args:
          message (GrafanaWebhookMessage): The message containing the notification details.

        Returns:
          str: The response from the LLM agent.

        """
        notification = {
            "system_instructions": remove_white_spaces(
                string=NOTIFICATION_PROMPT
            ),
            "network_alert": message.model_dump(),
        }

        return self.chat(output_to_json(notification), attempts=0)


if __name__ == "__main__":
    agent = LLMChatAgent()
    chat = agent.chat("can you check the interfaces on the cat8000v-0 device?")
    print(chat)
    print("#" * 80, "\n")
    chat = agent.chat("can you check if the isis is configured?")
    print(chat)
    print("#" * 80, "\n")
    chat = agent.chat("what vrfs I have there?")
    print(chat)
    print("#" * 80, "\n")
    chat = agent.chat(
        "please provide a summary of all activities I asked you to check in our conversation"
    )
    print(chat)
    print("#" * 80, "\n")
