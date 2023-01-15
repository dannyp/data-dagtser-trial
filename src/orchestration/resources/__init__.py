import os

from dagster import ResourceDefinition
from dagster._utils import file_relative_path

from .io_managers.duckdb_parquet_io_manager import duckdb_partitioned_parquet_io_manager
from .io_managers.parquet_io_manager import local_partitioned_io_manager
from .io_managers.domain_io_manager import domain_api_client

RESOURCES_LOCAL = {
    "parquet_io_manager": duckdb_partitioned_parquet_io_manager.configured(
        {"duckdb_path": "/tmp/domain.duckdb"}
    ),
    "domain_api": domain_api_client.configured(
        {
            "domain_client_id": {"env": "DOMAIN_CLIENT_ID"},
            "domain_client_secret": {"env": "DOMAIN_CLIENT_SECRET"},
        }
    ),
}
