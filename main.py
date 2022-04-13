import requests as req
from bs4 import BeautifulSoup as bs

my_url = 'http://books.toscrape.com/catalogue/1000-places-to-see-before-you-die_1/index.html'

def scrapping():
    response = req.get(url=my_url)
    soup = bs(response.content, 'html.parser')

    print(soup)




if __name__ == '__main__':
    scrapping()
