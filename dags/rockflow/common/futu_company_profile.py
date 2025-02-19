import json
import os

from bs4 import BeautifulSoup

from rockflow.common.downloader import Downloader


class FutuCompanyProfile(Downloader):
    def __init__(self, symbol: str, futu_ticker: str, prefix: str, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.symbol = symbol
        self.futu_ticker = futu_ticker
        self.prefix = prefix

    @property
    def oss_key(self):
        return os.path.join(
            f"{self.prefix}_{self.snakecase_class_name}",
            f"{self.symbol}.{self.type}"
        )

    @classmethod
    def language(self):
        raise NotImplementedError()

    @property
    def url(self):
        raise NotImplementedError()

    @property
    def type(self):
        return "html"

    @staticmethod
    def extract_data(fp, symbol):
        soup = BeautifulSoup(fp, "lxml", from_encoding="utf-8")
        table_dict = {}
        for row in soup.findAll(name="div", attrs={"class": "company-item"}):
            try:
                name = row.find('div', class_='name').find(text=True).strip()
            except:
                continue
            try:
                value = row.find('div', class_='value').find(text=True).strip()
            except:
                continue
            table_dict[name] = value
        table_dict["symbol"] = symbol
        return table_dict

    def format(self, table_dict):
        raise NotImplementedError()

    def to_json(self, fp):
        raw_table = self.extract_data(fp, self.symbol)
        table_dict = self.format(raw_table)
        print(json.dumps(table_dict, ensure_ascii=False))
        return table_dict


class FutuCompanyProfileEn(FutuCompanyProfile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def language(self):
        return "en"

    @property
    def url(self):
        return f"https://www.futunn.com/{self.language()}/stock/{self.futu_ticker}/company-profile"

    def format(self, table_dict):
        return self.format_(self.language(), table_dict)

    @staticmethod
    def format_(language, table_dict):
        new_table = {}
        new_table["symbol"] = table_dict.get("symbol")
        new_table["language"] = language

        new_table["short_name_a"] = table_dict.get("Short name-A")
        new_table["short_name_h"] = table_dict.get("Short name-H")
        new_table["name" + "_" + language] = table_dict.get("Company Name")
        new_table["profile" + "_" + language] = table_dict.get("Profile")
        new_table["business" + "_" + language] = table_dict.get("Business")
        new_table["exchange"] = table_dict.get("Market") if table_dict.get("Market") else table_dict.get(
            "Listed exchange")
        return new_table


class FutuCompanyProfileCn(FutuCompanyProfile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @classmethod
    def language(self):
        return "cn"

    @property
    def url(self):
        return f"https://www.futunn.com/stock/{self.futu_ticker}/company-profile"

    def format(self, table_dict):
        return self.format_(self.language(), table_dict)

    @staticmethod
    def format_(language, table_dict):
        new_table = {}
        new_table["symbol"] = table_dict.get("symbol")
        new_table["language"] = language

        new_table["short_name_a"] = table_dict.get("A股证券简称")
        new_table["short_name_h"] = table_dict.get("H股证券简称")
        new_table["name" + "_" + language] = table_dict.get("公司名称")
        new_table["profile" + "_" + language] = table_dict.get("公司简介")
        new_table["business" + "_" + language] = table_dict.get("公司业务") if table_dict.get(
            "公司业务") else table_dict.get("公司主营")
        new_table["exchange"] = table_dict.get("所属市场") if table_dict.get(
            "所属市场") else table_dict.get("上市交易所")
        return new_table
