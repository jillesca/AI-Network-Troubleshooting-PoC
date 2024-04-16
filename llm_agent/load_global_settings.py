"""
This module is responsible for loading global settings for the application.

It imports necessary modules and functions, 
defines a function for retrieving environment variables, 
and sets several global variables.

Variables:
    GLOBAL_SETTINGS_FILE (str): The path to the global settings JSON file.
    global_config (dict): The loaded global settings from the JSON file.
    TESTBED_FILE (str): The path to the testbed file, retrieved from the global settings.
    HOST_URL (str): The host URL for the application, retrieved from the global settings.
    PORT (int): The port for the application, retrieved from the global settings.
    WEBEX_TEAMS_ACCESS_TOKEN (str): The access token for Webex Teams, retrieved from an environment variable.
    WEBEX_APPROVED_USERS_MAIL (str): The approved users mail for Webex, retrieved from an environment variable.
    OPENAI_API_KEY (str): The API key for OpenAI, retrieved from an environment variable.
"""
import os
from utils.text_utils import load_json_file


def get_environment_variable(envvar: str) -> str:
    """
    Retrieve the value of an environment variable.
    If the environment variable is not set, raise an exception.
    """
    value = os.getenv(envvar)
    if value is None:
        raise EnvironmentError(
            f"The required environment variable {envvar} is not set."
        )
    return value


GLOBAL_SETTINGS_FILE = "llm_agent/global_settings.json"
global_config = load_json_file(json_file=GLOBAL_SETTINGS_FILE)


LLM_HTTP_PORT = global_config.get("llm_http_port", 5001)
HOST_URL = global_config.get("host_url", "0.0.0.0")
TESTBED_FILE = global_config.get("testbed_file", "pyats_testbed.yaml")

WEBEX_TEAMS_ACCESS_TOKEN = get_environment_variable("WEBEX_TEAMS_ACCESS_TOKEN")

WEBEX_APPROVED_USERS_MAIL = get_environment_variable(
    "WEBEX_APPROVED_USERS_MAIL"
)

OPENAI_API_KEY = get_environment_variable("OPENAI_API_KEY")
