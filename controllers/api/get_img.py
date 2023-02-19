from typing import Dict

from usecase.api.get_img_interface import GetImg
import requests
import json


class GetImgImpl(GetImg):
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
        try:
            description = res["results"][0]["overview"]
        except:
            description = ""
        if len(description) >= 100:
            description = description[:100]
            description += "..."
        elif description == "":
            description = "概要なし"
        return description

    def movies_info_response(self) -> Dict[str, str]:
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
        try:
            description = res["results"][0]["overview"]
        except:
            description = ""
        if len(description) >= 100:
            description = description[:100]
            description += "..."
        elif description == "":
            description = "概要なし"
        return description

    def shows_info_response(self) -> Dict[str, str]:
        real_value = str(round(self.value / 2, 1))
        img_url = self.search_shows_posters(self.title)
        movie_outline = self.search_shows_description(self.title)
        L = {'title': self.title, 'url': self.url, 'value': real_value, 'img_url': img_url,
             'movie_outline': movie_outline}
        return L

    def videos_info(self) -> Dict[str, str]:
        if self.content_type == "movie":
            return self.movies_info_response()
        else:
            return self.shows_info_response()