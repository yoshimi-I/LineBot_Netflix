import json,os

from flask import Flask, request, abort
from justwatch import JustWatch
from src.api.Movie_api import Recommend, TMDB
from src.responce_format.res import res_format

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, PostbackAction, MessageAction,
    FlexSendMessage, flex_message, BubbleContainer, ImageComponent, URIAction, ImageSendMessage,
)
from tinydb import TinyDB, Query



app = Flask(__name__)

# 環境変数一覧を記載
LINE_CHANNEL_SECRET = os.environ["LINE_CHANNEL_SECRET"]
LINE_CHANNEL_ACCESS_TOKEN = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
API_TOKEN = os.environ["API_TOKEN"]

# Linebotを使えるようにする準備
handler = WebhookHandler(LINE_CHANNEL_SECRET)
line_bot_api = LineBotApi(LINE_CHANNEL_ACCESS_TOKEN)

# ここからTinyDBの処理
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


# ここから実装開始

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event: MessageEvent):
    text = event.message.text
    user_id = event.source.user_id



    if text == "探す" or text == "初めからやり直す":
        try:
            db.remove(query.id == user_id)
            db.insert({"id": user_id, "content_type": None, "genre": None, "providers": None, "review_score": None,"ques_id": 1})
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='動画の視聴方法を選んでください',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="Amazon prime video", text="Amazon prime video")),
                                    QuickReplyButton(action=MessageAction(label="Netflix", text="Netflix")),
                                    QuickReplyButton(action=MessageAction(label="hulu", text="hulu")),
                                    QuickReplyButton(action=MessageAction(label="U-NEXT", text="U-NEXT")),
                                    QuickReplyButton(action=MessageAction(label="Disney+", text="Disney+")),
                                ])
                                )
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='実行に失敗しました,お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="初めからやり直す", text="初めからやり直す")),
                                ])
                                )
            )


    elif db.search(query.id == user_id)[0]["ques_id"] == 1:
        try:
            mes = event.message.text
            # 何かしらの処理で読み込まれなかった時用の保険
            providers = "null"
            if mes == "Amazon prime video":
                providers = "amp"
            elif mes == "Netflix":
                providers = "nfx"
            elif mes == "hulu":
                providers ="hlu"
            elif mes == "U-NEXT":
                providers = "unx"
            elif mes == "Disney+":
                providers = "dnp"
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                TextSendMessage(text='選択肢の中から選んでください',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="Amazon prime video", text="Amazon prime video")),
                                    QuickReplyButton(action=MessageAction(label="Netflix", text="Netflix")),
                                    QuickReplyButton(action=MessageAction(label="hulu", text="hulu")),
                                    QuickReplyButton(action=MessageAction(label="U-NEXT", text="U-NEXT")),
                                    QuickReplyButton(action=MessageAction(label="Disney+", text="Disney+")),
                                ])
                                )
                )

            db.update({"providers": providers, "ques_id": 2}, query.id == user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='作品の種類を選んでください',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="映画", text="映画")),
                                    QuickReplyButton(action=MessageAction(label="アニメ,ドラマ", text="アニメ,ドラマ")),
                                ])
                                )
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='実行に失敗しました,お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="Amazon prime video", text="Amazon prime video")),
                                    QuickReplyButton(action=MessageAction(label="Netflix", text="Netflix")),
                                    QuickReplyButton(action=MessageAction(label="hulu", text="hulu")),
                                    QuickReplyButton(action=MessageAction(label="U-NEXT", text="U-NEXT")),
                                    QuickReplyButton(action=MessageAction(label="Disney+", text="Disney+")),
                                ])
                                )
            )

    elif db.search(query.id == user_id)[0]["ques_id"] == 2:
        try:
            mes = event.message.text
            content_type = "null"
            if mes == "映画":
                content_type = "movie"
            elif mes == "アニメ,ドラマ":
                content_type = "show"
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='選択肢の中から選んでください',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="映画", text="映画")),
                                        QuickReplyButton(action=MessageAction(label="アニメ,ドラマ", text="アニメ,ドラマ")),
                                    ])
                                    )
                )


            # まずはデータベースをアップデートする,そして受け取った値を保持する必要がある
            db.update({"content_type":content_type ,"ques_id": 3},query.id == user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='作品のジャンルを選んでください(右にスクロールできます)',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="アクション", text="アクション")),
                                    QuickReplyButton(action=MessageAction(label="アニメーション", text="アニメーション")),
                                    QuickReplyButton(action=MessageAction(label="コメディ", text="コメディ")),
                                    QuickReplyButton(action=MessageAction(label="犯罪,戦争", text="犯罪,戦争")),
                                    QuickReplyButton(action=MessageAction(label="ドキュメンタリー", text="ドキュメンタリー")),
                                    QuickReplyButton(action=MessageAction(label="ドラマ", text="ドラマ")),
                                    QuickReplyButton(action=MessageAction(label="ファンタジー,SF", text="ファンタジー,SF")),
                                    QuickReplyButton(action=MessageAction(label="歴史", text="歴史")),
                                    QuickReplyButton(action=MessageAction(label="ホラー,ミステリー", text="ホラー,ミステリー")),
                                    QuickReplyButton(action=MessageAction(label="ファミリー", text="ファミリー")),
                                    QuickReplyButton(action=MessageAction(label="ミュージカル", text="ミュージカル")),
                                    QuickReplyButton(action=MessageAction(label="ロマンス", text="ロマンス")),
                                    QuickReplyButton(action=MessageAction(label="スポーツ", text="スポーツ")),

                                ])
                                )
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='実行に失敗しました,お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="映画", text="映画")),
                                    QuickReplyButton(action=MessageAction(label="アニメ,ドラマ", text="アニメ,ドラマ")),
                                ])
                                )
            )

    elif db.search(query.id == user_id)[0]["ques_id"] == 3:
        try:
            # 受け取る値は1つまえの選択肢となる
            mes = event.message.text

            # とりあえず初期化
            genre = "null"

            # 以下受け取った値をもとにDBへ格納する文字列を決める(本当は直接書きたかったけど,文字がバイト形で入るので無理だった)
            if mes == "アクション":
                genre = "act"
            elif mes == "アニメーション":
                genre = "ani"
            elif mes == "コメディ":
                genre = "cmy"
            elif mes == "犯罪,戦争":
                genre = "crm"
            elif mes == "ドキュメンタリー":
                genre = "doc"
            elif mes == "ドラマ":
                genre = "drm"
            elif mes == "ファンタジー,SF":
                genre = "scf"
            elif mes == "歴史":
                genre = "hst"
            elif mes == "ホラー,ミステリー":
                genre = "trl"
            elif mes == "ファミリー":
                genre = "fml"
            elif mes == "ミュージカル":
                genre = "msc"
            elif mes == "ロマンス":
                genre = "rma"
            elif mes == "スポーツ":
                genre = "spt"

            else:
                line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='選択肢の中から選んでください(右にスクロールできます)',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="アクション", text="アクション")),
                                    QuickReplyButton(action=MessageAction(label="アニメーション", text="アニメーション")),
                                    QuickReplyButton(action=MessageAction(label="コメディ", text="コメディ")),
                                    QuickReplyButton(action=MessageAction(label="犯罪,戦争", text="犯罪,戦争")),
                                    QuickReplyButton(action=MessageAction(label="ドキュメンタリー", text="ドキュメンタリー")),
                                    QuickReplyButton(action=MessageAction(label="ドラマ", text="ドラマ")),
                                    QuickReplyButton(action=MessageAction(label="ファンタジー,SF", text="ファンタジー,SF")),
                                    QuickReplyButton(action=MessageAction(label="歴史", text="歴史")),
                                    QuickReplyButton(action=MessageAction(label="ホラー,ミステリー", text="ホラー,ミステリー")),
                                    QuickReplyButton(action=MessageAction(label="ファミリー", text="ファミリー")),
                                    QuickReplyButton(action=MessageAction(label="ミュージカル", text="ミュージカル")),
                                    QuickReplyButton(action=MessageAction(label="ロマンス", text="ロマンス")),
                                    QuickReplyButton(action=MessageAction(label="スポーツ", text="スポーツ")),

                                ])
                                )
                )


            db.update({"genre": genre, "ques_id": 4}, query.id == user_id)
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
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='実行に失敗しました,お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="アクション", text="アクション")),
                                    QuickReplyButton(action=MessageAction(label="アニメーション", text="アニメーション")),
                                    QuickReplyButton(action=MessageAction(label="コメディ", text="コメディ")),
                                    QuickReplyButton(action=MessageAction(label="犯罪,戦争", text="犯罪,戦争")),
                                    QuickReplyButton(action=MessageAction(label="ドキュメンタリー", text="ドキュメンタリー")),
                                    QuickReplyButton(action=MessageAction(label="ドラマ", text="ドラマ")),
                                    QuickReplyButton(action=MessageAction(label="ファンタジー,SF", text="ファンタジー,SF")),
                                    QuickReplyButton(action=MessageAction(label="歴史", text="歴史")),
                                    QuickReplyButton(action=MessageAction(label="ホラー,ミステリー", text="ホラー,ミステリー")),
                                    QuickReplyButton(action=MessageAction(label="ファミリー", text="ファミリー")),
                                    QuickReplyButton(action=MessageAction(label="ミュージカル", text="ミュージカル")),
                                    QuickReplyButton(action=MessageAction(label="ロマンス", text="ロマンス")),
                                    QuickReplyButton(action=MessageAction(label="スポーツ", text="スポーツ")),

                                ])
                                )
            )

    elif db.search(query.id == user_id)[0]["ques_id"] == 4:
        try:
            mes = event.message.text
            if mes == "星4以上":
                score = 8
            elif mes == "星3.5以上":
                score = 7
            elif mes == "星3以上":
                score = 6
            elif mes == "なんでもいい":
                score = 0
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='選択肢の中から選んでください',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="星4以上", text="星4以上")),
                                        QuickReplyButton(action=MessageAction(label="星3.5以上", text="星3.5以上")),
                                        QuickReplyButton(action=MessageAction(label="星3以上", text="星3以上")),
                                        QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),
                                    ])
                                    )
                )

            db.update({"review_score": score, "ques_id": 5}, query.id == user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='検索を開始してよろしいですか？(5秒から10秒ほどかかります)',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="大丈夫", text="大丈夫")),
                                    QuickReplyButton(action=MessageAction(label="初めからやり直す", text="初めからやり直す")),
                                ])
                                )
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='実行に失敗しました,お手数ですがもう一度最初からお願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="星4以上", text="星4以上")),
                                    QuickReplyButton(action=MessageAction(label="星3.5以上", text="星3.5以上")),
                                    QuickReplyButton(action=MessageAction(label="星3以上", text="星3以上")),
                                    QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),
                                ])
                                )
            )


    elif db.search(query.id == user_id)[0]["ques_id"] == 5:
        # 以下にAPIを呼び出す処理を記載
        try:
            just_watch = JustWatch(country='JP')

            # DBからとってきた値を格納
            content_type = db.search(query.id == user_id)[0]["content_type"]
            provider = db.search(query.id == user_id)[0]["providers"]
            genre = db.search(query.id == user_id)[0]["genre"]
            score = db.search(query.id == user_id)[0]["review_score"]

        # インスタンス化を行う

            rec = Recommend(just_watch, content_type, provider, genre, score)
            a = rec.info()
            if len(a) == 0:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='条件に一致する作品が見つかりませんでした',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="初めからやり直す", text="初めからやり直す")),
                                    ])
                                    )
                )

        except:
            line_bot_api.reply_message(
            event.reply_token,
                TextSendMessage(text='実行に失敗しました,お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="初めからやり直す", text="初めからやり直す")),
                                ])
                                )
        )

        # 以下、jsonに書き出す処理
        res = res_format
        for i in range(len(a)):
            try:
                api = TMDB(API_TOKEN, a[i])
                movie_info = api.info()
                res_body = res["contents"][i]
            except:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='実行に失敗しました',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="再実行", text="再実行")),
                                    ])
                                    )
                )

            # タイトルの代入
            res_body["body"]["contents"][0]["text"] = movie_info["title"]

            # 評価を代入
            res_body["body"]["contents"][1]["contents"][-1]["text"] = movie_info["value"]

            # 概要の代入
            res_body["body"]["contents"][2]["contents"][0]["contents"][0]["text"] = movie_info["movie_outline"]

            # imgの代入
            res_body["hero"]["url"] = movie_info["img_url"]

            #
            res_body["footer"]["contents"][0]["action"]["uri"] = movie_info["url"]

        # とりあえずレスポンス

        line_bot_api.reply_message(
            event.reply_token,
            [
                # ここで入力した条件をもとに検索結果を返す
                FlexSendMessage(
                    alt_text='hello',
                    contents=res_format
                ),
                TextSendMessage(text='もう一度探す場合は「探す」と入力してください')
            ]
        )
        db.remove(query.id == user_id)

    else:
        try:
            db.remove(query.id == user_id)
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage("「探す」と入力することで映画の検索を開始します")
            )

if __name__ == "__main__":
    app.run()