"""
This script is used to test the interface state
"""

from pprint import pprint as pp
from test_llm_agent.load_test_settings import DEVICE_NAME

from llm_agent.pyats.api.routing import (
    vrfs_present,
    interface_interfaces_under_vrf,
    route_entries,
)

VRF_DEFAULT = "default"

if __name__ == "__main__":
    pp(vrfs_present(device_name=DEVICE_NAME))

    pp(
        interface_interfaces_under_vrf(
            device_name=DEVICE_NAME, vrf_name=VRF_DEFAULT
        )
    )

    pp(route_entries(device_name=DEVICE_NAME))
