from dagster import AssetsDefinition, op, graph
from dagster import DynamicOutput, DynamicOut
from typing import List

@op(out=DynamicOut())
def postcodes() -> List[DynamicOutput]:
    yield DynamicOutput({ "state" : "SA", "locality": "Felixstow", "postcode": "5070" }, mapping_key="1")
    yield DynamicOutput({ "state" : "SA", "locality": "Burnside", "postcode": "5066" }, mapping_key="2")
    yield DynamicOutput({ "state" : "SA", "locality": "Norwood", "postcode": "5067" }, mapping_key="3")

@op()
def lookup_postcode_in_domain(context, location) -> dict:
    """
    Grab Postcode information from the Domain.com.au API
    """
    state, locality, postcode = location['state'], location['locality'], location['postcode']
    return dict(state=state, locality=locality, postcode)
    #return context.resources.domain_client.fetch_location_performance(state,locality,postcode)

@op()
def fan_in(results):
    return (results)

@graph()
def run():
    locations = postcodes()
    results = locations.map(lookup_postcode_in_domain)
    return fan_in(results.collect())

graph_asset = AssetsDefinition.from_graph(run)

if __name__ == "__main__":
    run().execute_in_process()

# @asset()
# def postcodes() -> list:
#     url = "https://raw.githubusercontent.com/matthewproctor/australianpostcodes/master/australian_postcodes.json"
#     response = requests.get(url)
#     if response.ok:
#         return response.json()
#     else:
#         raise ValueError("Error getting list of postcodes")

# #context.domain_client.fetch_location_performance(data['state'], data['suburb'], data['postcode'])

# @asset(
#     required_resource_keys={"domain_client"},
# )
# def suburb_performance(context, postcodes):
#     results = []
#     for p in postcodes[:5]:
#         print(p)
#         results.append(context.resources.domain_client.fetch_location_performance(p['state'], p['locality'], p['postcode']))
#     return results

