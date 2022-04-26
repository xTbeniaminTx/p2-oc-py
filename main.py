import csv

import requests as req
from bs4 import BeautifulSoup as bs


def one_book_scrapping(url):
    """
    :param url:
    :return:
    """

    # declaration du dictionnaire qui contiendra les infos du livre
    header = [
        'product_page_url',
        'universal_product_code(upc)',
        'title',
        'price_including_tax',
        'price_excluding_tax',
        'number_available',
        'product_description',
        'category',
        'review_rating',
        'image_url',
    ]

    response = req.get(url)


    soup = bs(response.content, 'html.parser')

    titres_bs = soup.find_all("a", attrs="title", class_="product_main")
    print(titres_bs)
    titres = []
    for titre in titres_bs:
        titres.append(titre.string)

    print(titres)

    descriptions_bs = soup.find_all("article.p", class_="product_page")
    descriptions = []
    for desc in descriptions_bs:
        descriptions.append(desc.string)

    # Créer une liste pour les en-têtes
    # header = ["titre", "description"]

    # Créer un nouveau fichier pour écrire dans le fichier appelé « data.csv »
    with open('data.csv', 'w') as fichier_csv:
        # Créer un objet writer (écriture) avec ce fichier
        writer = csv.writer(fichier_csv, delimiter=',')
        writer.writerow(header)
        # Parcourir les titres et descriptions - zip permet d'itérer sur deux listes ou plus à la fois
        # for titre, description in zip(titres, descriptions):
        for i in range(len(titres)):
            # Créer une nouvelle ligne avec le titre et la description à ce moment de la boucle
            ligne = [titres[i], descriptions[i]]
            writer.writerow(ligne)


if __name__ == '__main__':
    product_page_url = 'http://books.toscrape.com/catalogue/category/books/history_32/index.html'
    one_book_scrapping(product_page_url)
