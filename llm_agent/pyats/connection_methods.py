"""
This module provides functions for connecting to devices using PyATSConnection API. 
"""

from typing import Optional, Union, Dict

from llm_agent.log_config.logger_setup import logger
from llm_agent.pyats.connection_handler import PyATSConnection


def api_connect(
    device_name: str,
    method: str,
    args: Optional[Union[str, Dict[str, str]]] = None,
) -> any:
    """
    Connects to a device using PyATSConnection API and executes a specified method.

    Args:
      device_name (str): The name of the device to connect to.
      method (str): The name of the method to execute on the device.
      args (dict, optional): A dictionary of arguments to pass to the method. Defaults to None.

    Returns:
      dict: A dictionary containing the result of the method execution or an exception if an error occurs.
    """
    logger.info("EXECUTING METHOD: %s, DEVICE: %s", method, device_name)
    logger.info("ARGS: %s", args)
    with PyATSConnection(device_name=device_name) as device_connection:
        method_to_call = getattr(device_connection.api, method)
        try:
            if isinstance(args, dict):
                return method_to_call(**args)
            elif isinstance(args, str):
                return method_to_call(args)
            elif isinstance(args, list):
                return method_to_call(args)
            else:
                return method_to_call()
        except Exception as e:
            return {method.__name__: e}


def parse_connect(device_name: str, string_to_parse: str) -> any:
    """
    Connects to a device using PyATSConnection parse and executes a specified method.

    Args:
      device_name (str): The name of the device to connect to.
      method (str): The name of the method to execute on the device.
      args (dict, optional): A dictionary of arguments to pass to the method. Defaults to None.

    Returns:
      dict: A dictionary containing the result of the method execution or an exception if an error occurs.
    """
    logger.info("Parsing: %s, DEVICE: %s", string_to_parse, device_name)
    with PyATSConnection(device_name=device_name) as device_connection:
        method = getattr(device_connection, "parse")
        try:
            return method(string_to_parse)
        except Exception as e:
            return {method.__name__: e}
