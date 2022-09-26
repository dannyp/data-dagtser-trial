from ast import Return
import json
from textwrap import indent

import requests
from requests.auth import HTTPBasicAuth
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry  # type: ignore -- nfi why this complains but it still worksq
 
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from dagster import resource
from dagster._utils import file_relative_path

LocationPerformanceRecord = Dict[str, any]
BASE_URL = "https://api.domain.com.au/v2"
AUTH_BASE_URL = "https://auth.domain.com.au/v1/connect/token"

class DomainClient(ABC):
    @abstractmethod
    def fetch_location(self) -> str:
        pass

    @abstractmethod
    def fetch_location_performance(self, state, suburb) -> LocationPerformanceRecord:
        pass

    def authenticate(self):
        pass

class DomainApiClient(DomainClient):
    
    def get_http_client(self) -> HTTPAdapter:
       # configure http client
        retry_strategy = Retry(
            total=3, 
            status_forcelist=[429, 500, 502, 503, 504], 
            allowed_methods=["HEAD", "GET", "OPTIONS"], 
            backoff_factor=1)
        adapter = HTTPAdapter(max_retries=retry_strategy)
        
        http = requests.Session()
        http.mount("http://", adapter=adapter)
        http.mount("https://", adapter=adapter)
        return http

    def __init__(self, client_id, client_secret) -> None:
        self.token = None
        self.client_id = client_id
        self.client_secret = client_secret
        self.http = self.get_http_client()
      
    def save_token(self, token):
        print(token)
        self.token = token

    def authenticate(self):
        auth = HTTPBasicAuth(self.client_id, self.client_secret)
        data = { 
            "grant_type" : "client_credentials", 
            "scope":"api_suburbperformance_read" 
            }
        r = self.http.post(
            AUTH_BASE_URL, 
            auth = auth, 
            data = data, 
            headers = { "Content-type" : "application/x-www-form-urlencoded" },
            timeout=10
            
        )
        
        if not r.ok:
            r.raise_for_status()
        
        self.save_token(r.json())

    def fetch_location(self) -> str:
        return super().fetch_location()


    def fetch_location_performance(self, state, suburb, postcode) -> Any:
        """
            Fetch the location performance statistics for a suburb from the Domain API
            If the API reuturns an empty payload, return an empty series.
        """
        result = self.call_api(url = f"{BASE_URL}/suburbPerformanceStatistics/{state}/{suburb}/{postcode}")
        if result is None:
            return {'header': {'suburb': suburb, 'state': state, 'propertyCategory': 'House'}, 'series': [] }
        return result

    def call_api(self, url):
        """
            Generically call the domain api (get requests) with authentication applied.
            The default OAuth sessions/handlers didn't seem to work
        """
        print(url)
        if self.token is None:
            self.authenticate()
        r = self.http.get(url=url, headers={"Authorization": f"Bearer {self.token['access_token']}"})
        if not r.ok: 
            r.raise_for_status()
        if len(r.content) == 0:
            return None                 # r.json fails on empty payloads
        return r.json()

@resource(
    description="A domain.com.au http client that fetches results from the rest API",
    config_schema={"client_id" : str, "client_secret": str}
)
def domain_api_client(context):
    return DomainApiClient(context.resource_config["client_id"], context.resource_config["client_secret"])

if __name__ == "__main__":
    c = DomainApiClient(**{"client_id": "", "client_secret": ""})
    c.authenticate()
    print(json.dumps(c.fetch_location_performance("SA", "Felixstow", "5070"), indent=2))