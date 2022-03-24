import requests
from bs4 import BeautifulSoup
import time

class BookScraper():

    def __init__(self):
        self.url = "https://www.todostuslibros.com/mas_vendidos"

    def __get_html(self, url):
        """
        Gets an html from a url given.
        """
        return requests.get(url)

    def __get_url_page(self, p):
        """
        Gets the url from a number given.
        """
        return "https://www.todostuslibros.com/mas_vendidos?page=" + str(p)

    def __get_books(self, soup):
        """
        Extracts the information about the books in a page.
        """
        return soup.find(class_="row bestsellers featured-books books")
    
    def scrape(self):
        """
        Scraps the web.
        """
        print ("Web Scraping of books data from " + self.url + " This process could take about x minutes.\n")

        # Start timer
        start_time = time.time()

        for p in range(1, 10):
            
            url_page = self.__get_url_page(p)
            html_page = self.__get_html(url_page)
            soup = BeautifulSoup(html_page.content)
            books = self.__get_books(soup)

    def data2csv(self, output_file):
        """
        Turns the data into a csv file to the path given.
        """
        return