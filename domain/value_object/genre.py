from typing import Type


class Genre:

    def __init__(self, genre_name: str):
        genre_list = [
            "act", # アクション
            "ani", # アニメーション
            "cmy", # コメディ
            "crm", # 犯罪
            "doc", # ドキュメンタリー
            "scf", # SF
            "fnt", # ファンタジー
            "hst", # 歴史
            "trl", # ホラー、ミステリー
            "fml", # ファミリー
            "msc", # ミュージカル
            "rma", # ロマンス
            "null"
        ]
        if genre_name not in genre_list:
            raise ValueError("genre_name is not collect")
        self.genre_name = genre_name

    def __eq__(self, other):
        return self.genre_name == other.genre_name