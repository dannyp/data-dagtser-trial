import os
import json

from dagster import load_assets_from_package_module
from dagster._utils import file_relative_path

from . import tutorial

TUTORIAL = "tutorial"

tutorial_assets = load_assets_from_package_module(package_module=tutorial, group_name=TUTORIAL)