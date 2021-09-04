import json
import datetime
from re import match
from typing import List, Generator
from fuzzywuzzy import fuzz as f
import requests
from loguru import logger
from .settings import RAPID_API


class RapidApi:
    def __init__(self, city: str, count: str) -> None:
        self._headers = {
            'x-rapidapi-key': RAPID_API,
            'x-rapidapi-host': "hotels4.p.rapidapi.com"
        }
        self._city = city
        self._count_hotels = count
        self.locale = None
        self.destination = list()
        self.hotels = list()

    @property
    def city(self) -> str:
        return self._city

    @property
    def count_hotels(self) -> str:
        return self._count_hotels

    def get_location_search(self) -> List:
        """
        Get location search
        :return: json
        """
        url = 'https://hotels4.p.rapidapi.com/locations/search'
        params = {"query": self.city, "locale": self.locale}
        try:
            response = requests.request("GET", url, headers=self._headers, params=params)
            suggestions = json.loads(response.text)['suggestions']
            return suggestions
        except (ConnectionError, KeyError):
            logger.debug('Connection error! Please, try again later!')

    def get_locale(self) -> str:
        """
        Get local
        :return: str
        """
        suggestions = self.get_location_search()
        try:
            for i_sug in suggestions:
                if i_sug.get('group') == 'CITY_GROUP':
                    suggestions = i_sug['entities']
                    break
            for i_loc in suggestions:
                caption = (i_loc['caption']).split(',')
                for i_loc in self.get_meta_data():
                    name, locale = i_loc
                    compare = f.WRatio(name, caption[2])
                    if compare > 80:
                        self.locale = locale
            return self.locale
        except TypeError:
            logger.debug('TypeError! Please, try again later!')

    def get_meta_data(self) -> Generator:
        """
        Get meta data
        :return: tuple
        """
        url = "https://hotels4.p.rapidapi.com/get-meta-data"
        try:
            response = requests.request("GET", url, headers=self._headers)
            data = json.loads(response.text)
            locale_tuple = ((i_name['name'], i_name['hcomLocale']) for i_name in data)
            return locale_tuple
        except ConnectionError:
            logger.debug('Connection error! Please, try again later!')

    def get_properties_list(self, destination_id) -> List:
        """
        Get properties list
        :param destination_id:
        :return: dict
        """
        url = 'https://hotels4.p.rapidapi.com/properties/list'
        today = datetime.datetime.today().date()
        tomorrow = today + datetime.timedelta(days=1)
        params = {"adults1": "1",
                  "pageNumber": "1",
                  "destinationId": destination_id,
                  "pageSize": self.count_hotels,
                  "checkOut": str(tomorrow),
                  "checkIn": str(today),
                  "sortOrder": "PRICE",
                  "locale": self.locale
                  }
        try:
            response = requests.request("GET", url, headers=self._headers, params=params)
            data = json.loads(response.text)['data']['body']['searchResults']['results']
            return data
        except (ConnectionError, KeyError):
            logger.debug('Connection error! Please, try again later!')

    def find_hotels(self, properties: List) -> List:
        """
        Find all hotels
        :param properties:
        :return: list
        """
        for i_hotel in properties:
            name = i_hotel['name']
            price = i_hotel['ratePlan']['price']['exactCurrent']
            distance = ''.join(sym for sym in
                               i_hotel.get('landmarks')[0].get('distance')
                               if match(r'[0-9,.]', sym)).replace(',', '.')
            self.hotels.append((name, price, float(distance)))
        return self.hotels

    def destination_id(self, suggestions: List) -> List:
        """
        Find destination id
        :param suggestions:
        :return: list
        """
        try:
            for i_sug in suggestions:
                if i_sug.get('group') == 'CITY_GROUP':
                    suggestions = i_sug['entities']
                    break

            for i_city in suggestions:
                city_name = i_city.get('name')
                if i_city.get('type') == 'CITY' or city_name.startswith(self.city):
                    self.destination.append(i_city.get('destinationId'))
            return self.destination
        except TypeError:
            logger.debug('TypeError! Please, try again later!')

    def find_all_hotels(self) -> List:
        """
        Find all hotels
        :return: list
        """
        sug = self.get_location_search()
        for i_destination in self.destination_id(sug):
            properties = self.get_properties_list(i_destination)
            if properties:
                all_hotels = self.find_hotels(properties)
                return all_hotels

    def lower_price(self) -> List:
        """
        Command /lowerprice
        :return: list
        """
        try:
            lower_price = self.find_all_hotels()
            lower_price.sort(key=lambda x: x[1])
            return lower_price
        except AttributeError:
            logger.debug("'NoneType' object has no attribute 'sort'")

    def high_price(self) -> List:
        """
        Command /highprice
        :return: list
        """
        try:
            high_price = self.find_all_hotels()
            high_price.sort(key=lambda x: x[1], reverse=True)
            return high_price
        except AttributeError:
            logger.debug("'NoneType' object has no attribute 'sort'")

    def best_deal(self, min_price, max_price, min_distance, max_distance) -> List:
        """
        Command /bestdeal
        :return: list
        """
        best_hotel = []
        try:
            best_deal = self.find_all_hotels()
            best_deal.sort(key=lambda x: (x[1], x[2]))
            for i_elem in best_deal:
                if max_price > i_elem[1] > min_price and max_distance > i_elem[2] > min_distance:
                    best_hotel.append(i_elem[0])
            return best_hotel
        except AttributeError:
            logger.debug("'NoneType' object has no attribute 'sort'")


def main():
    parser = RapidApi('new york', '20')
    print(parser.lower_price())
    print(parser.high_price())
    print(parser.best_deal(100, 200, 2, 5))


if __name__ == '__main__':
    main()
