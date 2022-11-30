import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from typing import Dict, List, Tuple

from src.dto.user_items_dto import UserItemsDTO

# firebaseの設定ファイルの読み込み
cred = credentials.Certificate("firebase-admin.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

class FirebaseCRUD:

    def create_document(self,user_items: UserItemsDTO):
        # もしも過去に存在していた時に削除
        db.collection('user_info').document(user_items.id).delete()
        doc = db.collection('user_info').document(user_items.id)
        doc.set(user_items.format_json())

    def read_document(self,field,user_id: str) -> int:
        doc = db.collection('user_info').document(user_id)
        return doc.get().to_dict()[field]

    def read_all_document(self, user_id: str) -> Dict:
        doc = db.collection('user_info').document(user_id)
        return doc.get().to_dict()

    def update_document(self,field: list,value: list,user_id: str):
        doc = db.collection('user_info').document(user_id)
        for i in range(len(field)):
            field_name = field[i]
            value_name = value[i]
            doc.update({field_name: value_name})

    def delete_document(self,user_id: str):
        doc = db.collection('user_info').document(user_id)
        doc.delete()

