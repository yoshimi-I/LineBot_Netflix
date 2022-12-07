from typing import Type


class ChoiceNum:
    def __init__(self, choice_num: int):
        if choice_num > 3 or choice_num < 0:
            raise ValueError("choice_num is not collect")
        self.choice_num = choice_num

    def __eq__(self, other):
        return self.choice_num == other.choice_num