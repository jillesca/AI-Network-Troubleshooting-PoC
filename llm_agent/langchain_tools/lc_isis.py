"""
Wrapper functions to work with langchain tools and openAI
"""

from langchain.agents import tool

from llm_agent.utils.text_utils import output_to_json
from llm_agent.pyats.api.isis import (
    isis_neighbors,
    isis_interface_events,
    isis_interfaces,
)


@tool
def verify_active_isis_neighbors(device_name: str) -> dict:
    """
    Retrieves the ISIS neighbors for a given device. Neighbors down are not included.

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      dict: A dictionary containing the ISIS neighbors information.
    """
    return output_to_json(isis_neighbors(device_name))


@tool
def get_isis_interface_events(device_name: str) -> dict:
    """
    Retrieves ISIS interface events for a given device.

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      dict: A dictionary containing the ISIS interface events.
    """
    return output_to_json(isis_interface_events(device_name))


@tool
def get_isis_interface_information(
    device_name: str, vrf_name: str = "default"
) -> list:
    """
    Retrieves the ISIS interfaces for a given device and VRF.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      vrf_name (str, optional): The name of the VRF. Defaults to "default".

    Returns:
      list: A list of ISIS interfaces.

    """
    return output_to_json(isis_interfaces(device_name, vrf_name))
