""" 
Script to retrieve the status of a device interface using the pyATS framework.
"""

from llm_agent.pyats.pyats_connection import api_connect, parse_connect


def interfaces_status(device_name: str) -> dict:
    """
    Retrieves the status of interfaces on a given device.

    Args:
      device_name (str): The name of the device.

    Returns:
      dict: A dictionary containing the status of interfaces on the device.
    """
    return api_connect(
        device_name=device_name,
        method="get_interfaces_status",
    )


def single_interface_status(device_name: str, interface_name: str) -> dict:
    """
    Retrieves the status of a single interface on a device.

    Args:
      device_name (str): The name of the device.
      interface_name (str): The name of the interface.

    Returns:
      dict: A dictionary containing the status of the interface. If the interface is not found,
          the value "ERROR_INTERFACE_NOT_FOUND" is returned.
    """
    result = parse_connect(
        device_name=device_name,
        string_to_parse=f"show interfaces {interface_name}",
    )
    return result.get(interface_name, "ERROR_INTERFACE_NOT_FOUND")


def interfaces_information(
    device_name: str, interfaces_name: list[str]
) -> str:
    """
    Retrieves interface information for the specified device and interfaces.
    TODO: Need to reduce the amount of information returned

    Args:
      device_name (str): The name of the device.
      interfaces_name (list[str]): A list of interface names.

    Returns:
      str: The interface information.

    """
    return api_connect(
        device_name=device_name,
        method="get_interface_information",
        args=interfaces_name,
    )


def interface_admin_status(device_name: str, interface_name: str) -> str:
    """
    Retrieves the administrative status of a network interface on a device.

    Args:
      device_name (str): The name or IP address of the device.
      interface_name (str): The name of the network interface.

    Returns:
      str: A message indicating the administrative status of the network interface.

    """
    result = api_connect(
        device_name=device_name,
        method="get_interface_admin_status",
        args=interface_name,
    )
    return f"Interface {interface_name} on device {device_name} is set to: {result} (Admin Status)"


def verify_state_up(device_name: str, interface_name: str) -> bool:
    """
    Verify if the interface state is up on a given device.

    Args:
      device_name (str): The name of the device to connect to.
      interface_name (str): The name of the interface to verify.

    Returns:
      str: A message indicating whether the interface state is up or not.
    """
    result = api_connect(
        device_name=device_name,
        method="verify_interface_state_up",
        args=interface_name,
    )
    state = "UP" if result else "NOT UP"
    return f"The interface {interface_name} on device {device_name} is {state}"


def interface_events(device_name: str, interface_name: str) -> dict:
    """
    Retrieve interface events for a specific device and interface.

    Args:
      device_name (str): The name of the device.
      interface_name (str): The name of the interface.

    Returns:
      dict: A dictionary containing the parsed interface events.

    """
    return parse_connect(
        device_name=device_name,
        string_to_parse=f"show logging | i {interface_name}",
    )
