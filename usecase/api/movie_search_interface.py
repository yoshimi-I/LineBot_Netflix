from abc import ABC, abstractmethod
from typing import List, Union, Dict


# 主に動画のタイトルとurl,作品の評価を取得する
# interfaceを作成　-> controllers/api/movie_searchで実装
class MovieSearch(ABC):
    @abstractmethod
    def select_videos(self, num: int, page_num: int) -> List[str]:
        pass

    @abstractmethod
    def top_5_videos(self) -> List[Union[str, List[str]]]:
        pass

    @abstractmethod
    def top_10_videos(self) -> List[Union[str, List[str]]]:
        pass

    @abstractmethod
    def top_100_videos(self) -> List[Union[str, List[str]]]:
        pass

    @abstractmethod
    def other_videos(self) -> List[Union[str, List[str]]]:
        pass

    @abstractmethod
    def videos_info(self,choice_num: int) -> List[Dict[str, str]]:
        pass
