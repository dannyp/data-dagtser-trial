import os

from dagster import repository, with_resources

from .jobs import tutorial_job
from .assets import tutorial_assets
from .resources import RESOURCES_LOCAL

all_assets = [*tutorial_assets]
all_jobs = [tutorial_job]

@repository
def base_repository():
    definitions = [
        with_resources(all_assets, RESOURCES_LOCAL),
        all_jobs
    ]
    return definitions 