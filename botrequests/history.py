from datetime import datetime


class History:
    """
    Save history search
    """

    def __init__(self) -> None:
        self.filename = 'history.txt'

    def add_history(self, command: str, date: datetime, hotels: list) -> None:
        """
        :param user_id:
        :param command:
        :param date:
        :param hotels:
        :return:
        """
        with open(self.filename, 'a') as file:
            file.write('{} {} {}\n'.format(command, date, hotels))

    def show_history(self) -> str:
        """
        :return: str
        """
        with open(self.filename, 'r') as file:
            data = file.read()
            return data
