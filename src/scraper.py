import requests
from bs4 import BeautifulSoup
import time
import csv
import re
import string
import pandas as pd


class FastBookScraper():
    """
    A class that scrapes the website todostuslibros.com/mas_vendidos faster \
        but with less information than BookScraper.

    Attributes:
        This class does not have public attributes

    Methods:
        scrape(): Scrapes the website
        data2csv(output_file): Creates and stores collected data into a csv \
                            in the given file path.
        download_covers(input_file, output_folder): Downloads and stores book \
                                                    covers.
    """
    _url = "https://www.todostuslibros.com/mas_vendidos"
    _id = 0
    _dt = []
    _headers = {
            "Accept": "text/html,application/xhtml+xml,\
                application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Encoding": "gzip, deflate, sdch, br",
            "Accept-Language": "en-US,en;q=0.8",
            "Cache-Control": "no-cache",
            "dnt": "1",
            "Pragma": "no-cache",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) \
                AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 \
                Safari/537.36"
            }

    def __init__(self):
        pass

    @classmethod
    def _generate_unique_id(cls, value):
        """
        Sums value to class variable _id.

        Parameters:
            value (int): The value of the last id
        """
        cls._id += value

    def _get_html(self, url):
        """
        Gets an html from a url given.

        Parameters:
            url (string): The url of the website the html is extracted

        Returns:
            The html from the url given
        """
        return requests.get(url, headers=self._headers)

    def _get_pages_links(self, soup):
        """
        Gets pages links from an html given.

        Parameters:
            soup (object 'bs4.BeautifulSoup'): An html object of the \
                                               first group of books.

        Returns:
            pages_urls (list): A list of the different url from all the \
                               pages where are books.
        """
        pages_urls = []
        page_items = soup.findAll('a', attrs={'class': 'page-link'})
        # Deleting last item corresponding to the (next_page button)
        page_items.pop()

        # Obtaining last page
        last_p = page_items.pop()
        max_p = int(last_p.contents[0])

        # Obtaining link
        full_link = last_p.attrs['href']
        link = full_link.rstrip(string.digits)

        for i in range(1, max_p + 1):
            # Obtaining list of links for all the pages
            pages_urls.append(link + str(i))

        return pages_urls

    def _get_title(self, book):
        """
        Extracts the book title.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a \
                                               book in html

        Returns:
            title (string): The title of the book given
        """
        title = book.find(class_="title").contents[1].contents[0]
        return title.strip()

    def _get_subtitle(self, book):
        """
        Extracts the book subtitle.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a book \
                                               in html

        Returns:
            subtitle (string): The subtitle of the book given
        """
        # There might be no subtitles
        try:
            subtitle = book.find(class_="subtitle").contents[0].contents[0]

        except IndexError:
            subtitle = ""

        return subtitle.strip()

    def _get_author(self, book):
        """
        Extracts the book author.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a \
                                               book in html

        Returns:
            author (string): The author of the book given
        """
        autor = book.find(class_="author").contents[0].contents[0]
        return autor.strip()

    def _get_editorial_and_ISBN(self, book):
        """
        Extracts the book editorial and ISBN.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a \
                                               book in html

        Returns:
            ed_isbn (list): The editorial and ISBN of the book
        """
        ed_isbn = book.find(class_="data").contents[0].split("/")
        # Deleting all unwanted whitespcaes
        return [s.strip() for s in ed_isbn]

    def _get_price(self, book):
        """
        Extracts the book price.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a \
                                               book in html

        Returns:
            price (list): The price of the book given
        """
        price = book.find(class_="book-price").contents[1].contents[0]
        # Digits are extracted from the string
        return re.findall(r'\d+\.\d+|\d+', price)[0]

    def _get_price_no_taxes(self, book):
        """
        Extracts the book price without taxes.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a \
                                               book in html

        Returns:
            untaxed price (list): The price without taxes of the book given
        """
        untaxed = book.find(class_="book-price").contents[2]
        # Digits are extracted from the string
        return re.findall(r'\d+\.\d+|\d+', untaxed)[0]

    def _get_book_image(self, book):
        """
        Extracts the book cover.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a \
                                               book in html

        Returns:
            cover (string): The url of the cover's picture
        """
        # TODO: Representa que con extraer el link es suficiente?
        img = book.find(class_="book-image col-3 col-sm-3 col-md-2")
        return img.a.img['src']

    def _get_books(self, soup):
        """
        Extracts the information from all books and appends them to the object.

        Parameters:
            soup (object 'bs4.BeautifulSoup'): An html of a page of different \
                                               books given
        """
        book_info = dict()
        books = soup.find_all(class_="book row")

        for book in books:
            self._generate_unique_id(1)
            book_info = {"id": self._id,
                         "title": self._get_title(book),
                         "subtitle": self._get_subtitle(book),
                         "author": self._get_author(book),
                         "editorial": self._get_editorial_and_ISBN(book)[0],
                         "ISBN": self._get_editorial_and_ISBN(book)[1],
                         "price (€)": self._get_price(book),
                         "untaxed price (€)": self._get_price_no_taxes(book),
                         "book cover": self._get_book_image(book)
                         }

            self._dt.append(book_info)

    def scrape(self):
        """
        Scrapes the website.
        """
        print("Web Scraping of books data from {} ".format(self._url) +
              "This process could take about 2 minutes.\n")

        # Start timer
        start_time = time.time()

        # Get main page
        html_page = self._get_html(self._url)
        soup = BeautifulSoup(html_page.content, features="html.parser")

        # Loop through all pages and get their relevant content
        for page in self._get_pages_links(soup):

            html_page = self._get_html(page)
            soup = BeautifulSoup(html_page.content, features="html.parser")
            self._get_books(soup)

    def data2csv(self, output_file):
        """
        Turns the data into a csv file to the path given.

        Parameters:
            output_file (string): File path for the output.
        """
        with open(output_file, 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self._dt[0].keys())
            writer.writeheader()
            writer.writerows(self._dt)

    def download_covers(self, input_filepath, output_folder):
        """
        Downloads and stores book covers images giving them their book \
        id as filename.

        Parameters:
            input_filepath (string): Filepath to scraped csv.
            output_folder (string): Path to the folder where \
                                    images will be stored.
        """
        df = pd.read_csv(input_filepath, usecols=['id', 'book cover'])
        for i in df.index:
            html = self._get_html(df["book cover"][i])
            if html.status_code == 200:
                output = open(output_folder + '/' + str(df["id"][i]) +
                              '.gif', "wb")

                for chunk in html:
                    output.write(chunk)

                output.close()
