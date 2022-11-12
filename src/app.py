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

app = Flask(__name__)


handler = WebhookHandler(LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)




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



    if MySession.read_context(user_id) == "0":
        if text == "探す":
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='作品の種類を選んでください',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="映画", text="映画")),
                                    QuickReplyButton(action=MessageAction(label="その他", text="その他")),
                                ])
                                )
            )


if __name__ == "__main__":
    app.run()
