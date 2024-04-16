from langchain.agents import tool

from pyats_tools.pyats_utils import output_to_json
from pyats_tools.pyats_connection import PyATSConnection


@tool
def get_interfaces_status(device_name: str) -> dict:
    """
    Get the status of interfaces on a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      dict: A dictionary containing the status of the interfaces on the device.
    """
    return output_to_json(_get_interfaces_status(device_name))


def _get_interfaces_status(device_name: str) -> dict:
    with PyATSConnection(device_name=device_name) as device:
        try:
            return device.api.get_interfaces_status()
        except Exception as e:
            return {"get_interfaces_status_error": e}


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
    return output_to_json(
        _get_single_interface_status(device_name, interface_name)
    )


def _get_single_interface_status(
    device_name: str, interface_name: str
) -> dict:
    with PyATSConnection(device_name=device_name) as device:
        try:
            output = device.parse(f"show interfaces {interface_name}")
        except Exception as e:
            return {"get_single_interface_status_error": e}
        return output.get(interface_name, "ERROR_INTERFACE_NOT_FOUND")


@tool
def get_interface_information(
    device_name: str, interfaces_name: list[str]
) -> list[dict]:
    """
    TODO: Need to reduce the amount of information returned
    Get interface information from device for a list of interfaces

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interfaces_name (list[str]): A list of interface names

    Returns:
      list[dict]: A list of dictionaries containing interface information
    """
    return output_to_json(
        _get_interface_information(device_name, interfaces_name)
    )


def _get_interface_information(
    device_name: str, interfaces_name: list[str]
) -> str:
    with PyATSConnection(device_name=device_name) as device:
        try:
            return device.api.get_interface_information(interfaces_name)
        except Exception as e:
            return {"get_interface_information_error": e}


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
    return output_to_json(
        _get_interface_admin_status(device_name, interface_name)
    )


def _get_interface_admin_status(device_name: str, interface_name: str) -> str:
    with PyATSConnection(device_name=device_name) as device:
        try:
            return device.api.get_interface_admin_status(interface_name)
        except Exception as e:
            return {"get_interface_admin_status_error": e}


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
    return output_to_json(
        _verify_interface_state_up(device_name, interface_name)
    )


def _verify_interface_state_up(device_name: str, interface_name: str) -> bool:
    with PyATSConnection(device_name=device_name) as device:
        try:
            return device.api.verify_interface_state_up(interface_name)
        except Exception as e:
            return {"verify_interface_state_up_error": e}


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
    return output_to_json(_get_interface_events(device_name, interface_name))


def _get_interface_events(device_name: str, interface_name: str) -> dict:
    with PyATSConnection(device_name=device_name) as device:
        try:
            return device.parse(f"show logging | i {interface_name}")
        except Exception as e:
            return {"get_interface_events_error": e}


if __name__ == "__main__":
    """
    To run locally, you need to adjust the import statements.
    TODO: Find a better way to import when running locally.
    """
    from pprint import pprint as pp
    from tests.load_test_settings import test_device, interface_name

    pp(
        _get_interface_information(
            device_name=test_device, interfaces_name=[interface_name]
        )
    )
    pp(_get_interfaces_status(device_name=test_device))
    pp(
        _get_single_interface_status(
            device_name=test_device, interface_name=interface_name
        )
    )
    pp(
        _get_interface_admin_status(
            device_name=test_device, interface_name=interface_name
        )
    )
    pp(
        _verify_interface_state_up(
            device_name=test_device, interface_name=interface_name
        )
    )
