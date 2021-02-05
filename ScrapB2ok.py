# Libraries:
import sys
import os
import csv
import time

import bs4
import requests


class AllLinks:
    """

    """
    WEBMASTER = "http://books.toscrape.com/catalogue/"
    WEBSITE = "http://books.toscrape.com/catalogue/category/books_1/index.html"

    def __init__(self):
        """

        """
        self.url_page = AllLinks.WEBSITE
        self.webmaster = AllLinks.WEBMASTER
        self.link_pages = []
        self.next = None
        self.next_page = None
        self.html_root = ""
        self.html_page = ""
        self.soup_pages = ""

        self.link = ""
        self.links = []
        self.fullLink = ""
        self.articles = ""
        self.soup_books = ""

        self.all_pages = []
        self.all_books_links = []

        self.link_book = ""

        self.get_all_pages_links()
        self.scrap_books_links()
        pass

    def get_page_links(self):
        """

        """
        self.url_page = self.url_page.replace('index.html', '')
        self.link_pages = ['index.html']

        self.html_root = requests.get(self.url_page + self.link_pages[0])
        self.soup_pages = bs4.BeautifulSoup(self.html_root.text, 'html.parser')

        self.next = None
        self.next_page = self.soup_pages.find('li', {'class': 'next'})

        if self.next_page is not None:
            self.next = (str(self.next_page.a).split('">')[0][9:])

        while self.next is not None:
            self.link_pages.append(self.next)
            self.html_root = requests.get(self.url_page + self.next)
            self.soup_pages = bs4.BeautifulSoup(self.html_root.text, 'html.parser')

            self.next_page = self.soup_pages.find('li', {'class': 'next'})

            if self.next_page is not None:
                self.next = (str(self.next_page.a).split('">')[0][9:])
            else:
                self.next = None

        return self.link_pages

    def get_all_pages_links(self):
        """

        """

        self.all_pages = self.get_page_links()
        self.all_books_links = []

        for i in range(len(self.all_pages)):
            self.link_book = f'{self.url_page + self.all_pages[i]}'
            self.all_books_links.append(self.link_book)

        return self.all_books_links

    def get_books_links_per_page(self, link_page):

        self.html_page = requests.get(link_page)
        self.soup_books = bs4.BeautifulSoup(self.html_page.text, 'html.parser')

        self.articles = self.soup_books.findAll('article', {'class': "product_pod"})

        for article in self.articles:
            self.link = str(article.find('h3').a)
            self.link = self.link.split(" title")[0][15:-1]
            self.link = self.link.replace('catalogue/', '')

            self.fullLink = f'{self.webmaster + self.link}'

            self.links.append(self.fullLink)
        pass

    def scrap_books_links(self):
        for link_page in self.all_books_links:
            self.get_books_links_per_page(link_page)
        pass

    def get_links(self):
        return self.links


class Book:

    def __init__(self, url):

        self.dict_stars = {'One': 1, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5}
        self.stars = ""

        self.url = url

        self.response = ""
        self.soup = ""

        self.cells = ""
        self.desc = ""

        self.product_page_url = url
        self.title = ""
        self.universal_product_code = ""
        self.product_description = ""
        self.category = []
        self.price_excluding_tax = ""
        self.price_including_tax = ""
        self.number_available = ""
        self.review_rating = ""
        self.image_url = ""
        self.picture = ""

        self.database = []
        self.scrap_book()
        pass

    def scrap_book(self):
        """
        Core function of this program:
        This function get all the informations needed for each book of the
        website. It return the datas and the category.
        """
        # HTML de la page web

        self.response = requests.get(self.url)

        if self.response.ok:
            # If the server is responding :
            self.soup = bs4.BeautifulSoup(self.response.content.decode('utf-8', 'ignore'),
                                     'html.parser')

            # Get data :
            self.cells = self.soup.findAll('td')
            self.desc = (self.soup.findAll('meta'))[-3]

            self.stars = self.soup.find('p', {'class': "star-rating"})
            self.stars = str(self.stars).split('\n')[0]

            for key in self.dict_stars:
                if key in self.stars:
                    review_rating = self.dict_stars[key]

            for text in self.soup.findAll("ul", {"class": "breadcrumb"}):
                for link in text.findAll('a'):
                    self.category.append(link.getText())
            # List of 3 titles, the right one is the third.
            # Use print(category) to see the list.
            # print(category)
            self.category = self.category[-1]

            self.picture = self.soup.find('img')
            self.picture = str(self.picture).split('src="../..')[1][:-3]
            self.picture = f'http://books.toscrape.com{self.picture}'

            # Write Datas :
            self.product_page_url = self.url

            self.universal_product_code = self.cells[0].text

            self.title = (str(self.soup.title))
            self.title = self.title.split("\n")[1]
            self.title = self.title.replace(" | Books to Scrape - Sandbox", "")
            self.title = self.title.replace('    ', '')

            # cellules[2] & [3] give the raw data.
            # by using .text[1:] you get the devise and the amount.
            self.price_including_tax = self.cells[2].text[1:]

            self.price_excluding_tax = self.cells[3].text[1:]

            self.number_available = str(self.cells[5])
            self.number_available = self.number_available.split("(")[1]
            self.number_available = self.number_available.replace(" available)</td>", "")

            self.product_description = str(self.desc).split('\n')[1]

            self.category = self.category

            self.review_rating = self.review_rating

            self.image_url = self.picture

            self.database = (list(map(str, (self.product_page_url,
                                            self.universal_product_code, self.title,
                                            self.price_including_tax,
                                            self.price_excluding_tax,
                                            self.number_available,
                                            self.product_description, self.category,
                                            self.review_rating, self.image_url
                                            )
                                      )))

            #downloadpic(image_url, universal_product_code, category)

            return self.database

        else:
            # The server is not responding :
            print("Connection issues : Verify your connection. Check in 10 sec.")
            time.time(10)
            # Retry
            self.scrap_book()

    def get_database(self):
        return self.database


def scrap():
    books_lib = AllLinks()
    dict_books = {}
    for k in range(len(books_lib.get_links())):
        dict_books[str(k)] = Book(books_lib.get_links()[k]).get_database()
    return dict_books


def main():
    """

    """
    books = scrap()

    # Exemple:
    book555 = books["555"]
    print(book555)

    return books


if __name__ == '__main__':
    main()
