# Importing Packages, Prequisites
from service.scraping_one_book import parse_book_details
from service.writing import save_images, write_to_csv
from service.scraping_categories import (
    get_categories_url,
    scrapping_categories_pagination,
)

if __name__ == "__main__":

    # Extracting all the main categories  50 URLs
    categories_url = get_categories_url()
    no_categories = 5
    # For every category URL
    for category_url in categories_url[:no_categories]:
        books = []

        # 1. Getting all the books urls from all the pages
        books_urls = scrapping_categories_pagination(category_url)

        # 2. Using these URLs we extract the book details
        for book_url in books_urls:
            print("Extracting from :", book_url)
            books.append(parse_book_details(book_url))

        # 3. Save the details to CSV file
        write_to_csv(books, f"./output/csv/{books[0]['category']}.csv")

        # 4. Extract all the images of books and save it locally
        save_images(books)
