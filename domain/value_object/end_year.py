from typing import Type


class EndYear:
    def __init__(self, end_year: int):
        if end_year < 2000:
            print("ques_id is not collect")
            raise ValueError("end_year is not collect")
        self.end_year = end_year

    def __eq__(self, other):
        return self.end_year == other.end_year
