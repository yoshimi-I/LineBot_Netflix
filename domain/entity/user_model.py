import dataclasses


# ユーザーが持つ値のモデルをvalueobjectとして保持
@dataclasses.dataclass
class User:
    id: str
    content_type: str
    genre: str
    providers: str
    choice_num: int
    start_year: int
    end_year: int
    ques_id: int

