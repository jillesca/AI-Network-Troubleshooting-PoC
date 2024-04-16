from langchain.agents import tool

from pyats_tools.pyats_utils import output_to_json
from pyats_tools.pyats_connection import PyATSConnection


@tool
def get_vrf_present(device_name: str) -> list:
    """
    Get all vrfs from device

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      list: List of vrfs present on the device
    """
    return output_to_json(_get_vrf_present(device_name))


def _get_vrf_present(device_name: str) -> list:
    with PyATSConnection(device_name=device_name) as device:
        try:
            return list(device.api.get_vrf_vrfs().keys())
        except Exception:
            return ["NO_VRFs_FOUND"]


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
        _get_interface_interfaces_under_vrf(device_name, vrf_name)
    )


def _get_interface_interfaces_under_vrf(
    device_name: str, vrf_name: str = None
) -> list:
    with PyATSConnection(device_name=device_name) as device:
        try:
            return device.api.get_interface_interfaces_under_vrf(vrf=vrf_name)
        except Exception:
            return [f"NO_INTERFACES_FOUND_FOR_VRF_{vrf_name}"]


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
    return output_to_json(
        _get_routing_routes(device_name, vrf_name, address_family)
    )


def _get_routing_routes(
    device_name: str, vrf_name: str = None, address_family: str = "ipv4"
) -> dict:
    with PyATSConnection(device_name=device_name) as device:
        try:
            return device.api.get_routing_routes(
                vrf=vrf_name, address_family=address_family
            )
        except Exception:
            return {"error": f"NO_ROUTES_FOUND_FOR_VRF_{vrf_name}"}


if __name__ == "__main__":
    """
    To run locally, you need to adjust the import statements.
    TODO: Find a better way to import when running locally.
    """
    from pprint import pprint as pp
    from tests.load_test_settings import test_device

    pp(_get_vrf_present(device_name=test_device))
    pp(
        _get_interface_interfaces_under_vrf(
            device_name=test_device, vrf_name="Mgmt-intf"
        )
    )
    pp(_get_routing_routes(device_name=test_device, vrf_name="Mgmt-intf"))
