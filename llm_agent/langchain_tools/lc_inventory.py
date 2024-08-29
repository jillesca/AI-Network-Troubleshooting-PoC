"""
Wrapper functions to work with langchain tools and openAI
"""

from langchain.agents import tool

from llm_agent.utils.text_utils import output_to_json
from llm_agent.pyats_connector.inventory import (
    get_devices_from_inventory,
)


@tool
def get_devices_list_available() -> list:
    """
    Retrieves the list of valid available devices.

    Returns:
      A list representation of the available devices.
    """
    return output_to_json(get_devices_from_inventory())
