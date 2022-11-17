from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, PostbackAction, MessageAction,
)
from tinydb import TinyDB, Query

app = Flask(__name__)


handler = WebhookHandler(LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# ここからTinyDBの処理
db = TinyDB("db/user_items.json")
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


# ここから実装開始

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    text = event.message.text
    user_id = event.source.user_id


    if text == "探す" or text == "初めからやり直す":
        db.remove(query.id == user_id)
        db.insert({"id": user_id, "content_type": None, "genre": None, "providers": None, "review_score": None,"ques_id": 1})
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='作品の種類を選んでください',
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=MessageAction(label="映画", text="映画")),
                                QuickReplyButton(action=MessageAction(label="シリーズ", text="シリーズ")),
                                ])
                            )
        )
    elif db.search(query.id == user_id)[0]["ques_id"] == 1:
        mes = event.message.text
        if mes == "映画":
            content_type = "movie"
        else:
            content_type = "show"

        # まずはデータベースをアップデートする,そして受け取った値を保持する必要がある
        db.update({"content_type":content_type ,"ques_id": 2},query.id == user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='作品のジャンルを選んでください',
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=MessageAction(label="アクション", text="アクション")),
                                QuickReplyButton(action=MessageAction(label="アニメーション", text="アニメーション")),
                            ])
                            )
        )
    elif db.search(query.id == user_id)[0]["ques_id"] == 2:

        # 受け取る値は1つまえの選択肢となる
        mes = event.message.text
        if mes == "アクション":
            genre = "act"
        elif mes == "アニメーション":
            genre = "ani"
        db.update({"genre": genre, "ques_id": 3}, query.id == user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='評価を選んでください',
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=MessageAction(label="星4以上", text="星4以上")),
                                QuickReplyButton(action=MessageAction(label="星3.5以上", text="星3.5以上")),
                                QuickReplyButton(action=MessageAction(label="星3以上", text="星3以上")),
                                QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),
                            ])
                            )
        )

    elif db.search(query.id == user_id)[0]["ques_id"] == 3:
        mes = event.message.text
        if mes == "星4以上":
            score = 8
        elif mes == "星3.5以上":
            score = 7
        elif mes == "星3以上":
            score = 6
        else:
            sore = 0
        db.update({"review_score": score, "ques_id": 4}, query.id == user_id)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='検索を開始してよろしいですか？',
                            quick_reply=QuickReply(items=[
                                QuickReplyButton(action=MessageAction(label="大丈夫", text="大丈夫")),
                                QuickReplyButton(action=MessageAction(label="初めからやり直す", text="初めからやり直す")),
                            ])
                            )
        )
    elif db.search(query.id == user_id)[0]["ques_id"] == 4:
    # 以下にAPIを呼び出す処理を記載
        exit()

    else:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage("「探す」と入力することで映画の検索を開始します。")
        )

if __name__ == "__main__":
    app.run()