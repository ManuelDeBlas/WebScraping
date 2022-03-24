import requests
from bs4 import BeautifulSoup
import time
import csv

class BookScraper():

    def __init__(self):
        self._id = 0
        self._dt = []

        self.url = "https://www.todostuslibros.com/mas_vendidos"
        
    
    def _get_number_of_pages(self, html):
        """
        Gets the number of web pages
        """
        # TODO. sin acabar
        number_of_pages = html.find(class_="pagination")
        


    def _get_html(self, url):
        """
        Gets an html from a url given.
        """
        return requests.get(url)


    def _get_url_page(self, p):
        """
        Gets the url from a number given.
        """
        return "https://www.todostuslibros.com/mas_vendidos?page=" + str(p)


    def _get_books(self, soup):
        """
        Extracts the information from all books.
        """
        book_info = dict()
        books = soup.find_all(class_="book row")

        for book in books:
            self._generate_unique_id()
            book_info = {"id": self._id,
                         "title": self._get_title(book),
                         "subtitle": self._get_subtitle(book),
                         "author": self._get_author(book),
                         "synopsis": self._get_synopsis(book),
                         "editorial": self._get_editorial(book),
                         "ISBN": self._get_ISBN(book),
                         "price": self._get_price(book),
                         "price without taxes": self._get_price_no_taxes(book)}

            self._dt.append(book_info)


    def _generate_unique_id(self):
        # TODO, ver como modificar el valor de la variable, no se esta actualizando.
        self._id + 1


    def _get_title(self, book):
        """
        Extracts the book title and gives it format.
        """
        title = book.find(class_="title").contents[1].contents[0]
        # TODO: '\n                        El castillo de Barbazul\n                        ' <- tratar el formato
        return title


    def _get_subtitle(self, book):
        """
        Extracts the book subtitle.
        """
        # There might be no subtitles
        try:
            subtitle = book.find(class_="subtitle").contents[0].contents[0]
        except:
            subtitle = ""
        # TODO: Inspenccionar si hace falta tratar el formato
        return subtitle

    
    def _get_author(self, book):
        """
        Extracts the book author.
        """
        return book.find(class_="author").contents[0].contents[0]
    
    
    def _get_synopsis(self, book):
        """
        Extracts the book synopsis.
        """
        # TODO: Hay 2 sinopsis diferentes. Ambas aparecen incompletas. Quizás haya que buscar en la página de cada libro
        return book.find(class_="synopsis d-none d-md-block d-lg-block d-xl-block").contents[0]
    
    
    def _get_editorial_and_ISBN(self, book):
        """
        Returns the editorial and the ISBN in a list.
        """
        return book.find(class_="data").contents[0].split("/")
    
    
    def _get_editorial(self,book):
        """
        Extracts the editorial.
        """
        return self._get_editorial_and_ISBN(book)[0]
    
    
    def _get_ISBN(self, book):
        """
        Extracts the ISBN.
        """
        return self._get_editorial_and_ISBN(book)[1].strip()
    
    
    def _get_price(self, book):
        """
        Extracts the book price.
        """
        # TODO: El formato sale con muchos espacios.
        return book.find(class_="book-price").contents[1].contents[0]
    
    
    def _get_price_no_taxes(self, book):
        """
        Extracts the book price without taxes.
        """
        # TODO: El formato sale con muchos espacios.
        return book.find(class_="book-price").contents[2]


    def scrape(self):
        """
        Scraps the web.
        """

        print ("Web Scraping of books data from " + self.url + " This process could take about x minutes.\n")

        # Start timer
        start_time = time.time()
        
        # Get number of pages
        # TODO. Sin acabar
        url_page = self._get_url_page(1)
        html_page = self._get_html(url_page)
        soup = BeautifulSoup(html_page.content, features="html.parser")
        number_of_pages = self._get_number_of_pages(soup)

        # Loop through all pages
        for page in range(1, 11):
            
            url_page = self._get_url_page(page)
            html_page = self._get_html(url_page)
            soup = BeautifulSoup(html_page.content, features="html.parser")
            self._get_books(soup)
        pass


    def data2csv(self, output_file):
        """
        Turns the data into a csv file to the path given.
        """
        with open(output_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames = self._dt[0].keys())
            writer.writeheader()
            writer.writerows(self._dt)