import json
import datetime
from re import match
from typing import List, Generator
import requests
from loguru import logger
from botrequests.settings import RAPID_API
from botrequests.search_location import destination_id


class RapidApi:
    def __init__(self, city: str, count: str) -> None:
        self._headers = {
            'x-rapidapi-key': RAPID_API,
            'x-rapidapi-host': "hotels4.p.rapidapi.com"
        }
        self._city = city
        self._count_hotels = count
        self.destination = dict()
        self.hotels = list()

    @property
    def city(self) -> str:
        return self._city

    @property
    def count_hotels(self) -> str:
        return self._count_hotels

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

    def get_properties_list(self, destination_id, distance=False) -> List:
        """
        Get properties list
        :param distance:
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
                  "sortOrder": "PRICE"
                  }
        if distance is True:
            params.update({"sortOrder": "DISTANCE_FROM_LANDMARK",
                           "landmarkIds": "city center"}
                          )

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
            label = i_hotel.get('landmarks')[0].get('label')
            address = i_hotel.get('address').get('streetAddress')
            photo = i_hotel.get('optimizedThumbUrls').get('srpDesktop')
            self.hotels.append((name, price, float(distance), label, address, photo))
        return self.hotels

    def lower_price(self) -> List:
        """
        Command /lowerprice
        :return: list
        """
        try:
            for i_destination in destination_id(self.city).values():
                properties = self.get_properties_list(i_destination)
                if properties:
                    lower_price = self.find_hotels(properties)
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
            for i_destination in destination_id(self.city).values():
                properties = self.get_properties_list(i_destination)
                if properties:
                    high_price = self.find_hotels(properties)
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
            for i_destination in destination_id(self.city).values():
                properties = self.get_properties_list(i_destination, distance=True)
                if properties:
                    best_deal = self.find_hotels(properties)
                    for i_elem in best_deal:
                        if i_elem[3] == 'City center':
                            best_deal.sort(key=lambda x: (x[2], x[1]))
                            if max_price > i_elem[1] > min_price and max_distance > i_elem[2] > min_distance:
                                best_hotel.append((i_elem[0], i_elem[1], i_elem[2], i_elem[3], i_elem[4], i_elem[5]))
                        else:
                            logger.info("No information found!")
                    return best_hotel

        except AttributeError:
            logger.debug("'NoneType' object has no attribute 'sort'")


def main():
    parser = RapidApi('new york', '20')
    print(parser.lower_price())
    print(parser.high_price())
    print(parser.best_deal(0, 200, 0, 5))


if __name__ == '__main__':
    main()
