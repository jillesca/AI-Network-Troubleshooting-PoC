from pyats_tools.pyats_inventory import get_devices_list_available
from pyats_tools.api.device_health_state import (
    get_health_memory,
    get_health_cpu,
    get_health_logging,
)
from pyats_tools.api.interfaces_config_api import (
    get_interface_running_config,
    get_interfaces_description,
)
from pyats_tools.api.interfaces_operations_api import (
    shut_interface,
    unshut_interface,
)
from pyats_tools.api.interfaces_state_api import (
    get_interfaces_status,
    get_single_interface_status,
    get_interface_information,
    get_interface_admin_status,
    verify_interface_state_up,
    get_interface_events,
)
from pyats_tools.api.isis_api import (
    verify_active_isis_neighbors,
    get_isis_interface_events,
    get_isis_interface_information,
)
from pyats_tools.api.routing_api import (
    get_vrf_present,
    get_interface_interfaces_under_vrf,
    get_routing_routes,
)

tools = [
    get_devices_list_available,
    get_health_memory,
    get_health_cpu,
    get_health_logging,
    get_interface_running_config,
    shut_interface,
    unshut_interface,
    get_interfaces_status,
    get_single_interface_status,
    get_interface_information,
    get_interfaces_description,
    get_interface_admin_status,
    verify_interface_state_up,
    get_interface_events,
    verify_active_isis_neighbors,
    get_isis_interface_events,
    get_isis_interface_information,
    get_vrf_present,
    get_interface_interfaces_under_vrf,
    get_routing_routes,
]
