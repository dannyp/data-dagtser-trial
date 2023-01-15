from dagster import build_op_context, with_resources, ResourceDefinition

from ....assets.tutorial import suburb_performance
from ....resources import RESOURCES_LOCAL

import pytest

def test_postcodes():
    result = suburb_performance.postcodes()
    assert result is not None

# Provide context for asset
asset = with_resources([suburb_performance.suburb_performance_asset], RESOURCES_LOCAL)[0]

# test singular response
@pytest.mark.skip("Not sure how to run the asset")
def test_suburb_performance_single():
    result = asset(build_op_context(), [{"state": "SA", "locality": "Felixstow", "postcode": "5070"}])
    assert result is not None
    assert len(result) == 1

# test multiple responses
@pytest.mark.skip("Not sure how to run the asset")
def test_suburb_performance_multiple():
    input = [
        {"state": "SA", "locality": "Felixstow", "postcode": "5070"}, 
        {"state": "SA", "locality": "Norwood", "postcode": "5067"}, 
    ]
    result = asset(build_op_context(), input)
    assert len(result) == 2

# test empty response
@pytest.mark.skip("Not sure how to run the asset")
def test_suburb_performance_multiple_one_empty():
    input = [
        {"state": "SA", "locality": "Felixstow", "postcode": "5070"}, 
        {"state": "SA", "locality": "Norwood", "postcode": "5067"}, 
        {"state": "ACT", "locality": "ANU", "postcode": "0200"}, #known to yield empty result 
    ]
    result = asset(build_op_context(), input)
    assert len(result) == 3
    assert result[2]['series'] == []
    
