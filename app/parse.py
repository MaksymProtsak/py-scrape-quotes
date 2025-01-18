from dataclasses import dataclass
from urllib.parse import urljoin

from bs4 import BeautifulSoup, Tag

import requests

BASE_URL = "https://quotes.toscrape.com/"


@dataclass
class Quote:
    text: str
    author: str
    tags: list[str]


def create_page_link(base_url: str, next_page_url: str) -> str:
    return urljoin(base_url, next_page_url)


def get_soup_page(url: str) -> BeautifulSoup:
    r = requests.get(url, ).content
    soup = BeautifulSoup(r, "html.parser")
    return soup


def next_page(soup: BeautifulSoup) -> dict:
    next_class = soup.select(".next")
    is_next_page = bool(len(next_class))
    next_page_link = None
    if is_next_page:
        next_page_link = soup.select(".next")[0].a.attrs["href"]
    return {
        "is_next_page": is_next_page,
        "next_page_link": next_page_link,
    }


def get_quotes(soup_page: BeautifulSoup) -> list[Tag]:
    quotes = soup_page.select(".quote")
    return quotes


def pars_single_quote(quote: Tag) -> Quote:
    text = quote.select(".text")[0].contents[0]
    author = quote.select(".author")[0].contents[0]
    tags = [str(tag.contents[0]) for tag in quote.select(".tag")]
    return Quote(text=str(text), author=str(author), tags=list(tags))


def main(output_csv_path: str) -> None:
    page_link = create_page_link(BASE_URL, "")
    bs_page = get_soup_page(page_link)
    is_next_page = next_page(bs_page)
    quotes = get_quotes(bs_page)
    parsed_quotes = []
    while True:
        for quote in quotes:
            parsed_quotes.append(
                pars_single_quote(quote)
            )
        if is_next_page["is_next_page"]:
            page_link = create_page_link(BASE_URL, is_next_page["next_page_link"])
            bs_page = get_soup_page(page_link)
            is_next_page = next_page(bs_page)
            quotes = get_quotes(bs_page)
        else:
            break


if __name__ == "__main__":
    main("quotes.csv")
