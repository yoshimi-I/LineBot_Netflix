from typing import Type


class StartYear:
    def __init__(self, start_year: int):

        if start_year < 0:
            print("ques_id is not collect")
            raise ValueError("start_year is not collect")
        self.start_year = start_year

    def __eq__(self, other):
        return self.start_year == other.start_year