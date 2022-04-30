# Importing Packages, Prequisites
from service.extracting_books_urls import get_books_urls
from service.scraping_one_book import parse_book_details
from service.writing import save_images, write_to_csv

if __name__ == '__main__':
    base_url = "http://books.toscrape.com/index.html"

    books_urls = []

    books = []
    pagination_url = "http://books.toscrape.com/catalogue/category/books_1/"

    for i in range(1, 5):
        page_url = f"{pagination_url}page-{i}.html"
        books_urls.extend(get_books_urls(page_url))

    for book_url in books_urls:
        print("Extracting from :", book_url)
        books.append(parse_book_details(book_url))

    print("Writing books details to csv file")
    write_to_csv(books, "./output/csv/all_books.csv")
    print("Saving images ...")
    save_images(books)
    print("______________________________________________Finish___________________________________________________")
