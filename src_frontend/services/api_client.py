import os
import requests
from typing import Optional, Dict, Any


class APIClient:
    def __init__(self, base_url: str, api_key: Optional[str] = None):
        self.base_url = base_url.rstrip('/')
        self.api_key = api_key or os.getenv('API_KEY')
        if not self.api_key:
            raise ValueError("API_KEY must be provided or set in environment variable")

    def _get_headers(self) -> Dict[str, str]:
        return {
            'Content-Type': 'application/json',
            'Authorization': self.api_key,
        }

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.base_url}{endpoint}"
        headers = self._get_headers()
        headers.update(kwargs.pop('headers', {}))

        response = requests.request(method, url, headers=headers, **kwargs)
        try:
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP Error: {response.status_code}")
            print(f"URL: {url}")
            print(f"Headers: {headers}")
            print(f"Response: {response.text}")
            raise
        return response.json()

    def list_vpcs(self) -> Dict[str, Any]:
        return self._request('GET', '/vpcs')

    def create_vpc(self, vpc_name: str, cidr_block: str, region: str) -> Dict[str, Any]:
        return self._request('POST', '/vpcs', json={
            'vpc_name': vpc_name,
            'cidr_block': cidr_block,
            'region': region,
        })

    def get_vpc(self, vpc_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/vpcs/{vpc_id}')

    def update_vpc(self, vpc_id: str, **kwargs) -> Dict[str, Any]:
        return self._request('PUT', f'/vpcs/{vpc_id}', json=kwargs)

    def delete_vpc(self, vpc_id: str) -> Dict[str, Any]:
        return self._request('DELETE', f'/vpcs/{vpc_id}')

    def list_subnets(self) -> Dict[str, Any]:
        return self._request('GET', '/subnets')

    def list_subnets_by_vpc(self, vpc_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/vpcs/{vpc_id}/subnets')

    def create_subnet(self, vpc_id: str, subnet_name: str, cidr_block: str,
                     availability_zone: Optional[str] = None) -> Dict[str, Any]:
        return self._request('POST', f'/vpcs/{vpc_id}/subnets', json={
            'subnet_name': subnet_name,
            'cidr_block': cidr_block,
            'availability_zone': availability_zone,
        })

    def get_subnet(self, subnet_id: str) -> Dict[str, Any]:
        return self._request('GET', f'/subnets/{subnet_id}')

    def update_subnet(self, subnet_id: str, **kwargs) -> Dict[str, Any]:
        return self._request('PUT', f'/subnets/{subnet_id}', json=kwargs)

    def delete_subnet(self, subnet_id: str) -> Dict[str, Any]:
        return self._request('DELETE', f'/subnets/{subnet_id}')
