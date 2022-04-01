import requests
from bs4 import BeautifulSoup
import time
import csv
import re
import string


class BookScraper():
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

    def __init__(self, url="https://www.todostuslibros.com/mas_vendidos"):

        self.url = url

    @classmethod
    def _generate_unique_id(cls, value):
        """
        Sums value to class variable _id
        """
        cls._id += value

    def _get_html(self, url):
        """
        Gets an html from a url given.
        """
        return requests.get(url, headers=self._headers)

    def _get_book_url(self, book_row):
        """
        Gets book url
        """
        book_url = book_row.find(class_="title").a['href']
        print(book_url)

    def _get_pages_links(self, soup):
        """
        Gets pages links
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
        Extracts the book title and gives it format.
        """
        title = book.find(class_="title").contents[1].contents[0]
        return title.strip()

    def _get_subtitle(self, book):
        """
        Extracts the book subtitle.
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
        """
        autor = book.find(class_="author").contents[0].contents[0]
        return autor.strip()

    def _get_synopsis(self, book):
        """
        Extracts the book synopsis.
        """
        # TODO: Descartarlo? las sinopsis completas ocupan demasiado
        return book.find(
            class_="synopsis d-none d-md-block " +
            "d-lg-block d-xl-block").contents[0]

    def _get_editorial_and_ISBN(self, book):
        """
        Returns the editorial and the ISBN in a list.
        """
        ed_isbn = book.find(class_="data").contents[0].split("/")
        # Deleting all unwanted whitespcaes
        return [s.strip() for s in ed_isbn]

    def _get_price(self, book):
        """
        Extracts the book price.
        """
        price = book.find(class_="book-price").contents[1].contents[0]
        # Digits are extracted from the string
        return re.findall(r'\d+\.\d+|\d+', price)[0]

    def _get_price_no_taxes(self, book):
        """
        Extracts the book price without taxes.
        """
        untaxed = book.find(class_="book-price").contents[2]
        # Digits are extracted from the string
        return re.findall(r'\d+\.\d+|\d+', untaxed)[0]

    def _get_book_image(self, book):
        """
        Extract book image
        """
        # TODO: Representa que con extraer el link es suficiente?
        img = book.find(class_="book-image col-3 col-sm-3 col-md-2")
        return img.a.img['src']

    def _get_books(self, soup):
        """
        Extracts the information from all books.
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

            book_info = {"id": self._id}
            # TODO: Reescribir las funciones de abajo para que extraigan la información de la pagina del libro.
            """
            book_info = {"id": self._id,
                         "title": self._get_title(soup),
                         "subtitle": self._get_subtitle(soup),
                         "author": self._get_author(soup),
                         "synopsis": self._get_synopsis(soup),
                         "editorial": self._get_editorial_and_ISBN(soup)[0],
                         "ISBN": self._get_editorial_and_ISBN(soup)[1],
                         "price (€)": self._get_price(soup),
                         "untaxed price (€)": self._get_price_no_taxes(soup),
                         "book cover": self._get_book_image(soup)
                         }
            """
            self._dt.append(book_info)

    def scrape(self):
        """
        Scraps the web.
        """
        print("Web Scraping of books data from {} ".format(self.url) +
              "This process could take about x minutes.\n")

        # Start timer
        start_time = time.time()

        # Get main page
        html_page = self._get_html(self.url)
        soup = BeautifulSoup(html_page.content, features="html.parser")
        self._get_books(soup)
        """
        # Loop through all pages and get their relevant content
        for page in self._get_pages_links(soup):

            html_page = self._get_html(page)
            soup = BeautifulSoup(html_page.content, features="html.parser")
            self._get_books(soup)
        """

    def data2csv(self, output_file):
        """
        Turns the data into a csv file to the path given.
        """
        with open(output_file, 'w', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=self._dt[0].keys())
            writer.writeheader()
            writer.writerows(self._dt)
