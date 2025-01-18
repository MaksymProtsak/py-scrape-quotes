from dataclasses import dataclass

from bs4 import BeautifulSoup, Tag

import requests

BASE_URL = "https://quotes.toscrape.com/"


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


def get_soup_page() -> BeautifulSoup:
    r = requests.get(BASE_URL, ).content
    soup = BeautifulSoup(r, "html.parser")
    return soup


def next_page(soup: BeautifulSoup) -> tuple:
    next_class = soup.select(".next")
    is_next_page = bool(len(next_class))
    next_page_link = None
    if is_next_page:
        next_page_link = soup.select(".next")[0].a.attrs["href"]
    return is_next_page, next_page_link


def get_quotes(soup_page: BeautifulSoup) -> list[Tag]:
    quotes = soup_page.select(".quote")
    return quotes


def pars_single_quote(quote: Tag) -> Quote:
    text = quote.select(".text")[0].contents[0]
    author = quote.select(".author")[0].contents[0]
    tags = [str(tag.contents[0]) for tag in quote.select(".tag")]
    return Quote(text=str(text), author=str(author), tags=list(tags))


def main(output_csv_path: str) -> None:
    bs_page = get_soup_page()
    is_next_page = next_page(bs_page)
    quotes = get_quotes(bs_page)
    parsed_quotes = [
        pars_single_quote(quote)
        for quote in quotes
    ]


if __name__ == "__main__":
    main("quotes.csv")
