from abc import ABC, abstractmethod

from linebot import LineBotApi


# interface　-> controllers/services/main.pyで実装
class MainFunc(ABC):
    @abstractmethod
    def first_question_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        pass

    @abstractmethod
    def second_question_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        pass

    @abstractmethod
    def third_question_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        pass

    @abstractmethod
    def fourth_question_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        pass

    @abstractmethod
    def fifth_question_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        pass

    @abstractmethod
    def sixth_question_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        pass

    @abstractmethod
    def final_question_func(self, event: str, user_id: str, api_token: str, line_bot_api: LineBotApi):
        pass

    @abstractmethod
    def except_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        pass

    @abstractmethod
    def handle_main_func(self, event: str, text: str, user_id: str, api_token: str, line_bot_api: LineBotApi):
        pass
