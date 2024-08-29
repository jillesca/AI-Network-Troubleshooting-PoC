"""
This script is used to test the interface state
"""

from pprint import pprint as pp
from test_llm_agent.load_test_settings import DEVICE_NAME

from llm_agent.pyats_connector.api.isis import (
    isis_neighbors,
    isis_interface_events,
    isis_interfaces,
)

VRF = "default"
INTERFACES_NAME = ["GigabitEthernet1", "GigabitEthernet2"]

if __name__ == "__main__":
    pp(isis_neighbors(device_name=DEVICE_NAME))

    pp(isis_interface_events(device_name=DEVICE_NAME))

    pp(isis_interfaces(device_name=DEVICE_NAME, vrf_name=VRF))
