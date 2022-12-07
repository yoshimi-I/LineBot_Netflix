from justwatch import JustWatch
from linebot import LineBotApi
from linebot.models import TextSendMessage, QuickReply, QuickReplyButton, MessageAction, FlexSendMessage

from domain.entity.user_model import User
from domain.value_object.choice_num import ChoiceNum
from domain.value_object.content_type import ContentType
from domain.value_object.end_year import EndYear
from domain.value_object.genre import Genre
from domain.value_object.providers import Providers
from domain.value_object.ques_id import QuesNum
from domain.value_object.start_year import StartYear
from infrastructure.firebase.repository.user_repository import UserRepositoryImpl
from interfaces.api.get_img import GetImgImpl
from interfaces.api.movie_search import MovieSearchImpl
from usecase.dto.user_items_dto import UserItemsDto
from usecase.response.res_1 import res_1_format
from usecase.response.res_2 import res_2_format
from usecase.response.res_3 import res_3_format
from usecase.response.res_4 import res_4_format
from usecase.response.res_5 import res_5_format
from usecase.services.main_interface import MainFunc


class MainFuncImpl(MainFunc):
    def __init__(self):
        self.firebase = UserRepositoryImpl()

    def handle_main_func(self, event: str, text: str, user_id: str, api_token: str, line_bot_api: LineBotApi):
        # firebaseを扱うためにインスタンス化を行う
        try:
            ques_num: int = self.firebase.read_document_question_num("ques_id", user_id)
        except:
            ques_num = 1

        if text == "探す" or text == "初めからやり直す":
            self.first_question_func(event, user_id, line_bot_api)
        elif ques_num == 2:
            self.second_question_func(event, user_id, line_bot_api)
        elif ques_num == 3:
            self.third_question_func(event, user_id, line_bot_api)
        elif ques_num == 4:
            self.fourth_question_func(event, user_id, line_bot_api)
        elif ques_num == 5:
            self.fifth_question_func(event, user_id, line_bot_api)
        elif ques_num == 6:
            self.sixth_question_func(event, user_id, line_bot_api)
        elif ques_num == 7:
            self.final_question_func(event, user_id, api_token, line_bot_api)
        else:
            self.except_func(event, user_id, line_bot_api)

    def first_question_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        try:
            # まずは最初にDBのテーブルを作成
            content_type = ContentType("null")
            genre = Genre("null")
            providers = Providers("null")
            choice_num = ChoiceNum(0)
            start_year = StartYear(0)
            end_year = EndYear(9999)
            ques_num = QuesNum(2)
            user_items = User(user_id, content_type, genre, providers, choice_num, start_year, end_year, ques_num)
            self.firebase.create_document(user_items)
            # 返却する言葉を実装
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='動画の視聴方法を選んでください',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(
                                        action=MessageAction(label="Amazon prime video",
                                                             text="Amazon prime video")),
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
                TextSendMessage(text='実行に失敗しました、お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="初めからやり直す", text="初めからやり直す")),
                                ])
                                )
            )

    def second_question_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        try:
            mes: str = event.message.text
            if mes == "Amazon prime video":
                providers = "amp"
            elif mes == "Netflix":
                providers = "nfx"
            elif mes == "hulu":
                providers = "hlu"
            elif mes == "U-NEXT":
                providers = "unx"
            elif mes == "Disney+":
                providers = "dnp"
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='選択肢の中から選んでください',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="Amazon prime video",
                                                                              text="Amazon prime video")),
                                        QuickReplyButton(action=MessageAction(label="Netflix", text="Netflix")),
                                        QuickReplyButton(action=MessageAction(label="hulu", text="hulu")),
                                        QuickReplyButton(action=MessageAction(label="U-NEXT", text="U-NEXT")),
                                        QuickReplyButton(action=MessageAction(label="Disney+", text="Disney+")),
                                    ])
                                    )
                )
                return

            # ここでDBの値を更新
            self.firebase.update_document(["providers", "ques_id"], [providers, 3], user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='動画の種類を選んでください',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="映画", text="映画")),
                                    QuickReplyButton(action=MessageAction(label="アニメ,ドラマ", text="アニメ,ドラマ")),
                                ])
                                )
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='実行に失敗しました、お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(
                                        action=MessageAction(label="Amazon prime video",
                                                             text="Amazon prime video")),
                                    QuickReplyButton(action=MessageAction(label="Netflix", text="Netflix")),
                                    QuickReplyButton(action=MessageAction(label="hulu", text="hulu")),
                                    QuickReplyButton(action=MessageAction(label="U-NEXT", text="U-NEXT")),
                                    QuickReplyButton(action=MessageAction(label="Disney+", text="Disney+")),
                                ])
                                )
            )

    def third_question_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
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

            # ここでDBの値を更新
            self.firebase.update_document(["content_type", "ques_id"], [content_type, 4], user_id)
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
                TextSendMessage(text='実行に失敗しました、お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="映画", text="映画")),
                                    QuickReplyButton(action=MessageAction(label="アニメ,ドラマ", text="アニメ,ドラマ")),
                                ])
                                )
            )

    def fourth_question_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        try:
            # 受け取る値は1つまえの選択肢となる
            mes = event.message.text

            # 以下受け取った値をもとにDBへ格納する文字列を決める
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

            # ここでDBの値を更新
            self.firebase.update_document(["genre", "ques_id"], [genre, 5], user_id)
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
                TextSendMessage(text='実行に失敗しました、お手数ですがもう一度お願いします',
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

    def fifth_question_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        start_year = 0
        end_year = 9999
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
                end_year = 9999
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

            # ここでDBの値を更新
            self.firebase.update_document(["start_year", "end_year", "ques_id"], [start_year, end_year, 6], user_id)
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='動画の評価を選んでください',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="Top5", text="Top5")),
                                    QuickReplyButton(action=MessageAction(label="Top20の中から", text="Top20の中から")),
                                    QuickReplyButton(action=MessageAction(label="Top100の中から", text="Top100の中から")),
                                    QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),
                                ])
                                )
            )
        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='実行に失敗しました、お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="~2000", text="~2000")),
                                    QuickReplyButton(action=MessageAction(label="2000~2010", text="2000~2010")),
                                    QuickReplyButton(action=MessageAction(label="2010~2020", text="2010~2020")),
                                    QuickReplyButton(action=MessageAction(label="2020~現在", text="2020~現在")),
                                    QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),
                                ])
                                )
            )

    def sixth_question_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        choice_num = 0
        try:
            mes = event.message.text
            if mes == "Top5":
                choice_num = 0
            elif mes == "Top20の中から":
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
                                        QuickReplyButton(action=MessageAction(label="Top5", text="Top5")),
                                        QuickReplyButton(
                                            action=MessageAction(label="Top20の中から", text="Top20の中から")),
                                        QuickReplyButton(
                                            action=MessageAction(label="Top100の中から", text="Top100の中から")),
                                        QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),
                                    ])
                                    )
                )
                return

            # ここでDBに格納
            self.firebase.update_document(["choice_num", "ques_id"], [choice_num, 7], user_id)

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
                TextSendMessage(text='実行に失敗しました、お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="~2000", text="~2000")),
                                    QuickReplyButton(action=MessageAction(label="2000~2010", text="2000~2010")),
                                    QuickReplyButton(action=MessageAction(label="2010~2020", text="2010~2020")),
                                    QuickReplyButton(action=MessageAction(label="2020~現在", text="2020~現在")),
                                    QuickReplyButton(action=MessageAction(label="なんでもいい", text="なんでもいい")),
                                ])
                                )
            )

    def final_question_func(self, event: str, user_id: str, api_token: str, line_bot_api: LineBotApi):
        # 以下にAPIを呼び出す処理を記載
        try:
            mes = event.message.text
            if mes == "大丈夫" or mes == "再実行":
                pass
            else:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='選択肢の中から選んでください',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="大丈夫", text="大丈夫")),
                                        QuickReplyButton(
                                            action=MessageAction(label="初めからやり直す", text="初めからやり直す")),

                                    ])
                                    )
                )
                return

            # インスタンス化を行う(APIとEntity)
            just_watch = JustWatch(country='JP')

            # db_itemsに辞書型で保持する
            db_items = self.firebase.read_document(user_id)

            # entityを用いることで辞書型だったものをメンバ変数のようにして取り出している
            user_items = UserItemsDto(db_items)

            # DBからとってきた値を格納
            content_type = user_items.content_type
            providers = user_items.providers
            genre = user_items.genre
            choice_num = user_items.choice_num
            start_year = user_items.start_year
            end_year = user_items.end_year

            # APIを叩く処理
            rec = MovieSearchImpl(just_watch, content_type, providers, genre, 0, start_year, end_year)
            a = rec.videos_info(choice_num)

            # 受け取った値の数で条件分岐
            if len(a) == 0:
                line_bot_api.reply_message(
                    event.reply_token,
                    TextSendMessage(text='条件に一致する作品が見つかりませんでした',
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(
                                            action=MessageAction(label="初めからやり直す", text="初めからやり直す")),
                                    ])
                                    )
                )
            elif len(a) == 1:
                res = res_1_format
            elif len(a) == 2:
                res = res_2_format
            elif len(a) == 3:
                res = res_3_format
            elif len(a) == 4:
                res = res_4_format
            else:
                res = res_5_format
            # 以下、jsonにとってきた値を代入していく
            for i in range(len(a)):
                api = GetImgImpl(api_token, a[i])
                movie_info = api.videos_info()
                res_body = res["contents"][i]

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

            line_bot_api.reply_message(
                event.reply_token,
                [
                    # ここで入力した条件をもとに検索結果を返す
                    FlexSendMessage(
                        alt_text='hello',
                        contents=res
                    ),
                    TextSendMessage(text="初めから探す場合は「探す」を、条件を変えずに検索をする場合は「再実行」を押してください",
                                    quick_reply=QuickReply(items=[
                                        QuickReplyButton(action=MessageAction(label="探す", text="探す")),
                                        QuickReplyButton(action=MessageAction(label="再実行", text="再実行")),
                                    ])
                                    )
                ]
            )

        except:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text='実行に失敗しました、お手数ですがもう一度お願いします',
                                quick_reply=QuickReply(items=[
                                    QuickReplyButton(action=MessageAction(label="初めからやり直す", text="初めからやり直す")),
                                    QuickReplyButton(action=MessageAction(label="再実行", text="再実行"))
                                ])
                                )
            )

    def except_func(self, event: str, user_id: str, line_bot_api: LineBotApi):
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="「探す」と入力することで映画の検索を開始します")
        )
