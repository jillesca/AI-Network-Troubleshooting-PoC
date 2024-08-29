"""
Wrapper functions to work with langchain tools and openAI
"""

from langchain.agents import tool

from llm_agent.utils.text_utils import output_to_json
from llm_agent.pyats_connector.api.interface_config import (
    interface_running_config,
    interfaces_description,
)


@tool
def get_interface_running_config(
    device_name: str, interface_name: str
) -> dict:
    """
    Get the running config of a single interface on a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interface_name (str): The name of the interface.

    Returns:
      dict: The running configuration of the specified interface.
    """

    return output_to_json(
        interface_running_config(device_name, interface_name)
    )


@tool
def get_interfaces_description(device_name: str) -> dict:
    """
    Get the description of the interfaces per device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interface_name (str): The name of the interface.

    Returns:
      dict: A dictionary containing the status of the interface.
    """
    return output_to_json(interfaces_description(device_name))
