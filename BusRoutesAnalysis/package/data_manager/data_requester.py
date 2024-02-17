"""
Module for sending requests to the Warsaw API and returning the response as a dictionary.
"""

import requests
from typing import List


class DataRequester:

    """
    Class sending reqests to the Warsaw API and returning the response as a dictionary.
    
    """
    def __init__(self, api_key : str):
        self.api_key = api_key
        self.path = 'https://api.um.warszawa.pl/api/action'
    
    def send_api_request(self, endpoint, kwargs):
        """
        Send a request to the Warsaw API and return the response as a dictionary.
        """
        url = f'{self.path}/{endpoint}'
        params = {
            'apikey': self.api_key,
            **kwargs
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            print(f'Błąd związany z żądaniem: {e}')
            raise

        return response.json()

    def get_live_locations(self, vehicle_type : str, line_number : str | None = None, brigade : str | None = None) -> List[dict]:
        """
        Return live locations of vehicles from the Warsaw API
        vehicle_type (int): type of vehicle (1 - bus, 2 - tram)
        line_number (int): line number
        brigade (int or str): brigade number
        """
        params = {
            'resource_id': 'f2e5503e-927d-4ad3-9500-4ab9e55deb59',
            'type': vehicle_type,
            'line': line_number,
            'brigade': brigade
        }
        endpoint = 'busestrams_get'
        try:
            result = self.send_api_request(endpoint, params)
        except Exception as e:
            print(f'Error while getting live locations: {e}')
            raise Exception(f'Error while getting live locations: {e}')
        return result['result']
    
    def get_bus_stops(self, name : str = None) -> List[dict]:
        endpoint = 'dbstore_get'
        params = {
            'id': 'ab75c33d-3a26-4342-b36a-6e5fef0a3ac3', 
            'name' : name
        }
        result = self.send_api_request(endpoint, params)
        while not isinstance(result, dict):
            result = self.send_api_request(endpoint, params)
        return result['result']

    def get_lines_for_stop(self, busstopId : str, busstopNR : str) -> List[dict]:
        endpoint = 'dbtimetable_get'
        params = {
            'id' : '88cd555f-6f31-43ca-9de4-66c479ad5942',
            'busstopId' : busstopId,
            'busstopNr' : busstopNR
        }
        try: 
            result = self.send_api_request(endpoint, params)
        except Exception as e:
            print(f'Error while getting lines for stop: {e}')
            raise Exception(f'Error while getting lines for stop: {e}')
        return result['result']
    
    def get_line_schedule(self, line : str, bus_stop_id : str, busstopNR : str) -> List[dict]:
        endpoint = 'dbtimetable_get'
        params = {
            'id' : 'e923fa0e-d96c-43f9-ae6e-60518c9f3238',
            'busstopId' : bus_stop_id,
            'busstopNr' : busstopNR,
            'line' : line

        }
        result = self.send_api_request(endpoint, params)
        while not isinstance(result, dict):
            result = self.send_api_request(endpoint, params)
        return result['result']

    def get_routes(self) -> List[dict]:
        endpoint = 'public_transport_routes'
        result = self.send_api_request(endpoint, {})
        while not isinstance(result, dict):
            result = self.send_api_request(endpoint, {})
        # print(result['result'])
        return result['result']

    