# interfaceを実装　-> infrastructure/firebase/repository/user_repositoryで実装
import json
from abc import ABC, abstractmethod
from typing import Dict

from domain.entity.user_model import User


class UserRepository(ABC):
    @abstractmethod
    def format_json(self, user_items: User) -> Dict:
        pass

    @abstractmethod
    def create_document(self, user_items: User):
        pass

    @abstractmethod
    def read_document_question_num(self,colum_name:str, user_id: str) -> int:
        pass

    @abstractmethod
    def read_document(self, user_id: str) -> Dict:
        pass

    @abstractmethod
    def update_document(self, colum_name: list, value: list, user_id: str):
        pass

    @abstractmethod
    def delete_document(self, user_id: str):
        pass
