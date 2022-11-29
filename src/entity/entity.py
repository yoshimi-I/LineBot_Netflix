import dataclasses


@dataclasses.dataclass
class UserItemsEntity:
    def __init__(self, user_items):
        self.__content_type: str = user_items["content_type"]
        self.__providers: str = user_items["providers"]
        self.__genre: str = user_items["genre"]
        self.__choice_num: int = user_items["choice_num"]
        self.__start_year: int = user_items["start_year"]
        self.__end_year: int = user_items["end_year"]

    @property
    def content_type(self) -> str:
        return self.__content_type

    @property
    def providers(self) -> str:
        return self.__providers

    @property
    def genre(self) -> str:
        return self.__genre

    @property
    def choice_num(self) -> int:
        return self.__choice_num

    @property
    def start_year(self) -> int:
        return self.__start_year

    @property
    def end_year(self) -> int:
        return self.__end_year
