from abc import ABC, abstractmethod
from typing import List, Union, Dict


# 主に動画のタイトルをもとに,作品のイメージ画像と説明文を取得する
# interfaceを作成　-> interfaces/api/get_imgで実装
class GetImg(ABC):
    @abstractmethod
    def _json_by_get_request(self, url: str, params: dict) -> dict:
        pass

    @abstractmethod
    def search_movies_posters(self, query: str) -> str:
        pass

    @abstractmethod
    def search_movies_description(self, query: str) -> str:
        pass

    @abstractmethod
    def movies_info_response(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def search_shows_posters(self, query: str) -> str:
        pass

    @abstractmethod
    def search_shows_description(self, query: str) -> str:
        pass

    @abstractmethod
    def shows_info_response(self) -> Dict[str, str]:
        pass

    @abstractmethod
    def videos_info(self) -> Dict[str, str]:
        pass
