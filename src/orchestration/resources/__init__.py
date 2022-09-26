import os

from dagster import ResourceDefinition
from dagster._utils import file_relative_path

from .duckdb_parquet_io_manager import duckdb_partitioned_parquet_io_manager
from .parquet_io_manager import local_partitioned_io_manager
from .domain_io_manager import domain_api_client

RESOURCES_LOCAL = {
    "parquet_io_manager": duckdb_partitioned_parquet_io_manager.configured({"duckdb_path": "/tmp/domain.duckdb"}),
    "domain_client" : domain_api_client.configured({"client_id": "", "client_secret": ""})
}