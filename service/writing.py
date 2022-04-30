import requests as req
from pathlib import Path
import csv


# `save_images()` | A method to save images.
def save_images(books):
    for book in books:
        # specifing the image name
        image_name = book["title"].replace(":", " -").replace("/", " ") + ".jpg"

        # specifing the image path
        image_path = f'./output/images/{book["category"]}/{image_name}'

        # creating the category folder for the image
        Path(f'./output/images/{book["category"]}/').mkdir(parents=True, exist_ok=True)

        # Here, we are downloading the image from the website, books.toscrape.com.
        image_content = req.get(book["image_url"]).content

        # The 'b' in mode is used to specify that the file is a binary.
        # Images are usually stored as binary.
        # That is why we added mode = 'wb', "Write the file as binary"
        with open(image_path, mode="wb") as image_file:
            image_file.write(image_content)


def write_to_csv(books_details, csv_filename):
    headers = books_details[0].keys()

    with open(csv_filename, mode="w") as csv_file:
        dict_writer = csv.DictWriter(csv_file, fieldnames=headers)
        dict_writer.writeheader()
        dict_writer.writerows(books_details)
