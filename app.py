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
LINE_CHANNEL_SECRET = os.getenv("LINE_CHANNEL_SECRET")
LINE_CHANNEL_ACCESS_TOKEN = os.getenv("LINE_CHANNEL_ACCESS_TOKEN")
API_TOKEN = os.getenv("API_TOKEN")

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
            db.insert({"id": user_id, "content_type": None, "genre": None, "providers": None,"choice_num" : None,"start_year": None,"end_year": None,"ques_id": 1})
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
                return

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
                return


            # まずはデータベースをアップデートする,そして受け取った値を保持する必要がある
            db.update({"content_type":content_type ,"ques_id": 3},query.id == user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='動画のジャンルを選んでください(右にスクロールできます)',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="アクション", text="アクション")),
                                    QuickReplyButton(action=MessageAction(label="アニメーション", text="アニメーション")),
                                    QuickReplyButton(action=MessageAction(label="コメディ", text="コメディ")),
                                    QuickReplyButton(action=MessageAction(label="犯罪,戦争", text="犯罪,戦争")),
                                    QuickReplyButton(action=MessageAction(label="ドキュメンタリー", text="ドキュメンタリー")),
                                    QuickReplyButton(action=MessageAction(label="SF", text="SF")),
                                    QuickReplyButton(action=MessageAction(label="ファンタジー", text="ファンタジー")),
                                    QuickReplyButton(action=MessageAction(label="歴史", text="歴史")),
                                    QuickReplyButton(action=MessageAction(label="ホラー,ミステリー", text="ホラー,ミステリー")),
                                    QuickReplyButton(action=MessageAction(label="ファミリー", text="ファミリー")),
                                    QuickReplyButton(action=MessageAction(label="ミュージカル", text="ミュージカル")),
                                    QuickReplyButton(action=MessageAction(label="ロマンス", text="ロマンス")),
                                    QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),

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
            elif mes == "SF":
                genre = "scf"
            elif mes == "ファンタジー":
                genre = "fnt"
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
            elif mes == "なんでもいい":
                genre = "null"

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
                                    QuickReplyButton(action=MessageAction(label="SF", text="SF")),
                                    QuickReplyButton(action=MessageAction(label="ファンタジー", text="ファンタジー")),
                                    QuickReplyButton(action=MessageAction(label="歴史", text="歴史")),
                                    QuickReplyButton(action=MessageAction(label="ホラー,ミステリー", text="ホラー,ミステリー")),
                                    QuickReplyButton(action=MessageAction(label="ファミリー", text="ファミリー")),
                                    QuickReplyButton(action=MessageAction(label="ミュージカル", text="ミュージカル")),
                                    QuickReplyButton(action=MessageAction(label="ロマンス", text="ロマンス")),
                                    QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),

                                ])
                                )
                )
                return


            db.update({"genre": genre, "ques_id": 4}, query.id == user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='動画の放送時期を選んでください',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="~2000", text="~2000")),
                                    QuickReplyButton(action=MessageAction(label="2000~2010", text="2000~2010")),
                                    QuickReplyButton(action=MessageAction(label="2010~2020", text="2010~2020")),
                                    QuickReplyButton(action=MessageAction(label="2020~現在", text="2020~現在")),
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
                                    QuickReplyButton(action=MessageAction(label="SF", text="SF")),
                                    QuickReplyButton(action=MessageAction(label="ファンタジー", text="ファンタジー")),
                                    QuickReplyButton(action=MessageAction(label="歴史", text="歴史")),
                                    QuickReplyButton(action=MessageAction(label="ホラー,ミステリー", text="ホラー,ミステリー")),
                                    QuickReplyButton(action=MessageAction(label="ファミリー", text="ファミリー")),
                                    QuickReplyButton(action=MessageAction(label="ミュージカル", text="ミュージカル")),
                                    QuickReplyButton(action=MessageAction(label="ロマンス", text="ロマンス")),
                                    QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),

                                ])
                                )
            )

    elif db.search(query.id == user_id)[0]["ques_id"] == 4:
        start_year = 0
        end_year = 999999
        try:
            mes = event.message.text
            if mes == "~2000":
                end_year = 2000
            elif mes == "2000~2010":
                start_year = 2000
                end_year = 2010
            elif mes == "2010~2020":
                start_year = 2010
                end_year = 2020
            elif mes == "2020~現在":
                start_year = 2020
            elif mes == "なんでもいい":
                start_year = 0
                end_year = 999999
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='選択肢の中から選んでください',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="~2000", text="~2000")),
                                        QuickReplyButton(action=MessageAction(label="2000~2010", text="2000~2010")),
                                        QuickReplyButton(action=MessageAction(label="2010~2020", text="2010~2020")),
                                        QuickReplyButton(action=MessageAction(label="2020~現在", text="2020~現在")),
                                        QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),
                                    ])
                                    )
                )
                return


            db.update({"start_year": start_year, "end_year": end_year, "ques_id": 5}, query.id == user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='動画の評価を選んでください',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="Top3", text="Top3")),
                                    QuickReplyButton(action=MessageAction(label="Top10の中から", text="Top10の中から")),
                                    QuickReplyButton(action=MessageAction(label="Top100の中から", text="Top100の中から")),
                                    QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),
                                ])
                                )
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='実行に失敗しました,お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="~2000", text="~2000")),
                                    QuickReplyButton(action=MessageAction(label="2000~2010", text="2000~2010")),
                                    QuickReplyButton(action=MessageAction(label="2010~2020", text="2010~2020")),
                                    QuickReplyButton(action=MessageAction(label="2020~現在", text="2020~現在")),
                                    QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),
                                ])
                                )
            )
    elif db.search(query.id == user_id)[0]["ques_id"] == 5:
        choice_num = 0
        try:
            mes = event.message.text
            if mes == "Top3":
                choice_num = 0
            elif mes == "Top10の中から":
                choice_num = 1
            elif mes == "Top100の中から":
                choice_num = 2
            elif mes == "なんでもいい":
                choice_num = 3
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='選択肢の中から選んでください',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="Top3", text="Top3")),
                                        QuickReplyButton(action=MessageAction(label="Top10の中から", text="Top10の中から")),
                                        QuickReplyButton(action=MessageAction(label="Top100の中から", text="Top100の中から")),
                                        QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),
                                    ])
                                    )
                )
                return

            # ここでDBに格納
            db.update({"choice_num": choice_num, "ques_id": 6}, query.id == user_id)

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
                TextSendMessage(text='実行に失敗しました,お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="~2000", text="~2000")),
                                    QuickReplyButton(action=MessageAction(label="2000~2010", text="2000~2010")),
                                    QuickReplyButton(action=MessageAction(label="2010~2020", text="2010~2020")),
                                    QuickReplyButton(action=MessageAction(label="2020~現在", text="2020~現在")),
                                    QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),
                                ])
                                )
            )


    elif db.search(query.id == user_id)[0]["ques_id"] == 6:

        # 以下にAPIを呼び出す処理を記載
        try:
            mes = event.message.text
            if mes == "大丈夫":
                pass
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='選択肢の中から選んでください',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="大丈夫", text="大丈夫")),
                                        QuickReplyButton(action=MessageAction(label="初めからやり直す", text="初めからやり直す")),

                                    ])
                                    )
                )
                return

            # インスタンス化を行う
            just_watch = JustWatch(country='JP')

            # DBからとってきた値を格納
            content_type = db.search(query.id == user_id)[0]["content_type"]
            provider = db.search(query.id == user_id)[0]["providers"]
            genre = db.search(query.id == user_id)[0]["genre"]
            choice_num = db.search(query.id == user_id)[0]["choice_num"]
            start_year = db.search(query.id == user_id)[0]["start_year"]
            end_year = db.search(query.id == user_id)[0]["end_year"]
            rec = Recommend(just_watch, content_type, provider, genre,0,start_year,end_year)
            print(content_type, provider, genre,start_year,end_year)
            a = rec.info(choice_num)
            if len(a) == 0:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='条件に一致する作品が見つかりませんでした',
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


        except:
                line_bot_api.reply_message(
                event.reply_token,
                    TextSendMessage(text='実行に失敗しました,お手数ですがもう一度お願いします',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="初めからやり直す", text="初めからやり直す")),
                                    ])
                                    )
            )

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