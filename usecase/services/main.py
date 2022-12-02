from abc import ABC, abstractmethod


# interface　-> interfaces/services/main.pyで実装
class MainFunc:
    def handle_main_func(self,event: str, text: str, user_id: str, API_TOKEN: str, line_bot_api: str):
        pass
