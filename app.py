import os

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage
)
from tinydb import TinyDB, Query
from src.services.main import handle_main_func

app = Flask(__name__)

LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")

handler = WebhookHandler(LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)


db = TinyDB("src/db/user_items.json")
query = Query()


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
# ここから実装開始
def handle_message(event: MessageEvent):
    text = event.message.text
    user_id = event.source.user_id
    handle_main_func(event,text,user_id,db,query,API_TOKEN,line_bot_api)

if __name__ == "__main__":
    app.run()