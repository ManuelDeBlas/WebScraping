from pickle import TRUE
from scrape_each_book import BookScraper
from scraper import FastBookScraper
import argparse


def main(output_file, fast):
    """
    Scrape todostuslibros website
    """
    if (fast == "TRUE"):
        scraper = FastBookScraper()
    else:
        scraper = BookScraper()

    scraper.scrape()
    scraper.data2csv(output_file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Escoja el metodo de \
        ejecución o el path al fichero de salida.')
    parser.add_argument('-f', '--fast', type=str, default="FALSE",
                        help="TRUE - Utiliza una version rapida que obtiene \
                            solo los datos más importantes. \
                            FALSE - Utiliza una version más lenta que obtiene \
                            todos los datos.\
                            Por defecto es TRUE")
    parser.add_argument('-o', '--output_filepath', type=str,
                        default="output/Fast_Bestsellers.csv",
                        help='FilePath al fichero de salida. Por defecto es \
                            output/Fast_Bestsellers.csv')
    args = parser.parse_args()

    output_file = args.output_filepath
    fast = args.fast

    main(output_file, fast)
