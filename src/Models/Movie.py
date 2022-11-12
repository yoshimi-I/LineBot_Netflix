class Movie:
    def __init__(self):
        self.just_watch = None
        self.content_type = None
        self.provider = None
        self.genre = None
        self.num = None
        self.score = None


class MySession:
    def __init__(self):
        self.status_map = dict()

    def register(user_id):
        # ここでidでclassをインスタンス化
        if MySession.get_status(user_id) is None:
            MySession.put_status(user_id, Movie())

    def reset(user_id):
        MySession.put_status(user_id, Movie())

    def get_status(user_id):
        # keyを指定してvalueを取得
        return MySession.status_map.get(user_id)

    def put_status(user_id, movie):
        MySession.status_map[user_id] = movie


