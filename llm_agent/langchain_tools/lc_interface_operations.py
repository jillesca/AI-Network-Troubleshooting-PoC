"""
Wrapper functions to work with langchain tools and openAI
"""

from langchain.agents import tool

from llm_agent.utils.text_utils import output_to_json
from llm_agent.pyats_connector.api.interface_operations import (
    shut_interface,
    unshut_interface,
)


@tool
def action_shut_interface(device_name: str, interface_name: str) -> None:
    """
    Shut down an interface on a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interface_name (str): The name of the interface to shut down.

    Returns:
      None
    """
    return output_to_json(shut_interface(device_name, interface_name))


@tool
def action_unshut_interface(device_name: str, interface_name: str) -> None:
    """
    Shut down an interface on a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interface_name (str): The name of the interface to be shut down.

    Returns:
      None
    """
    return output_to_json(unshut_interface(device_name, interface_name))
