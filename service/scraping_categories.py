import requests as req
from bs4 import BeautifulSoup as bs
import re


def get_categories_url():
    """
    Extract all the main categories URLs

    :return: categories_url, List, containg all 50 categories URL
    """
    # Go to Homepage
    base_url = "http://books.toscrape.com/index.html"

    response = req.get(base_url)
    soup = bs(response.content, "html.parser")

    # From the side menu, extact all the categories URL
    base_urls_cat = soup.select(".side_categories > ul > li > ul > li > a")

    categories_url = []

    # Clean the categories URL and save them
    for cat_url in base_urls_cat:
        full_url = "http://books.toscrape.com/" + cat_url["href"]
        categories_url.append(full_url)

    return categories_url


def scrapping_categories_pagination(url):
    """
    Extract all the books' URL from a category page

    :param url: str, Link to a category page

    :return books_urls: list, contains all the books' URL from a category page
    """
    # Go to the category page
    response = req.get(url)
    soup = bs(response.content, "html.parser")

    max_page = 1
    books_urls = []

    # Check if the category has pagination
    if soup.select_one("li.current"):
        # If it does, extract the "Page 1 of n" text
        pages = soup.select_one("li.current").string

        try:
            # Extracting n from  "Page 1 of n" text
            max_page = int(re.findall(r"Page \d+ of (\d+)", pages)[0])

        except IndexError:
            max_page = 1

    # If we have pagination
    if max_page > 1:
        # For all the pages in category, extract the books URL
        for page in range(1, max_page + 1):
            pagination_url = url.replace("index", f"page-{page}")
            print(pagination_url)

            if page != 1:
                response = req.get(pagination_url)
                soup = bs(response.content, "html.parser")

            books_urls_bs = soup.find_all("a", attrs={"title": True})

            for book_url in books_urls_bs:
                book_url_cleaned = "https://books.toscrape.com/catalogue/" + book_url[
                    "href"
                ].replace("../", "")
                books_urls.append(book_url_cleaned)

        return books_urls

    # If there is only 1 page, this code will run instead.
    else:
        books_urls_bs = soup.find_all("a", attrs={"title": True})

        for book_url in books_urls_bs:
            book_url_cleaned = "https://books.toscrape.com/catalogue/" + book_url[
                "href"
            ].replace("../", "")
            books_urls.append(book_url_cleaned)

        return books_urls
