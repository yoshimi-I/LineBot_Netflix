import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from typing import Dict, List, Tuple


# firebaseの設定ファイルの読み込み
class FirebaseConnect:
    def connect(self):
        if not firebase_admin._apps:
            cred = credentials.Certificate("firebase-admin.json")
            firebase_admin.initialize_app(cred)
