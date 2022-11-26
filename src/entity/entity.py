class UserItemsEntity:
    def __init__(self, db):
        self.__content_type = db["content_type"]
        self.__providers = db["providers"]
        self.__genre = db["genre"]
        self.__choice_num = db["choice_num"]
        self.__start_year = db["start_year"]
        self.__end_year = db["end_year"]

    @property
    def content_type(self):
        return self.__content_type

    @property
    def providers(self):
        return self.__providers

    @property
    def genre(self):
        return self.__genre

    @property
    def choice_num(self):
        return self.__choice_num

    @property
    def start_year(self):
        return self.__start_year

    @property
    def end_year(self):
        return self.__end_year
