# Importing Packages, Prequisites

import csv
import re
import requests as req
from bs4 import BeautifulSoup as bs
import pandas as pd


# Extracting details from the book page
def parse_book_details(url):
    response = req.get(url)
    soup = bs(response.content, 'html.parser')

    # extracting the title
    title = soup.select_one("h1").string  # select first h1 in the page

    # Extracting the description, the right way
    description = soup.select_one("#content_inner > article > p").string if soup.select_one(
        "#content_inner > article > p") else ""

    # Extracting the category
    breadcrumb = soup.select("ul.breadcrumb > li > a")
    category = breadcrumb[-1].string

    # Extracting the img
    img_url = soup.select_one("#product_gallery img")['src']
    img_url = img_url.replace('../../', 'http://books.toscrape.com/')

    # Extracting the rating, the right way
    rating_class = soup.select_one("p.star-rating")['class']
    rating = rating_class[-1]

    rating_dict = {
        "Zero": 0,
        "One": 1,
        "Two": 2,
        "Three": 3,
        "Four": 4,
        "Five": 5
    }

    rating = rating_dict[rating]

    # Extracting the UPC
    table_info = soup.select("td")

    upc = table_info[0].string
    price_ht = table_info[2].string
    price_ttc = table_info[3].string
    stock = table_info[5].string

    stock = int(re.findall(r"\d+", stock)[0])

    return {
        'product_page_url': url,
        'universal_product_code(upc)': upc,
        'title': title,
        'price_including_tax': price_ttc,
        'price_excluding_tax': price_ht,
        'number_available': stock,
        'product_description': description,
        'category': category,
        'review_rating': rating,
        'image_url': img_url,
    }


def get_books_urls(url):
    response = req.get(url)
    soup = bs(response.content, 'html.parser')

    books_urls_bs = soup.find_all("a", attrs={"title": True})  # all a with a title attribute

    books_urls = []

    for url in books_urls_bs:
        if "../" in url['href']:
            url_cleaned = url['href'].replace("../../", "")
        books_urls.append('http://books.toscrape.com/catalogue/' + url_cleaned)

    return books_urls


def write_to_csv(books_details, csv_filename):
    headers = books_details[0].keys()

    with open(csv_filename, mode="w") as csv_file:
        dict_writer = csv.DictWriter(csv_file, fieldnames=headers)
        dict_writer.writeheader()
        dict_writer.writerows(books_details)


if __name__ == '__main__':
    base_url = "http://books.toscrape.com/index.html"

    books_urls = []

    books = []
    pagination_url = "http://books.toscrape.com/catalogue/category/books_1/"

    for i in range(1, 51):
        page_url = f"{pagination_url}page-{i}.html"
        books_urls.extend(get_books_urls(page_url))

    print(len(books_urls))

    for book_url in books_urls:
        print(book_url)
        books.append(parse_book_details(book_url))

    write_to_csv(books, "all_books.csv")
