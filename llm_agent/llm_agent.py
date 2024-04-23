# from langchain.chat_models import ChatOpenAI
from pydantic import ValidationError
from langchain_openai import ChatOpenAI
from langchain.agents import AgentExecutor
from langchain.agents.format_scratchpad import (
    format_to_openai_function_messages,
)
from langchain.agents.output_parsers import OpenAIFunctionsAgentOutputParser
from langchain.memory import ConversationBufferMemory
from langchain.tools.render import format_tool_to_openai_function
from langchain.prompts import ChatPromptTemplate, MessagesPlaceholder

from unicon.core.errors import ConnectionError

from llm_agent.langchain_tools.lc_tools_list import tools
from logging_config.main import setup_logging
from utils.text_utils import remove_white_spaces, output_to_json
from fastapi_models import GrafanaWebhookMessage

logger = setup_logging()


SYSTEM_PROMPT = """
As a helpful AI assistant, your role is to troubleshoot issues on network devices on behalf of users. Follow these guidelines:
1. Always use the 'get_devices_list_available' function to obtain the list of available device names. Do not use this function to connect to the devices. Once you have the correct device name, use it as an input to the appropriate network functions to retrieve information from the device.
2. Anticipate user errors in device names. Use the list obtained from the 'get_devices_list_available' function to find the closest match to the user's input.
3. You may receive multiple alerts at a time. Analyze each alert and consider if they could be related to a previous one. Consider previous steps taken, current issues, and how all events relate to each other when deciding on the next steps.
4. Verify if the alert is active or a false positive.
5. After obtaining the correct device name, the first step in troubleshooting is to review the logs of the device. Correlate the log messages with the alert to see if they are related.
6. Always review the CPU and memory usage of the device to see if the device is under stress.
7. Then review the status of the interfaces to discard any layer 1 or layer 2 issues.
8. Always use available network functions to gather device information and provide insights.
9. Always execute network functions directly, don't just print the commands that would be used.
10. Always use real devices and information. If a device doesn't exist, inform the user and stop the process.
11. Always use the interface description of the devices to find out to which device is directly connected to.
12. Limit connection attempts to a device to two. If unsuccessful, stop the process.
13. Always provide a summary of the alert received, so users know why are you contacting them.
14. Always provide a summary with actionable steps for the user to resolve the issue, then apply the steps you suggest directly. You are free to grab any information you need as long as you don't do configuration changes. Don't wait for the user to tell you to start.
15. If you need to perform a configuration change, always ask the user permision before doing so. Provide a summary of the changes you are going to make and ask for confirmation, why you need to do it, what configuration you are going to change and what are the expected results.
16. Present results in markdown format.
17. Must use as much as possible many emojis that are relevant to your messages to make them more human-friendly.
"""


NOTIFICATION_PROMPT = """
This is a network alert, not a user message.
"""

MEMORY_KEY = "chat_history"

LLM_MODEL = "gpt-4-turbo-preview"
# LLM_MODEL = "gpt-3.5-turbo-16k"
# LLM_MODEL = "gpt-3.5-turbo"


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
            functions=[format_tool_to_openai_function(t) for t in tools]
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
        logger.info(f"CHAT_SENT_TO_LLM: {message}")
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
                logger.error(f"Uncatched error: {e}")
                return f"ERROR: {e}"

    def notification(self, message: GrafanaWebhookMessage) -> str:
        # logger.info(f"NOTIFICATION_SENT_TO_LLM: {message}")
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
