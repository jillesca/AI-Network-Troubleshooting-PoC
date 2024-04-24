"""
This module provides a class for managing pyATS connections.
"""

import logging
from dataclasses import dataclass
from typing import Optional


from pyats.topology import loader, Device

from llm_agent.pyats.inventory import get_devices_from_inventory
from llm_agent.config.global_settings import TESTBED_FILE
from llm_agent.log_config.logger_setup import logger


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
        # So the connection close faster
        self.device_pyats.settings.GRACEFUL_DISCONNECT_WAIT_SEC = 0
        self.device_pyats.settings.POST_DISCONNECT_WAIT_SEC = 0

    def _connection_handler(self) -> None:
        for _ in range(NUMBER_OF_TRIES_TO_CONNECT):
            try:
                self._connect_to_device()
                break
            except ConnectionError as e:
                logger.error("Connection failed: %s", e)

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
            logger.error("An error occurred: %s", exc_val)
        self.device_pyats.disconnect()
        logger.info("CONNECTION CLOSED")

        return False
