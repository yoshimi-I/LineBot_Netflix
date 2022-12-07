import dataclasses

from domain.value_object.choice_num import ChoiceNum
from domain.value_object.content_type import ContentType
from domain.value_object.end_year import EndYear
from domain.value_object.genre import Genre
from domain.value_object.providers import Providers
from domain.value_object.ques_id import QuesNum
from domain.value_object.start_year import StartYear


# ユーザーが持つ値のモデルをvalueobjectとして保持
@dataclasses.dataclass
class User:
    id: str
    content_type: ContentType
    genre: Genre
    providers: Providers
    choice_num: ChoiceNum
    start_year: StartYear
    end_year: EndYear
    ques_num: QuesNum

