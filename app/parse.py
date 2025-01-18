from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag

import requests

BASE_URL = "https://quotes.toscrape.com/"


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


def get_quotes() -> list[Tag]:
    r = requests.get(BASE_URL, ).content
    soup = BeautifulSoup(r, "html.parser")
    quotes = soup.select(".quote")
    return quotes


def pars_single_quote(quote: Tag) -> Quote:
    text = quote.select(".text")[0].contents[0]
    author = quote.select(".author")[0].contents[0]
    tags = [str(tag.contents[0]) for tag in quote.select(".tag")]
    return Quote(text=str(text), author=str(author), tags=list(tags))


def main(output_csv_path: str) -> None:
    quotes = get_quotes()
    parsed_quotes = [
        pars_single_quote(quote)
        for quote in quotes
    ]


if __name__ == "__main__":
    main("quotes.csv")
