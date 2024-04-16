from utils.text_utils import load_json_file

TEST_SETTINGS_FILE = "llm_agent/tests/test_settings.json"

test_config = load_json_file(json_file=TEST_SETTINGS_FILE)

test_device = test_config.get("device", "cat8000v-0")
interface_name = test_config.get("interface_name", "GigabitEthernet2")
