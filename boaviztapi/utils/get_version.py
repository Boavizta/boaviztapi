import os
from importlib import metadata

import toml


def get_version_from_pyproject():
    try:
        return metadata.version("boaviztapi")
    except metadata.PackageNotFoundError:
        pass

    potential_paths = [
        os.path.join(os.path.dirname(__file__), "../../pyproject.toml"),
        os.path.join(os.path.dirname(__file__), "../pyproject.toml"),
        os.path.join(os.path.dirname(__file__), "pyproject.toml"),
    ]

    for path in potential_paths:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as file:
                return toml.loads(file.read())["tool"]["poetry"]["version"]

    raise FileNotFoundError("pyproject.toml not found in expected locations")
