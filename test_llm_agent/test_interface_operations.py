"""
This script is used to test interface operations
"""

from pprint import pprint as pp
from test_llm_agent.load_test_settings import DEVICE_NAME, INTERFACE_NAME

from llm_agent.pyats.api.interface_operations import (
    shut_interface,
    unshut_interface,
)
from llm_agent.pyats.api.interface_state import interfaces_status


if __name__ == "__main__":
    pp(interfaces_status(device_name=DEVICE_NAME))

    pp(shut_interface(device_name=DEVICE_NAME, interface_name=INTERFACE_NAME))

    pp(interfaces_status(device_name=DEVICE_NAME))

    pp(
        unshut_interface(
            device_name=DEVICE_NAME, interface_name=INTERFACE_NAME
        )
    )
    pp(interfaces_status(device_name=DEVICE_NAME))
