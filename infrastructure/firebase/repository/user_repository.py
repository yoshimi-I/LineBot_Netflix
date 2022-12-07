# domainのrepositoryを実装
from typing import Dict

from domain.entity.user_model import User
from domain.repository.user_repository_interface import UserRepository
from infrastructure.firebase.database_connect import FirebaseConnect
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

# 継承したFirebaseConnectを用いてFirebaseに接続



class UserRepositoryImpl(UserRepository,FirebaseConnect):
    def __init__(self):
        FirebaseConnect.connect(self)
    def format_json(self, user_items: User):
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

    def create_document(self, user_items: User):
        # すでに存在しているテーブルの場合は削除
        db = firestore.client()
        db.collection('user_info').document(user_items.id).delete()
        doc = db.collection('user_info').document(user_items.id)

        # jsonに変換した後DBに保存
        set_user_json = self.format_json(user_items)
        doc.set(set_user_json)

    def read_document_question_num(self,colum_name:str, user_id: str) -> int:
        db = firestore.client()
        doc = db.collection('user_info').document(user_id)
        return doc.get().to_dict()[colum_name]

    def read_document(self,  user_id: str) -> Dict:
        db = firestore.client()
        doc = db.collection('user_info').document(user_id)
        return doc.get().to_dict()

    def update_document(self, colum_name: list, value: list, user_id: str):
        db = firestore.client()
        doc = db.collection('user_info').document(user_id)
        for i in range(len(colum_name)):
            field_name = colum_name[i]
            value_name = value[i]
            doc.update({field_name: value_name})

    def delete_document(self,user_id: str):
        db = firestore.client()
        doc = db.collection('user_info').document(user_id)
        doc.delete()