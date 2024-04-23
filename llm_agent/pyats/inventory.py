""" 
Script to retrieve the devices from the inventory using the pyATS framework.
"""

from pyats.topology import loader

from llm_agent.config.load_global_settings import TESTBED_FILE


def get_devices_from_inventory() -> list:
    """
    Retrieves a list of devices from the inventory.

    Returns:
      list: A list of device names.
    """
    topology = loader.load(TESTBED_FILE)
    return list(topology.devices.names)
