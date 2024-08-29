"""
Script to retrieve the health state of a device using the pyATS framework.
"""

from llm_agent.pyats_connector.connection_methods import api_connect


def health_memory(device_name: str) -> dict:
    """
    Retrieves the memory health information for a given device.

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      dict: A dictionary containing the memory health information. Empty is good.
    """
    result = api_connect(device_name=device_name, method="health_memory")
    if not result["health_data"]:
        return {"message": "No memory health issues detected on the device"}
    return result


def health_cpu(device_name: str) -> dict:
    """
    Retrieves the CPU health information for a given device.

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      dict: A dictionary containing the CPU health information. Empty is good.
    """
    result = api_connect(device_name=device_name, method="health_cpu")
    if not result["health_data"]:
        return {"message": "No CPU health issues detected on the device"}
    return result


def health_logging(device_name: str, keywords: list[str] = None) -> dict:
    """
    Retrieves health logging information from a device.

    Args:
      device_name (str): Must come from the function get_devices_list_available
      keywords (list[str], optional): List of keywords to filter the health logging information.
        Defaults to traceback, error, down and adjchange.

    Returns:
      dict: The health logging information in JSON format.
    """
    if keywords is None:
        keywords = [
            "traceback",
            "Traceback",
            "TRACEBACK",
            "rror",
            "own",
            "ADJCHANGE",
        ]

    result = api_connect(
        device_name=device_name,
        method="health_logging",
        args={"keywords": keywords},
    )

    if not result["health_data"]:
        return {"message": "No issues detected on the logs of the device"}
    return result
