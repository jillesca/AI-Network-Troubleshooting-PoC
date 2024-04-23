""" 
Import all the tools from the langchain_tools folder
"""

from llm_agent.pyats.inventory import get_devices_list_available
from llm_agent.langchain_tools.lc_device_health_state import (
    get_health_memory,
    get_health_cpu,
    get_health_logging,
)
from llm_agent.langchain_tools.lc_interface_config import (
    get_interface_running_config,
    get_interfaces_description,
)
from llm_agent.langchain_tools.lc_interface_operations import (
    action_shut_interface,
    action_unshut_interface,
)
from llm_agent.langchain_tools.lc_interface_state import (
    get_interfaces_status,
    get_single_interface_status,
    get_interface_information,
    get_interface_admin_status,
    verify_interface_state_up,
    get_interface_events,
)
from llm_agent.langchain_tools.lc_isis import (
    verify_active_isis_neighbors,
    get_isis_interface_events,
    get_isis_interface_information,
)
from llm_agent.langchain_tools.lc_routing import (
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
    action_shut_interface,
    action_unshut_interface,
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
