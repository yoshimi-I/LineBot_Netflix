from typing import Type


class Providers:
    def __init__(self, provider_name: str):
        providers_list = [
            "amp", # アマプラ
            "nfx", # ネトフリ
            "hlu", # Hulu
            "unx", # U-NEXT
            "dnp", # ディズニープラス
            "null"

        ]
        if provider_name not in providers_list:
            raise ValueError("provider_name is not collect")
        self.provider_name = provider_name

    def __eq__(self, other):
        return self.provider_name == other.provider_name