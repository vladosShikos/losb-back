import os

import tomli

with open(os.path.join("pyproject.toml"), mode="rb") as fp:
    pyproject = tomli.load(fp)
PACKAGE_VERSION = pyproject["tool"]["poetry"]["version"]
DOCKER_IMAGE_NAME = pyproject["tool"]["poetry"]["name"]

DOCKER_IMAGE_REGISTRY = (
    "hekata.pro:5000"  # os.environ.get("DOCKER_IMAGE_REGISTRY", "hekata.pro:5000")
)
DOCKER_REGISTRY_USER = os.environ.get("DOCKER_REGISTRY_USER", "")
DOCKER_REGISTRY_PASSWORD = os.environ.get("DOCKER_REGISTRY_PASSWORD", "")
