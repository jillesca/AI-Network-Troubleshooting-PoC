"""
Wrapper functions to work with langchain tools and openAI
"""

from langchain.agents import tool

from llm_agent.utils.text_utils import output_to_json
from llm_agent.pyats_connector.api.routing import (
    vrfs_present,
    interface_interfaces_under_vrf,
    route_entries,
)


@tool
def get_vrf_present(device_name: str) -> list:
    """
    Get all vrfs from device

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      list: List of vrfs present on the device
    """
    return output_to_json(vrfs_present(device_name))


@tool
def get_interface_interfaces_under_vrf(
    device_name: str, vrf_name: str = None
) -> list:
    """
    Get interfaces configured under specific Vrf

    Args:
      device_name (str): Must come from the function get_devices_list_available
      vrf_name (str, optional): Name of the VRF. Defaults to None.

    Returns:
      list: List of interfaces configured under the specified VRF
    """
    return output_to_json(
        interface_interfaces_under_vrf(device_name, vrf_name)
    )


@tool
def get_routing_routes(
    device_name: str, vrf_name: str = None, address_family: str = "ipv4"
) -> dict:
    """
    TODO: Need to reduce the amount of inrormation returned
    Execute 'show ip route vrf <vrf>' and retrieve the routes

    Args:
      device_name (str): Must come from the function get_devices_list_available
      vrf_name (str, optional): The name of the VRF. Defaults to None.
      address_family (str, optional): The address family name. Defaults to "ipv4".

    Returns:
      dict: A dictionary containing the received routes.
    """
    return output_to_json(route_entries(device_name, vrf_name, address_family))
