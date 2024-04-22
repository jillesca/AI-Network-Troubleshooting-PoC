from pyats_tools.pyats_connection import api_connect, parse_connect


def interface_running_config(device_name: str, interface_name: str) -> dict:
    """
    Get the running config of a single interface on a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interface_name (str): The name of the interface.

    Returns:
      dict: The running configuration of the specified interface.
    """
    return api_connect(
        device_name=device_name,
        method="get_interface_running_config",
        args=interface_name,
    )


def interfaces_description(device_name: str) -> dict:
    """
    Get the description of the interfaces per device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interface_name (str): The name of the interface.

    Returns:
      dict: A dictionary containing the status of the interface.
    """
    result = parse_connect(
        device_name=device_name, string_to_parse="show interfaces description"
    )

    return result.get("interfaces", "ERROR_GETTING_INTERFACES_DESCRIPTION")
