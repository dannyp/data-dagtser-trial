import os
import json

from dagster import load_assets_from_package_module, Definitions
from dagster._utils import file_relative_path

from . import tutorial
from ..resources.io_managers.domain_io_manager import domain_api_client

TUTORIAL = "tutorial"

tutorial_assets = load_assets_from_package_module(package_module=tutorial, group_name=TUTORIAL)
