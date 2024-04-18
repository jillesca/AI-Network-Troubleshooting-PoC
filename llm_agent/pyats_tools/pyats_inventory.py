from pyats.topology import loader
from langchain.agents import tool

from load_global_settings import TESTBED_FILE
from utils.text_utils import output_to_json


@tool
def get_devices_list_available() -> list:
    """
    Retrieves the list of valid available devices.

    Returns:
      A list representation of the available devices.
    """
    return output_to_json(get_devices_from_inventory())


def get_devices_from_inventory() -> list:
    topology = loader.load(TESTBED_FILE)
    return list(topology.devices.names)


if __name__ == "__main__":
    """
    To run locally, you need to adjust the import statements.
    TODO: Find a better way to import when running locally.
    """
    print(get_devices_from_inventory())
