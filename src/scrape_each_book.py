import requests
from bs4 import BeautifulSoup
import time
import csv
import re
import string
import pandas as pd


class BookScraper():
    """
    A class that scrapes the website todostuslibros.com/mas_vendidos.

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

    def _get_book_url(self, book_row):
        """
        Gets book url

        Parameters:
            book_row (object 'bs4.element.Tag'): The information of a book.

        Returns:
            book_url (string): The book's url from the object given.
        """
        book_url = book_row.find(class_="title").a['href']

        return book_url

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
        try:
            title = book.find(class_="title").contents[0].strip()
        except IndexError:
            title = ""
        except AttributeError:
            title = ""

        return title

    def _get_subtitle(self, book):
        """
        Extracts the book subtitle.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a book \
                                               in html

        Returns:
            subtitle (string): The subtitle of the book given
        """
        try:
            subtitle = book.find(class_="subtitle").contents[0]
        except IndexError:
            subtitle = ""
        except AttributeError:
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
        try:
            author = book.find(class_="author").contents[0].contents[0].strip()
        except IndexError:
            author = ""
        except AttributeError:
            author = ""

        return author

    def _get_matter(self, book):
        """
        Extracts the book matter.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a \
                                               book in html

        Returns:
            matter (string): The matter of the book given
        """
        try:
            matter = book.find(
                class_="col-12 col-sm-12").contents[1].contents[1] \
                    .contents[1].contents[3].contents[1].contents[0].strip()
        except IndexError:
            matter = ""
        except AttributeError:
            matter = ""

        return matter

    def _get_editorial(self, book):
        """
        Extracts the book editorial.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a \
                                               book in html

        Returns:
            editorial (string): The editorial of the book given
        """
        try:
            editorial = book.find(class_="col-12 col-sm-12").contents[3] \
                .contents[1].contents[1].contents[2].contents[0].contents[0] \
                .strip()
        except IndexError:
            editorial = ""
        except AttributeError:
            editorial = ""

        return editorial

    def _get_collection(self, book):
        """
        Extracts the book collection.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a \
                                               book in html

        Returns:
            collection (string): The collection of the book given
        """
        try:
            collection = book.find(class_="col-12 col-sm-12").contents[3] \
                .contents[1].contents[1].contents[6].contents[0].strip()
        except IndexError:
            collection = ""
        except AttributeError:
            collection = ""

        return collection

    def _get_binding(self, book):
        """
        Extracts the book binding.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of \
                                               a book in html

        Returns:
            binding (string): The binding of the book given
        """
        try:
            binding = book.find(class_="col-12 col-sm-12").contents[3] \
                .contents[1].contents[1].contents[9].contents[0].strip()
        except IndexError:
            binding = ""
        except AttributeError:
            binding = ""

        return binding

    def _get_book_feature(self, book, c1, c2):
        """
        Extracts a book feature for 2 parameters given. The parameters depend \
        on the feature to look for.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a book \
                                               in html
            c1 (integer): A number to look for inside the html
            c2 (integer): Another number to look for inside an html

        Returns:
            feature (string): The feature of the book given
        """
        try:
            feature = book.find(class_="col-12 col-sm-12").contents[3] \
                .contents[c1].contents[1].contents[c2].contents[0].strip()
        except IndexError:
            feature = ""
        except AttributeError:
            feature = ""

        return feature

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
        return re.findall(r'\d+\,\d+|\d+', price)[0]

    def _get_price_no_taxes(self, book):
        """
        Extracts the book price without taxes.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a \
                                               book in html

        Returns:
            untaxed price (list): The price without taxes of the book given
        """
        try:
            untaxed = book.find(class_="book-price-alternative").contents[0]
            # Digits are extracted from the string
            untaxed = re.findall(r'\d+\,\d+|\d+', untaxed)[0]
        except AttributeError:
            untaxed = ['']

        return untaxed

    def _get_book_cover(self, book):
        """
        Extracts the book cover.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a \
                                               book in html

        Returns:
            cover (string): The url of the cover's picture
        """
        try:
            cover = book.find(class_="portada").attrs['src']
        except AttributeError:
            cover = ""

        return cover

    def _get_book_info(self, book):
        """
        Extracts the book information.

        Parameters:
            book (object 'bs4.BeautifulSoup'): The information of a \
                                               book in html

        Returns:
            book_dict (dict): The book parameters
        """
        return {"id": self._id,
                "title": self._get_title(book),
                "subtitle": self._get_subtitle(book),
                "author": self._get_author(book),
                "matter": self._get_matter(book),
                "editorial": self._get_editorial(book),
                "collection": self._get_collection(book),
                "binding": self._get_binding(book),
                "country": self._get_book_feature(book, 1, 12),
                "lenguage of publication": self._get_book_feature(book, 1, 15),
                "original lenguage": self._get_book_feature(book, 1, 18),
                "ISBN": self._get_book_feature(book, 3, 2),
                "EAN": self._get_book_feature(book, 3, 6),
                "dimension": self._get_book_feature(book, 3, 9),
                "weight": self._get_book_feature(book, 3, 13),
                "number of pages": self._get_book_feature(book, 3, 17),
                "publication date": self._get_book_feature(book, 3, 20),
                "price (€)": self._get_price(book),
                "untaxed price (€)": self._get_price_no_taxes(book),
                "book cover": self._get_book_cover(book)
                }

    def _get_books(self, soup, delay):
        """
        Extracts the information from all books and appends them to the object.

        Parameters:
            soup (object 'bs4.BeautifulSoup'): An html of a page of different \
                                               books given
            delay (float): The time it gets to request an html
        """
        book_info = dict()
        books = soup.find_all(class_="book row")

        for book in books:
            # Get book url
            book_url = self._get_book_url(book)
            html_page = self._get_html(book_url)
            soup = BeautifulSoup(html_page.content, features="html.parser")

            # Increase unique id by modifiying private variable _id
            self._generate_unique_id(1)

            book_info = self._get_book_info(soup)

            self._dt.append(book_info)
            # Force delay between html requests:
            time.sleep(5 * delay)

    def scrape(self):
        """
        Scrapes the website.
        """
        print("Web Scraping of books data from {} ".format(self._url) +
              "This process could take about 20 minutes.\n")

        # Start timer
        start_time = time.time()

        # Get main page
        html_page = self._get_html(self._url)

        # Obtain the response delay of a html request
        response_delay = time.time() - start_time

        soup = BeautifulSoup(html_page.content, features="html.parser")

        # Loop through all pages and get their relevant content
        for page in self._get_pages_links(soup):
            html_page = self._get_html(page)
            soup = BeautifulSoup(html_page.content, features="html.parser")
            self._get_books(soup, response_delay)

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
