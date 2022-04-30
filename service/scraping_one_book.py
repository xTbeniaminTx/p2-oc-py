import requests as req
from bs4 import BeautifulSoup as bs
import re


def parse_book_details(url):
    """
    Extracting details from the book page

    :param url: str, Product (Book) URL

    :return: dict, containing single book details
    """
    response = req.get(url)
    soup = bs(response.content, "html.parser")

    # extracting the title
    title = soup.select_one("h1").string  # select first h1 in the page

    # Extracting the description, the right way
    description = (
        soup.select_one("#content_inner > article > p").string
        if soup.select_one("#content_inner > article > p")
        else ""
    )

    # Extracting the category
    breadcrumb = soup.select("ul.breadcrumb > li > a")
    category = breadcrumb[-1].string

    # Extracting the img
    img_url = soup.select_one("#product_gallery img")["src"]
    img_url = img_url.replace("../../", "http://books.toscrape.com/")

    # Extracting the rating, the right way
    rating_class = soup.select_one("p.star-rating")["class"]
    rating = rating_class[-1]

    rating_dict = {"Zero": 0, "One": 1, "Two": 2, "Three": 3, "Four": 4, "Five": 5}

    rating = rating_dict[rating]

    # Extracting the UPC
    table_info = soup.select("td")

    upc = table_info[0].string
    price_ht = table_info[2].string
    price_ttc = table_info[3].string
    stock = table_info[5].string

    stock = int(re.findall(r"\d+", stock)[0])

    return {
        "product_page_url": url,
        "universal_product_code(upc)": upc,
        "title": title,
        "price_including_tax": price_ttc,
        "price_excluding_tax": price_ht,
        "number_available": stock,
        "product_description": description,
        "category": category,
        "review_rating": rating,
        "image_url": img_url,
    }
