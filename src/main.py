from scrape_each_book import BookScraper
import argparse


def main(output_file, keyword):
    """
    Scrape todostuslibros website
    """
    if(keyword != ""):
        scraper = BookScraper(
            "https://www.todostuslibros.com/busquedas?keyword=" +
            keyword)
    else:
        scraper = BookScraper()
    scraper.scrape()
    scraper.data2csv(output_file)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Seleccione una busqueda \
        a realizar.')
    parser.add_argument('-k', '--keyword', type=str, default="",
                        help='Palabra clabe que se quiere \
                            usar para la busqueda')
    parser.add_argument('-o', '--output_filepath', type=str,
                        default="output/test.csv",
                        help='FilePath al fichero de salida')
    args = parser.parse_args()

    output_file = args.output_filepath
    keyword = args.keyword

    if(" " in keyword):
        keyword = keyword.replace(" ", "+")

    main(output_file, keyword)
