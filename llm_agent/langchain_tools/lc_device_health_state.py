"""
Wrapper functions to work with langchain tools and openAI
"""

from langchain.agents import tool

from llm_agent.utils.text_utils import output_to_json
from llm_agent.pyats_connector.api.device_health_state import (
    health_cpu,
    health_memory,
    health_logging,
)


@tool
def get_health_memory(device_name: str) -> dict:
    """
    Retrieves the memory health information for a given device.

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      dict: A dictionary containing the memory health information. Empty is good.
    """
    return output_to_json(health_memory(device_name))


@tool
def get_health_cpu(device_name: str) -> dict:
    """
    Retrieves the CPU health information for a given device.

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      dict: A dictionary containing the CPU health information. Empty is good.
    """
    return output_to_json(health_cpu(device_name))


@tool
def get_health_logging(
    device_name: str,
    keywords: list[str] = None,
) -> dict:
    """
    Retrieves health logging information from a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      keywords (list[str], optional): List of keywords to filter the health logging information.
        Defaults to traceback, error, down and adjchange.

    Returns:
      dict: The health logging information in JSON format.
    """
    if keywords is None:
        keywords = [
            "traceback",
            "Traceback",
            "TRACEBACK",
            "rror",
            "own",
            "ADJCHANGE",
        ]
    return output_to_json(health_logging(device_name, keywords))
