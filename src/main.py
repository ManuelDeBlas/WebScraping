from scraper import BookScraper

output_file = "output/test.csv"

scraper = BookScraper()
scraper.scrape()
scraper.data2csv(output_file)
