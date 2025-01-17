from dataclasses import dataclass

from bs4 import BeautifulSoup

import requests


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


def main(output_csv_path: str) -> None:
    r = requests.get("https://quotes.toscrape.com/",)
    bs = BeautifulSoup(r.text, "html.parser")
    bs_quotes = bs.find(".quote")
    print(bs_quotes)


if __name__ == "__main__":
    main("quotes.csv")
