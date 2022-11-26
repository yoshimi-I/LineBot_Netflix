class UserItems:
    def __init__(self, db, query, user_id):
        db_items_list = db.search(query.id == user_id)[0]
        self.__content_type = db_items_list["content_type"]
        self.__provider = db_items_list["providers"]
        self.__genre = db_items_list["genre"]
        self.__choice_num = db_items_list["choice_num"]
        self.__start_year = db_items_list["start_year"]
        self.__end_year = db_items_list["end_year"]

    @property
    def content_type(self):
        return self.__content_type

    @property
    def provider(self):
        return self.__provider

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
