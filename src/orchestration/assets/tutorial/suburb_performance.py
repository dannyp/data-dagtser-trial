from dagster import AssetsDefinition, op, graph
from dagster import DynamicOutput, DynamicOut
from typing import List

@op(out=DynamicOut())
def postcodes() -> List[DynamicOutput]:
    yield DynamicOutput({ "state" : "SA", "locality": "Felixstow", "postcode": "5070" }, mapping_key="1")
    yield DynamicOutput({ "state" : "SA", "locality": "Burnside", "postcode": "5066" }, mapping_key="2")
    yield DynamicOutput({ "state" : "SA", "locality": "Norwood", "postcode": "5067" }, mapping_key="3")

@op(
    required_resource_keys=['domain_api']
)
def lookup_postcode_in_domain(context, location) -> dict:
    """
    Grab Postcode information from the Domain.com.au API
    """
    state, locality, postcode = location['state'], location['locality'], location['postcode']
    return context.resources.domain_api.fetch_location_performance(state,locality,postcode)

@op()
def fan_in(results):
    return (results)

@graph(
    name="extract_postcodes_domain",
    description="Extracts location performance data for selected postcodes from the Domain API.",
)
def suburb_performance():
    locations = postcodes()
    results = locations.map(lookup_postcode_in_domain)
    return fan_in(results.collect())

suburb_performance_asset = AssetsDefinition.from_graph(suburb_performance)

if __name__ == "__main__":
    suburb_performance().execute_in_process()

# @asset()
# def postcodes() -> list:
#     url = "https://raw.githubusercontent.com/matthewproctor/australianpostcodes/master/australian_postcodes.json"
#     response = requests.get(url)
#     if response.ok:
#         return response.json()
#     else:
#         raise ValueError("Error getting list of postcodes")

# #context.domain_api.fetch_location_performance(data['state'], data['suburb'], data['postcode'])