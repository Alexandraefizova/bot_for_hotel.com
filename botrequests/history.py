from datetime import datetime
from typing import List

import dataset


class DB:
    """Search data storage"""
    def __init__(self) -> None:
        self.db = None
        try:
            self.db = dataset.connect('sqlite:///history.sqlite3')
        except Exception:
            raise RuntimeError("db not found")

    def save_inform(self, command: str, date: datetime, hotels: list) -> None:
        """
        Create table and save information
        :param command: str
        :param date: datetime
        :param hotels: hotels
        :return: None
        """
        table = self.db['history']
        for i_row in hotels:
            data = {
                'command': command,
                'date': date,
                'hotel': i_row,
            }
            table.insert(data)

    def get_inform(self) -> List:
        """
        Get information
        :return: list
        """
        rows = []
        for row in self.db['history']:
            rows.append(row)
        return rows

