import dataclasses


@dataclasses.dataclass
class UserItemsDTO:
    id: str
    content_type: str
    genre: str
    providers: str
    choice_num: int
    start_year: int
    end_year: int
    ques_id: int

    def format_json(self):
        return {
            'id': self.id,
            'content_type': self.content_type,
            "genre": self.genre,
            "providers": self.providers,
            "choice_num": self.choice_num,
            "start_year": self.start_year,
            "end_year": self.end_year,
            "ques_id": self.ques_id,
        }
