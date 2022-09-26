import json
from lib2to3.pgen2.pgen import DFAState
from unittest import result
import pandas as pd
import itertools
import requests

from dagster import AssetsDefinition, op, asset, job, graph
from dagster import DynamicOutput, DynamicOut, Output

from ...resources import RESOURCES_LOCAL
from ...utils import postcodes as pc

@asset()
def postcodes() -> list:
    url = "https://raw.githubusercontent.com/matthewproctor/australianpostcodes/master/australian_postcodes.json"
    response = requests.get(url)
    if response.ok:
        return response.json()
    else:
        raise ValueError("Error getting list of postcodes")

#context.domain_client.fetch_location_performance(data['state'], data['suburb'], data['postcode'])

@asset(
    required_resource_keys={"domain_client"},
)
def suburb_performance(context, postcodes):
    results = []
    for p in postcodes[:5]:
        print(p)
        results.append(context.resources.domain_client.fetch_location_performance(p['state'], p['locality'], p['postcode']))
    return results
