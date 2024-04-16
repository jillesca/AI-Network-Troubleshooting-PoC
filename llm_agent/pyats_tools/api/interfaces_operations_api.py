from langchain.agents import tool

from pyats_tools.pyats_utils import output_to_json
from pyats_tools.pyats_connection import PyATSConnection


@tool
def shut_interface(device_name: str, interface_name: str) -> None:
    """
    Shut down an interface on a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interface_name (str): The name of the interface to shut down.

    Returns:
      None
    """
    return output_to_json(_shut_interface(device_name, interface_name))


def _shut_interface(device_name: str, interface_name: str) -> None:
    with PyATSConnection(device_name=device_name) as device:
        try:
            return device.api.shut_interface(interface_name)
        except Exception as e:
            return {"shut_interface_error": e}


@tool
def unshut_interface(device_name: str, interface_name: str) -> None:
    """
    Shut down an interface on a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      interface_name (str): The name of the interface to be shut down.

    Returns:
      None
    """
    return output_to_json(_unshut_interface(device_name, interface_name))


def _unshut_interface(device_name: str, interface_name: str) -> None:
    with PyATSConnection(device_name=device_name) as device:
        try:
            device.api.unshut_interface(interface_name)
        except Exception as e:
            return {"unshut_interface_error": e}


if __name__ == "__main__":
    """
    To run locally, you need to adjust the import statements.
    TODO: Find a better way to import when running locally.
    """
    from pprint import pprint as pp
    from tests.load_test_settings import test_device, interface_name

    pp(_shut_interface(device_name=test_device, interface_name=interface_name))
    pp(
        _unshut_interface(
            device_name=test_device, interface_name=interface_name
        )
    )
