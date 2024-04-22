"""
This module provides a class for managing pyATS connections.
"""

import logging
from dataclasses import dataclass
from typing import Optional, Union, Dict


from pyats.topology import loader, Device

from llm_agent.logging_config.main import setup_logging
from llm_agent.load_global_settings import TESTBED_FILE
from llm_agent.pyats.pyats_inventory import get_devices_from_inventory

logger = setup_logging()
NUMBER_OF_TRIES_TO_CONNECT = 10


@dataclass
class PyATSConnection:
    """
    A class to manage pyATS connections.
    """

    device_name: str
    testbed_file: str = TESTBED_FILE
    device_pyats: Optional[Device] = None

    def __enter__(self):
        logger.debug("CREATING INSTANCE")
        self._establish_connection()
        return self.device_pyats

    def _establish_connection(self) -> Device:
        """
        Establish a connection to a device using pyATS.
        """

        logger.debug("LOADING DEVICES")
        self._load_devices_from_testbed()
        self._connection_handler()
        self._set_device_settings()

    def _load_devices_from_testbed(self) -> None:
        testbed = loader.load(self.testbed_file)
        try:
            self.device_pyats = testbed.devices[self.device_name]
        except KeyError as exc:
            devices_available = get_devices_from_inventory()
            raise KeyError(
                f"Device {self.device_name} not found in testbed. Devices available are: {devices_available}"
            ) from exc

    def _set_device_settings(self) -> None:
        self.device_pyats.settings.GRACEFUL_DISCONNECT_WAIT_SEC = 0
        self.device_pyats.settings.POST_DISCONNECT_WAIT_SEC = 0

    def _connection_handler(self) -> None:
        for _ in range(NUMBER_OF_TRIES_TO_CONNECT):
            try:
                self._connect_to_device()
                break
            except ConnectionError as e:
                logger.error(f"Connection failed: {e}")

    def _connect_to_device(self) -> None:
        logger.info("ESTABLISHING CONNECTION")
        self.device_pyats.connect(
            mit=True,
            via="cli",
            learn_hostname=True,
            connection_timeout=10,
            log_stdout=self._get_logging_level(),
        )

    def _get_logging_level(self) -> bool:
        return logger.getEffectiveLevel() == logging.DEBUG

    def __exit__(self, exc_type, exc_val, exc_tb):
        logger.debug("CLOSING CONNECTION")
        if exc_type is not None:
            logger.error(f"An error occurred: {exc_val}")
        self.device_pyats.disconnect()
        logger.info("CONNECTION CLOSED")

        return False


def api_connect(
    device_name: str,
    method: str,
    args: Optional[Union[str, Dict[str, str]]] = None,
):
    """
    Connects to a device using PyATSConnection API and executes a specified method.

    Args:
      device_name (str): The name of the device to connect to.
      method (str): The name of the method to execute on the device.
      args (dict, optional): A dictionary of arguments to pass to the method. Defaults to None.

    Returns:
      dict: A dictionary containing the result of the method execution or an exception if an error occurs.
    """
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


def parse_connect(device_name: str, string_to_parse: str):
    """
    Connects to a device using PyATSConnection parse and executes a specified method.

    Args:
      device_name (str): The name of the device to connect to.
      method (str): The name of the method to execute on the device.
      args (dict, optional): A dictionary of arguments to pass to the method. Defaults to None.

    Returns:
      dict: A dictionary containing the result of the method execution or an exception if an error occurs.
    """
    with PyATSConnection(device_name=device_name) as device_connection:
        method = getattr(device_connection, "parse")
        try:
            return method(string_to_parse)
        except Exception as e:
            return {method.__name__: e}
