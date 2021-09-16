import re
from loguru import logger
from typing import List, Dict
import requests
from botrequests.settings import RAPID_API
import json

HEADERS = {
    'x-rapidapi-key': RAPID_API,
    'x-rapidapi-host': 'hotels4.p.rapidapi.com'

}


def get_location_search(city) -> List:
    """
        Get location search
        :return: json
        """
    url = 'https://hotels4.p.rapidapi.com/locations/search'
    params = {"query": city}
    try:
        response = requests.request("GET", url, headers=HEADERS, params=params)
        suggestions = json.loads(response.text)['suggestions']
        return suggestions
    except (ConnectionError, KeyError):
        logger.debug('Connection error! Please, try again later!')


def destination_id(city) -> Dict:
    """
        Find destination id
        :param city:
        :param suggestions:
        :return: dict
        """
    destination = dict()
    suggestion = get_location_search(city)
    try:
        for i_sug in suggestion:
            if i_sug.get('group') == 'CITY_GROUP':
                suggestion = i_sug['entities']
                break

        for i_city in suggestion:
            city_name = i_city.get('name')
            if i_city.get('type') == 'CITY' or city_name.startswith(city):
                full_name_city = re.sub(r'<.+?>', '', i_city.get('caption'))
                destination[full_name_city] = i_city.get('destinationId')
        return destination
    except TypeError:
        logger.debug('TypeError! Please, try again later!')


