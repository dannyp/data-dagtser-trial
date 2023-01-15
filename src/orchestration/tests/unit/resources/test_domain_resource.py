import os

from ....resources.io_managers.domain_io_manager import DomainApiClient  

domain_client_id = os.getenv("DOMAIN_CLIENT_ID")
domain_client_secret = os.getenv("DOMAIN_CLIENT_SECRET")

client = DomainApiClient(domain_client_id, domain_client_secret)

def test_domain_client_not_none():
    print(f"domain_client_id = {domain_client_id}")
    print(f"domain_client_secret = {domain_client_secret}")

    assert client is not None    
    assert domain_client_id is not None    
    assert domain_client_secret is not None    

def test_domain_client_can_authenticate():
    client.authenticate()
    assert client.token is not None

def test_domain_client_can_fetch_location_performance_empty():
    anu_data = client.fetch_location_performance(state="ACT", suburb="ANU", postcode="0200")
    assert anu_data is not None
    assert len(anu_data['series']) == 0
    
def test_domain_client_can_fetch_location():
    data = client.fetch_location_performance(state="SA", suburb="Felixstow", postcode="5070")
    assert data is not None
    assert data['header'] is not None
    assert data['series'] is not None