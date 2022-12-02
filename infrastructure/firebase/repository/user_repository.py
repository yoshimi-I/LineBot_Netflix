# domainのrepositoryを実装
from typing import Dict

from domain.model.user_model import UserItems
from domain.repository.user_repository_interface import UserRepository
from infrastructure.firebase.database_connect import FirebaseConnect


class UserRepositoryImpl(UserRepository, FirebaseConnect):
    # 継承したFirebaseConnectを用いてFirebaseに接続
    def __init__(self):
        self.db = FirebaseConnect.connect(self)

    # 実装開始
    def format_json(self, user_items: UserItems):
        # firebaseに保存するときにjson形式である必要があるため,そのための処理を実装
        return {
            'id': user_items.id,
            'content_type': user_items.content_type,
            "genre": user_items.genre,
            "providers": user_items.providers,
            "choice_num": user_items.choice_num,
            "start_year": user_items.start_year,
            "end_year": user_items.end_year,
            "ques_id": user_items.ques_id,
        }

    def create_document(self, user_items: UserItems):
        # すでに存在しているテーブルの場合は削除
        self.db.collection('user_info').document(user_items.id).delete()
        doc = self.db.collection('user_info').document(user_items.id)

        # jsonに変換した後DBに保存
        set_user_json = self.format_json(user_items)
        doc.set(set_user_json)

    def read_document_question_num(self, user_id: str, colum_name:str) -> int:
        doc = self.db.collection('user_info').document(user_id)
        return doc.get().to_dict()[colum_name]

    def read_document(self,  user_id: str) -> Dict:
        doc = self.db.collection('user_info').document(user_id)
        return doc.get().to_dict()

    def update_document(self,  user_id: str, colum_name: list, value: list):
        doc = self.db.collection('user_info').document(user_id)
        for i in range(len(colum_name)):
            field_name = colum_name[i]
            value_name = value[i]
            doc.update({field_name: value_name})

    def delete_document(self,  user_id: str, colum_name: str):
        doc = self.db.collection('user_info').document(user_id)
        doc.delete()