from pyats_tools.api.interface_operations import (
    shut_interface,
    unshut_interface,
)
from pyats_tools.api.interface_state import _get_interfaces_status


if __name__ == "__main__":
    from pprint import pprint as pp

    pp(_get_interfaces_status(device_name="cat8000v-0"))
    pp(
        shut_interface(
            device_name="cat8000v-0", interface_name="GigabitEthernet2"
        )
    )
    pp(_get_interfaces_status(device_name="cat8000v-0"))
    pp(
        unshut_interface(
            device_name="cat8000v-0", interface_name="GigabitEthernet2"
        )
    )
    pp(_get_interfaces_status(device_name="cat8000v-0"))
