from typing import Type


class QuesNum:
    def __init__(self, ques_num: int):
        if ques_num > 7 or ques_num < 1:
            print("ques_id is not collect")
            raise ValueError("ques_id is not collect")
        self.ques_num = ques_num

    def __eq__(self, other):
        return self.ques_num == other.ques_num
