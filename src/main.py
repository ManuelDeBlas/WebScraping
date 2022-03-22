from src.scraper import BookScraper

output_file = "casadellibro.csv"

scraper = BookScraper()
scraper.scrape()
scraper.data2csv(output_file)