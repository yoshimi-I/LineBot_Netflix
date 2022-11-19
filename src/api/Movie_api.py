import random
import time

import requests
import json


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
        self.results = self.just_watch.search_for_item(content_types=[self.content_type],providers=[self.provider],genres=[self.genre],scoring_filter_types=self.score)
        self.page_num = self.results["total_pages"]
        self.items = self.results["items"]

    def recommend(self):
        L = []
        i = random.randint(0,self.page_num)
        results2 = self.just_watch.search_for_item(content_types=[self.content_type],providers=[self.provider],genres=[self.genre],scoring_filter_types=self.score,page=i)
        for j in range(len(results2["items"])):
            title = results2["items"][j]["title"]
            L.append(title)
        return L

    def info(self):
        watch_info = list()
        title_list = self.recommend()
        title_num = len(title_list)
        num = random.sample(range(title_num), title_num)
        count = 0
        for i in num:
            # recommendメソッドで作った作品名で検索して出てきたurlを保持
            title_name  = title_list[i]
            title_info = self.just_watch.search_for_item(query=str(title_name),page=0)

            movie_info = title_info["items"][0]["offers"]
            for j in range(len(movie_info)):
                movie_self_info = movie_info[j]
                providers = movie_self_info["package_short_name"]
                if providers == self.provider:
                    url = movie_self_info["urls"]["standard_web"]
                    break

            # 評価を取得
            # なぜだかわからないが順番が毎回バラバラ(多分シーズン毎の評価だと思われる)

            value_list  = title_info["items"][0]["scoring"]
            for j in range(len(value_list)):
                value = value_list[j]["value"]
                if self.num <= value <= 10:
                    watch_info.append({"title":title_name,"url":url,"value":value,"content_type":self.content_type})
                    break
            if len(watch_info) == 3:
                break

        return watch_info


class TMDB:
    def __init__(self, token, info):
        self.token = token
        self.headers_ = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json;charset=utf-8'}
        self.base_url_ = 'https://api.themoviedb.org/3/'
        self.img_base_url_ = 'https://image.tmdb.org/t/p/w500'
        self.language = 'ja-JA'
        self.title = info["title"]
        self.content_type = info["content_type"]
        self.value = info["value"]
        self.url = info["url"]

    def _json_by_get_request(self, url, params={}):
        res = requests.get(url, headers=self.headers_, params=params)
        return json.loads(res.text)

    def search_movies_posters(self, query):
        params = {'query': query, "language": self.language}
        url = f'{self.base_url_}search/movie'
        res = self._json_by_get_request(url, params)
        try:
            poster_path = res["results"][0]["poster_path"]
            url = self.img_base_url_ + poster_path
        except:
            url = "https://generative-placeholders.glitch.me/image?width=600&height=300&style=cellular-automata&cells=10 "
        return url

    def search_movies_description(self, query):
        params = {'query': query, "language": self.language}
        url = f'{self.base_url_}search/movie'
        res = self._json_by_get_request(url, params)
        description = res["results"][0]["overview"]
        if len(description) >= 100:
            description = description[:100]
            description+="..."
        elif description == "":
            description = "概要なし"
        return description

    def movies_info(self):
        real_value = str(round(self.value / 2, 1))
        img_url = self.search_movies_posters(self.title)
        movie_outline = self.search_movies_description(self.title)
        L = {'title': self.title, 'url': self.url, 'value': real_value, 'img_url': img_url,
             'movie_outline': movie_outline}
        return L

    def search_shows_posters(self, query):
        params = {'query': query, "language": self.language}
        url = f'{self.base_url_}search/tv'
        res = self._json_by_get_request(url, params)
        try:
            poster_path = res["results"][0]["poster_path"]
            url = self.img_base_url_ + poster_path
        except:
            url = "https://generative-placeholders.glitch.me/image?width=600&height=300&style=cellular-automata&cells=10"
        return url

    def search_shows_description(self, query):
        params = {'query': query, "language": self.language}
        url = f'{self.base_url_}search/tv'
        res = self._json_by_get_request(url, params)
        description = res["results"][0]["overview"]
        if len(description) >= 100:
            description = description[:100]
            description += "..."
        elif description == "":
            description = "概要なし"
        return description

    def shows_info(self):
        real_value = str(round(self.value / 2, 1))
        img_url = self.search_shows_posters(self.title)
        movie_outline = self.search_shows_description(self.title)
        L = {'title': self.title, 'url': self.url, 'value': real_value, 'img_url': img_url,
             'movie_outline': movie_outline}
        return L

    def info(self):
        if self.content_type == "movie":
            return self.movies_info()
        else:
            return self.shows_info()
