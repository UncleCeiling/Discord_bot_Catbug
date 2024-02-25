from typing import Literal

months = range(1, 13)
days = range(1, 32)


class Birthday:
    def __init__(
        self,
        month: int,
        day: int,
        user_id: int,
        years_wished: list[int] = [],
    ):
        self.month = month
        self.day = day
        self.user_id = user_id
        self.month = month
        pass


def import_birthdays():
    """"""
    lines = (open("./files/birthdays.csv", "r").readlines())[0].split(",")
    return lines  #! DO THIS LATER
