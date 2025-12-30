import os
import toml


def get_version_from_pyproject():
    # List of potential locations for the pyproject.toml file
    potential_paths = [
        os.path.join(os.path.dirname(__file__), "../../pyproject.toml"),
        os.path.join(os.path.dirname(__file__), "../pyproject.toml"),
        os.path.join(os.path.dirname(__file__), "pyproject.toml"),
    ]

    for path in potential_paths:
        if os.path.exists(path):
            with open(path, "r") as f:
                return toml.loads(f.read())["tool"]["poetry"]["version"]

    # Raise an error if the file is not found in any of the locations
    raise FileNotFoundError("pyproject.toml not found in expected locations")
