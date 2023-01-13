from os import lseek
from time import daylight

from dagster import AssetSelection, define_asset_job, build_schedule_from_partitioned_job

from .assets import TUTORIAL
from .assets import job


tutorial_jobs = [
    define_asset_job(
        "tutorial_job",
        selection=AssetSelection.groups(TUTORIAL),
        tags= {
        }
    ),
    job
]
