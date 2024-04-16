from langchain.agents import tool

from pyats_tools.pyats_utils import output_to_json
from pyats_tools.pyats_connection import PyATSConnection


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
        _get_interface_running_config(device_name, interface_name)
    )


def _get_interface_running_config(
    device_name: str, interface_name: str
) -> dict:
    with PyATSConnection(device_name=device_name) as device:
        try:
            return device.api.get_interface_running_config(interface_name)
        except Exception as e:
            return {"get_interface_running_config_error": e}


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
    return output_to_json(_get_interfaces_description(device_name))


def _get_interfaces_description(device_name: str) -> dict:
    with PyATSConnection(device_name=device_name) as device:
        try:
            output = device.parse("show interfaces description")
        except Exception as e:
            return {"get_single_interface_status_error": e}
        return output.get("interfaces", "ERROR_GETTING_INTERFACES_DESCRIPTION")


if __name__ == "__main__":
    """
    To run locally, you need to adjust the import statements.
    TODO: Find a better way to import when running locally.
    """
