"""
This script is used to test the device health state operations.
"""

from pprint import pprint as pp
from test_llm_agent.load_test_settings import DEVICE_NAME

from llm_agent.pyats.api.device_health_state import (
    health_cpu,
    health_memory,
    health_logging,
)


if __name__ == "__main__":
    pp(health_cpu(device_name=DEVICE_NAME))
    pp(health_memory(device_name=DEVICE_NAME))
    pp(health_logging(device_name=DEVICE_NAME))
