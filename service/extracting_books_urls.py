import requests as req
from bs4 import BeautifulSoup as bs


def get_books_urls(url):
    response = req.get(url)
    soup = bs(response.content, 'html.parser')

    # all anchors with a title attribute
    books_urls_bs = soup.find_all("a", attrs={"title": True})

    books_urls_list = []

    for url in books_urls_bs:
        url_cleaned = url['href'].replace("../", "")
        books_urls_list.append('http://books.toscrape.com/catalogue/' + url_cleaned)

    return books_urls_list
