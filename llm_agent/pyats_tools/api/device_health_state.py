from langchain.agents import tool

from pyats_tools.pyats_utils import output_to_json
from pyats_tools.pyats_connection import PyATSConnection


@tool
def get_health_memory(device_name: str) -> dict:
    """
    Retrieves the memory health information for a given device.

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      dict: A dictionary containing the memory health information. Empty is good.
    """
    return output_to_json(_health_memory(device_name))


def _health_memory(device_name: str) -> dict:
    with PyATSConnection(device_name=device_name) as device:
        try:
            result = device.api.health_memory()
            if not result["health_data"]:
                return {
                    "message": "No memory health issues detected on the device"
                }
            return result
        except Exception as e:
            return {"health_memory_error": e}


@tool
def get_health_cpu(device_name: str) -> dict:
    """
    Retrieves the CPU health information for a given device.

    Args:
      device_name (str): Must come from the function get_devices_list_available

    Returns:
      dict: A dictionary containing the CPU health information. Empty is good.
    """
    return _health_cpu(device_name)


def _health_cpu(device_name: str) -> dict:
    with PyATSConnection(device_name=device_name) as device:
        try:
            result = device.api.health_cpu()
            if not result["health_data"]:
                return {
                    "message": "No CPU health issues detected on the device"
                }
            return result
        except Exception as e:
            return {"health_cpu_error": e}


@tool
def get_health_logging(
    device_name: str,
    keywords: list[str] = None,
) -> dict:
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
    return output_to_json(_health_logging(device_name, keywords))


def _health_logging(
    device_name: str,
    keywords: list[str] = None,
) -> dict:
    if keywords is None:
        keywords = [
            "traceback",
            "Traceback",
            "TRACEBACK",
            "rror",
            "own",
            "ADJCHANGE",
        ]
    with PyATSConnection(device_name=device_name) as device:
        try:
            result = device.api.health_logging(keywords=keywords)
            if not result["health_data"]:
                return {
                    "message": "No issues detected on the logs of the device"
                }
            return result
        except Exception as e:
            return {"health_logging_error": e}


if __name__ == "__main__":
    """
    To run locally, you need to adjust the import statements.
    TODO: Find a better way to import when running locally.
    """
    from pprint import pprint as pp
    from tests.load_test_settings import test_device

    pp(_health_memory(device_name=test_device))
    pp(_health_cpu(device_name=test_device))
    pp(_health_logging(device_name=test_device))
