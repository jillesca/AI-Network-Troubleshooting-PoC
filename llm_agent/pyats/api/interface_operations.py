""" 
Script to perform operations on a device interface using the pyATS framework.
"""

from llm_agent.pyats.connection_methods import api_connect


def shut_interface(device_name: str, interface_name: str) -> dict:
    """
    Shuts down the specified interface on the given device.

    Args:
      device_name (str): The name of the device.
      interface_name (str): The name of the interface to shut down.

    Returns:
      dict: A dictionary containing the result of the operation.
    """
    return api_connect(
        device_name=device_name,
        method="shut_interface",
        args=interface_name,
    )


def unshut_interface(device_name: str, interface_name: str) -> dict:
    """
    Unshuts the specified interface on the given device.

    Args:
      device_name (str): The name of the device.
      interface_name (str): The name of the interface to unshut.

    Returns:
      dict: A dictionary containing the result of the operation.

    """
    return api_connect(
        device_name=device_name,
        method="unshut_interface",
        args=interface_name,
    )
