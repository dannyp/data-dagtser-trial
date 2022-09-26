from difflib import restore
from dagster import build_op_context, with_resources

from ....assets.tutorial import suburb_performance
from ....resources.domain_io_manager import domain_api_client

def test_postcodes():
    result = suburb_performance.postcodes()
    assert result is not None

# define api client resource with 
api_client = domain_api_client.configured({"client_id": "", "client_secret": ""})

# Provide context for asset
asset = with_resources([suburb_performance.suburb_performance],{ "domain_client" : api_client})[0]

# test singular response
def test_suburb_performance_single():
    result = asset(build_op_context(), [{"state": "SA", "locality": "Felixstow", "postcode": "5070"}])
    assert result is not None
    assert len(result) == 1

# test multiple responses
def test_suburb_performance_multiple():
    input = [
        {"state": "SA", "locality": "Felixstow", "postcode": "5070"}, 
        {"state": "SA", "locality": "Norwood", "postcode": "5067"}, 
    ]
    result = asset(build_op_context(), input)
    assert len(result) == 2

# test empty response
def test_suburb_performance_multiple_one_empty():
    input = [
        {"state": "SA", "locality": "Felixstow", "postcode": "5070"}, 
        {"state": "SA", "locality": "Norwood", "postcode": "5067"}, 
        {"state": "ACT", "locality": "ANU", "postcode": "0200"}, #known to yield empty result 
    ]
    result = asset(build_op_context(), input)
    assert len(result) == 3
    assert result[2]['series'] == []
    
