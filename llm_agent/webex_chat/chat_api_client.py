import requests

from llm_agent.config.load_global_settings import (
    HOST_URL,
    LLM_HTTP_PORT,
)

import requests

NUMBER_OF_TRIES_TO_CONNECT = 10


def send_message_to_chat_api(message: str) -> str:
    """
    Sends a message to the chat API and returns the response.

    Args:
        message (str): The message to send.

    Returns:
        str: The response from the API, or an error message if the request failed.
    """
    url = f"http://{HOST_URL}:{LLM_HTTP_PORT}/chat"
    data = {"message": message}
    for _ in range(NUMBER_OF_TRIES_TO_CONNECT):  # try twice
        try:
            response = requests.post(url, json=data, timeout=120)
            if response.status_code == 200:
                return response.json()
            else:
                print(
                    f"Error: http status code: {response.status_code}, http response: {response.text}"
                )
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
        return "Ouch, Error connecting webex to LLM. try again."
