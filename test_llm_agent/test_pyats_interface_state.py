"""
This script is used to test the interface state
"""

from pprint import pprint as pp
from test_llm_agent.load_test_settings import DEVICE_NAME, INTERFACE_NAME

from llm_agent.pyats_connector.api.interface_state import (
    interfaces_status,
    single_interface_status,
    interfaces_information,
    interface_admin_status,
    verify_state_up,
    interface_events,
)

INTERFACES_NAME = ["GigabitEthernet1", "GigabitEthernet2"]

if __name__ == "__main__":
    pp(interfaces_status(device_name=DEVICE_NAME))

    pp(
        single_interface_status(
            device_name=DEVICE_NAME, interface_name=INTERFACE_NAME
        )
    )

    pp(
        interfaces_information(
            device_name=DEVICE_NAME, interfaces_name=INTERFACES_NAME
        )
    )

    pp(
        interface_admin_status(
            device_name=DEVICE_NAME, interface_name=INTERFACE_NAME
        )
    )

    pp(verify_state_up(device_name=DEVICE_NAME, interface_name=INTERFACE_NAME))

    pp(
        interface_events(
            device_name=DEVICE_NAME, interface_name=INTERFACE_NAME
        )
    )
