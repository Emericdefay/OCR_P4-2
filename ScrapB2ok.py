# Libraries:
import sys
import os
import csv

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
        self.url_page = "http://books.toscrape.com/catalogue/category/books_1/index.html"
        self.webmaster = "http://books.toscrape.com/catalogue/"
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

        self.get_all_books_links()
        pass

    def get_pages_links(self):
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

    def get_books_links_per_page(self):

        self.html_page = requests.get(self.url_page)
        self.soup_books = bs4.BeautifulSoup(self.html_page.text, 'html.parser')

        self.links = []
        self.articles = self.soup_books.findAll('article', {'class': "product_pod"})

        for self.article in self.articles:
            self.link = str(self.article.find('h3').a)
            self.link = self.link.split(" title")[0][18:-1]
            self.link = self.link.replace('catalogue/', '')

            self.fullLink = f'{self.webmaster + self.link}'

            self.links.append(self.fullLink)

        return self.links

    def get_all_books_links(self):
        """

        """

        self.all_pages = self.get_pages_links()

        self.url_page = self.url_page.replace('index.html', '')

        self.all_books_links = []

        for i in range(len(self.all_pages)):
            self.link_book = f'{self.url_page + self.all_pages[i]}'
            self.all_books_links.append(self.link_book)

        return self.all_books_links

    def get_links(self):
        print(self.all_books_links)


def main():
    """

    """
    pass


if __name__ == '__main__':
    a = AllLinks()
    print(a.get_links())
