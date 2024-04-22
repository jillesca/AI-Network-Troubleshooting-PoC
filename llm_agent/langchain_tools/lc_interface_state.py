"""
Wrapper functions to work with langchain tools and openAI
"""

from langchain.agents import tool

from pyats.pyats_utils import output_to_json
from pyats.api.interface_state import (
    interfaces_status,
    single_interface_status,
    interfaces_information,
    interface_admin_status,
    verify_state_up,
    interface_events,
)


@tool
def get_interfaces_status(device_name: str) -> dict:
    """
    Get the status of interfaces on a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      dict: A dictionary containing the status of the interfaces on the device.
    """
    return output_to_json(interfaces_status(device_name))


@tool
def get_single_interface_status(device_name: str, interface_name: str) -> dict:
    """
    Get the status of a single interface on a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interface_name (str): The name of the interface.

    Returns:
      dict: A dictionary containing the status of the interface.
    """
    return output_to_json(single_interface_status(device_name, interface_name))


@tool
def get_interface_information(
    device_name: str, interfaces_name: list[str]
) -> list[dict]:
    """
    Get interface information from device for a list of interfaces

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interfaces_name (list[str]): A list of interface names

    Returns:
      list[dict]: A list of dictionaries containing interface information
    """
    return output_to_json(interfaces_information(device_name, interfaces_name))


@tool
def get_interface_admin_status(device_name: str, interface_name: str) -> str:
    """
    Get the administrative status of a single interface on a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interface_name (str): The name of the interface.

    Returns:
      str: The administrative status of the interface.

    """
    return output_to_json(interface_admin_status(device_name, interface_name))


@tool
def verify_interface_state_up(device_name: str, interface_name: str) -> bool:
    """
    Verify interface state is up and line protocol is up

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interface_name (str): The name of the interface

    Returns:
      bool: True if the interface state is up and line protocol is up, False otherwise
    """
    return output_to_json(verify_state_up(device_name, interface_name))


@tool
def get_interface_events(device_name: str, interface_name: str) -> dict:
    """
    Retrieves the events for a specific interface on a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interface_name (str): The name of the interface.

    Returns:
      dict: A dictionary containing the events for the specified interface.
    """
    return output_to_json(interface_events(device_name, interface_name))
