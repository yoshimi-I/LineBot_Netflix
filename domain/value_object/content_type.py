from typing import Type

class ContentType:

    def __init__(self, content_name:str):
        content_list = [
            "null",
            "movie",# 映画
            "show" # ドラマ,アニメ
        ]
        if content_name not in content_list:
            raise ValueError("content_name is not collect")
        self.name = content_name

    def __eq__(self, other):
        return self.name == other.name