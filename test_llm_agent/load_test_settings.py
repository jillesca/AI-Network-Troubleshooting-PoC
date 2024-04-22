"""
Load test settings from JSON file.
"""

import json

TEST_SETTINGS_FILE = "test_llm_agent/test_settings.json"


def load_json_file(json_file: str) -> dict:
    """
    Load JSON file.
    """
    with open(json_file, encoding="utf-8") as f:
        return json.load(f)


test_config = load_json_file(json_file=TEST_SETTINGS_FILE)
DEVICE_NAME = test_config.get("device")
INTERFACE_NAME = test_config.get("interface_name")
