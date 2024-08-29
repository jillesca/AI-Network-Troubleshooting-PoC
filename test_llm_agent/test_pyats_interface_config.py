"""
This script is used to test the interface configuration
"""

from pprint import pprint as pp
from test_llm_agent.load_test_settings import DEVICE_NAME, INTERFACE_NAME

from llm_agent.pyats_connector.api.interface_config import (
    interface_running_config,
    interfaces_description,
)


if __name__ == "__main__":
    pp(
        interface_running_config(
            device_name=DEVICE_NAME, interface_name=INTERFACE_NAME
        )
    )

    pp(interfaces_description(device_name=DEVICE_NAME))
