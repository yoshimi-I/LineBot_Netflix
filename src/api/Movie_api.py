from justwatch import JustWatch
import random

class Recommend:
    def __init__(self,just_watch,content_type,provider,genre,score):
        self.just_watch = just_watch
        self.content_type = content_type
        self.provider = provider
        self.genre = genre
        self.num = score
        self.score = {
						"imdb:score":
							{
							"min_scoring_value":score,"max_scoring_value":10.0
							}
}
        self.results = just_watch.search_for_item(content_types=[self.content_type],providers=[self.provider],genres=[self.genre],scoring_filter_types=self.score)
        self.page_num = self.results["total_pages"]
        self.items = self.results["items"]

    def recommend(self):
        L = []
        for i in range(self.page_num):
            results2 = self.just_watch.search_for_item(content_types=[self.content_type], providers=[self.provider], genres=[self.genre], scoring_filter_types=self.score, page=i)
            for j in range(len(results2["items"])):
                title = results2["items"][j]["title"]
                L.append(title)
        return L

    def info(self):
        watch_info = dict()
        title_list = self.recommend()
        num = random.sample(range(len(title_list)), 5)
        for i in num:
            # recommendメソッドで作った作品名で検索して出てきたurlを保持
            title_name  = title_list[i]
            title_info = just_watch.search_for_item(query=str(title_name),page=1)
            #urlを取得
            url = title_info["items"][0]["offers"][0]["urls"]["deeplink_web"]
            # 評価を取得
            # なぜだかわからないが順番が毎回バラバラ(多分シーズン毎の評価だと思われる)

            value_list  = title_info["items"][0]["scoring"]
            for j in range(len(value_list)):
                value = value_list[j]["value"]
                if self.num <= value <= 10:
                    watch_info[title_name] = {"url":url,"value":value}
        return watch_info