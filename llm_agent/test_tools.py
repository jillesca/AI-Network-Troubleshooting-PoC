from pyats_tools.api.interfaces_config_api import (
    _get_interfaces_description,
)


if __name__ == "__main__":
    from pprint import pprint as pp
    from tests.load_test_settings import test_device, interface_name

    pp(_get_interfaces_description(device_name="cat8000v-0"))
