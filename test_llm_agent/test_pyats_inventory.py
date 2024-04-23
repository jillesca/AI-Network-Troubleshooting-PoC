"""
This script is used to test the get_devices_from_inventory function
"""

from pprint import pprint as pp


from llm_agent.pyats.inventory import (
    get_devices_from_inventory,
)

if __name__ == "__main__":
    pp(get_devices_from_inventory())
