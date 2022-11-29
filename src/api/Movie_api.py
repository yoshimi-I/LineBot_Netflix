import random
import time

import requests
import json

from justwatch import JustWatch


class Recommend:
    def __init__(self, just_watch: JustWatch, content_type: str, provider: str, genre: str, score: int, start_year: int,
                 end_year: int):
        self.just_watch = just_watch
        self.content_type = content_type
        self.provider = provider
        self.genre = genre
        self.num = score
        self.start_year = start_year
        self.end_year = end_year
        self.score = {
            "imdb:score":
                {
                    "min_scoring_value": score, "max_scoring_value": 10.0
                }
        }
        self.results = self.just_watch.search_for_item(content_types=[self.content_type], providers=[self.provider],
                                                       genres=[self.genre], scoring_filter_types=self.score,
                                                       release_year_from=self.start_year,
                                                       release_year_until=self.end_year)
        self.page_num = self.results["total_pages"]
        self.items = self.results["items"]

    def select_movies(self, num: int, page_num: int) -> list:
        L = []
        movie_list = []
        total_page = page_num
        for i in range(total_page):
            results = self.just_watch.search_for_item(content_types=[self.content_type], providers=[self.provider],
                                                      genres=[self.genre], scoring_filter_types=self.score, page=i,
                                                      release_year_from=self.start_year,
                                                      release_year_until=self.end_year)
            items_num = len(results["items"])
            for j in range(items_num):
                title = results["items"][j]["title"]
                if title not in movie_list:
                    movie_list.append(title)
                if len(movie_list) >= num:
                    break
        return movie_list

    def top_first(self) -> list:
        L = []
        choice_num = 5
        movie_list = self.select_movies(choice_num, 1)
        if len(movie_list) <= choice_num:
            choice_num = len(movie_list)
        for k in range(choice_num):
            L.append(movie_list[k])
        return L

    def top_10(self) -> list:
        L = []
        choice_num = 20
        movie_list = self.select_movies(choice_num, 1)
        output_num = 5
        if len(movie_list) <= 5:
            output_num = len(movie_list)
        num = random.sample(range(len(movie_list)), output_num)
        for k in num:
            L.append(movie_list[k])
        return L

    def top_100(self) -> list:
        L = []
        choice_num = 100
        movie_list = self.select_movies(choice_num, 4)  # 1ページにつき30の作品があることがわかってるので4*30 > 100
        output_num = 5
        if len(movie_list) <= output_num:
            output_num = len(movie_list)
        num = random.sample(range(len(movie_list)), output_num)
        for k in num:
            L.append(movie_list[k])
        return L

    def recommend(self) -> list:
        L = []
        choice_num = 5
        # ページの番号をランダムで取得して,そのページからとってくる(forのネスト回避)
        i = random.randint(0, self.page_num)
        results2 = self.just_watch.search_for_item(content_types=[self.content_type], providers=[self.provider],
                                                   genres=[self.genre], scoring_filter_types=self.score, page=i,
                                                   release_year_from=self.start_year, release_year_until=self.end_year)
        items_num = len(results2["items"])
        if items_num <= choice_num:
            choice_num = items_num
        num = random.sample(range(items_num), choice_num)
        for j in range(items_num):
            if j in num:
                title = results2["items"][j]["title"]
                L.append(title)
        return L

    def info(self, choice_num: int) -> list:
        url = ""
        watch_info = list()
        if choice_num == 0:
            title_list = self.top_first()
        elif choice_num == 1:
            title_list = self.top_10()
        elif choice_num == 2:
            title_list = self.top_100()
        else:
            title_list = self.recommend()
        title_num = len(title_list)
        count = 0
        for title_name in title_list:
            # recommendメソッドで作った作品名で検索して出てきたurlを保持
            title_info = self.just_watch.search_for_item(query=str(title_name), page=0)

            movie_info = title_info["items"][0]["offers"]
            for j in range(len(movie_info)):
                movie_self_info = movie_info[j]
                providers = movie_self_info["package_short_name"]
                if providers == self.provider:
                    url = movie_self_info["urls"]["standard_web"]
                    break

            # 評価を取得
            # なぜだかわからないが順番が毎回バラバラ(多分シーズン毎の評価だと思われる)

            value_list = title_info["items"][0]["scoring"]
            for j in range(len(value_list)):
                value_site = value_list[j]["provider_type"]
                value_num = value_list[j]["value"]
                if value_site == "imdb:score":
                    watch_info.append(
                        {"title": title_name, "url": url, "value": value_num, "content_type": self.content_type})
                    break

        return watch_info


class TMDB:
    def __init__(self, token: str, info: dict):
        self.token = token
        self.headers_ = {'Authorization': f'Bearer {self.token}', 'Content-Type': 'application/json;charset=utf-8'}
        self.base_url_ = 'https://api.themoviedb.org/3/'
        self.img_base_url_ = 'https://image.tmdb.org/t/p/w500'
        self.language = 'ja-JA'
        self.title = info["title"]
        self.content_type = info["content_type"]
        self.value = info["value"]
        self.url = info["url"]

    def _json_by_get_request(self, url: str, params: dict) -> dict:
        res = requests.get(url, headers=self.headers_, params=params)
        return json.loads(res.text)

    def search_movies_posters(self, query: str) -> str:
        params = {'query': query, "language": self.language}
        url = f'{self.base_url_}search/movie'
        res = self._json_by_get_request(url, params)
        try:
            poster_path = res["results"][0]["poster_path"]
            url = self.img_base_url_ + poster_path
        except:
            url = "https://generative-placeholders.glitch.me/image?width=600&height=300&style=cellular-automata&cells=10 "
        return url

    def search_movies_description(self, query: str) -> str:
        params = {'query': query, "language": self.language}
        url = f'{self.base_url_}search/movie'
        res = self._json_by_get_request(url, params)
        description = res["results"][0]["overview"]
        if len(description) >= 100:
            description = description[:100]
            description += "..."
        elif description == "":
            description = "概要なし"
        return description

    def movies_info(self) -> dict:
        real_value = str(round(self.value / 2, 1))
        img_url = self.search_movies_posters(self.title)
        movie_outline = self.search_movies_description(self.title)
        L = {'title': self.title, 'url': self.url, 'value': real_value, 'img_url': img_url,
             'movie_outline': movie_outline}
        return L

    def search_shows_posters(self, query: str) -> str:
        params = {'query': query, "language": self.language}
        url = f'{self.base_url_}search/tv'
        res = self._json_by_get_request(url, params)
        try:
            poster_path = res["results"][0]["poster_path"]
            url = self.img_base_url_ + poster_path
        except:
            url = "https://generative-placeholders.glitch.me/image?width=600&height=300&style=cellular-automata&cells=10"
        return url

    def search_shows_description(self, query: str) -> str:
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

    def shows_info(self) -> dict:
        real_value = str(round(self.value / 2, 1))
        img_url = self.search_shows_posters(self.title)
        movie_outline = self.search_shows_description(self.title)
        L = {'title': self.title, 'url': self.url, 'value': real_value, 'img_url': img_url,
             'movie_outline': movie_outline}
        return L

    def info(self) -> dict:
        if self.content_type == "movie":
            return self.movies_info()
        else:
            return self.shows_info()
