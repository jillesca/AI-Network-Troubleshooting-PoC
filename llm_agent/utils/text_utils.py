import json


def output_to_json(data: str) -> str:
    """
    Convert python to JSON string.
    """
    return json.dumps(data)


def remove_white_spaces(string: str) -> str:
    """
    Removes extra white spaces from a string.
    """
    return " ".join(string.split())


def load_json_file(json_file: str) -> dict:
    """
    Load JSON file.
    """
    with open(json_file, encoding="utf-8") as f:
        return json.load(f)
