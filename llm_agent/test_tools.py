from pyats_tools.api.device_health_state import (
    health_cpu,
    health_memory,
    health_logging,
)


if __name__ == "__main__":
    from pprint import pprint as pp

    pp(health_logging(device_name="cat8000v-0"))
    pp(health_memory(device_name="cat8000v-0"))
    pp(health_cpu(device_name="cat8000v-0"))
