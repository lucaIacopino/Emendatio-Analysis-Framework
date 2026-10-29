"""Configuration loading (see D-21, D-29).

Reads the TOML configuration file and returns it as a nested dictionary:
sections become dictionaries, e.g. config["llm"]["ollama"]["model"].
"""

import tomllib
from pathlib import Path


def load_config(toml_file: str | Path) -> dict:
    """Load a TOML configuration file and return its content as a dict.

    Raises FileNotFoundError if the file does not exist and
    tomllib.TOMLDecodeError if it is not valid TOML.
    """
    with open(toml_file, "rb") as f:
        return tomllib.load(f)