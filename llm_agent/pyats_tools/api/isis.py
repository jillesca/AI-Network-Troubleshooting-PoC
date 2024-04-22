from langchain.agents import tool
from genie.libs.parser.iosxe.show_isis import (
    ShowIsisNeighbors,
)

from pyats_tools.pyats_utils import output_to_json
from pyats_tools.pyats_connection import PyATSConnection


@tool
def verify_active_isis_neighbors(device_name: str) -> dict:
    """
    Retrieves the ISIS neighbors for a given device. Neighbors down are not included.

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      dict: A dictionary containing the ISIS neighbors information.
    """
    return output_to_json(_get_isis_neighbors(device_name))


def _get_isis_neighbors(device_name: str) -> dict:
    with PyATSConnection(device_name=device_name) as device:
        try:
            return ShowIsisNeighbors(device=device).parse()
        except Exception as e:
            return {
                "get_isis_neighbors_error": f"NO_ISIS_NEIGHBORS_FOUND_ON: {device_name}"
            }


@tool
def get_isis_interface_events(device_name: str) -> dict:
    """
    Retrieves ISIS interface events for a given device.

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      dict: A dictionary containing the ISIS interface events.
    """
    return output_to_json(_get_isis_interface_events(device_name))


def _get_isis_interface_events(device_name: str) -> dict:
    with PyATSConnection(device_name=device_name) as device:
        try:
            return device.parse("show isis lsp-log")
        except Exception as e:
            return {
                "get_isis_interface_events_error": f"NO_ISIS_CONFIGURED_ON: {device_name}"
            }


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
    return output_to_json(_get_isis_interfaces(device_name, vrf_name))


def _get_isis_interfaces(device_name: str, vrf_name: str = "default") -> list:
    with PyATSConnection(device_name=device_name) as device:
        try:
            data = device.parse("show ip protocols")
        except Exception as e:
            return [f"NO_ISIS_INTERFACES_FOUND_FOR_VRF_{vrf_name}"]

        isis_interfaces = _extract_isis_interfaces(data=data)
        return isis_interfaces.get(
            vrf_name, f"NO_ISIS_INTERFACES_FOUND_FOR_VRF:{vrf_name}"
        )


def _extract_isis_interfaces(data: dict) -> dict:
    isis_data = data.get("protocols", {}).get("isis", {}).get("vrf", {})
    result = {}
    for vrf, vrf_data in isis_data.items():
        interfaces = (
            vrf_data.get("address_family", {})
            .get("ipv4", {})
            .get("instance", {})
            .get("default", {})
            .get("configured_interfaces")
        )
        if interfaces is not None:
            result[vrf] = interfaces
    return result


if __name__ == "__main__":
    """
    To run locally, you need to adjust the import statements.
    TODO: Find a better way to import when running locally.
    """
    from pprint import pprint as pp
    from tests.load_test_settings import test_device, interface_name

    # pp(_get_isis_neighbors(device_name=device))
    pp(_get_isis_interfaces(device_name=test_device))
