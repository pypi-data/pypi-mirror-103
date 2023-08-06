import json
from typing import Any


def load_text(path: str) -> str:
    """Load file contents into a string

    Args:
    - path: Path to the text file

    Returns: A string containing the file contents
    """
    with open(path, "r") as file:
        return file.read()


def load_json(path: str) -> Any:
    """Load and deserialise a JSON file.

    Args:
    - path: Path to the JSON file

    Returns: A deserialised Python object
    """
    with open(path, "r") as file:
        return json.load(file)
