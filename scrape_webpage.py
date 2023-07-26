# Import necessary modules
import scrapy
from scrapy.crawler import CrawlerProcess
import re

# Define the Spider to scrape quotes from a webpage and save them to a CSV file
class QuotesToCsv(scrapy.Spider):
    # Set the name of the Spider
    name = "MJKQuotesToCsv"

    # Define the URLs to start scraping from
    start_urls = [
        'https://en.wikiquote.org/wiki/Maynard_James_Keenan',
    ]

    # Customize settings for the Spider, including pipelines and CSV output
    custom_settings = {
        'ITEM_PIPELINES': {
            '__main__.ExtractFirstLine': 1  # Use ExtractFirstLine pipeline to process items
        },
        'FEEDS': {
            'Output/Quotes.csv': {
                'format': 'csv',  # Save the scraped data in CSV format
                'overwrite': True  # Overwrite the file if it already exists
            }
        }
    }

    # Define how to parse the data from the URLs
    def parse(self, response):
        # Extract quotes from the webpage using CSS selectors
        for quote in response.css('div.mw-parser-output > ul > li'):
            yield {'quote': quote.extract()}  # Yield the extracted quote


# Pipeline to extract the first line from the scraped quote and remove HTML tags
class ExtractFirstLine(object):
    # Process each item (quote) returned by the Spider
    def process_item(self, item, spider):
        # Split the quote into lines
        lines = dict(item)["quote"].splitlines()
        # Extract the first line and remove HTML tags using regex
        first_line = self.__remove_html_tags__(lines[0])
        # Return the quote with only the first line
        return {'quote': first_line}

    # Function to remove HTML tags from the given text using regex
    def __remove_html_tags__(self, text):
        html_tags = re.compile('<.*?>')
        return re.sub(html_tags, '', text)


# Create a CrawlerProcess to run the Spider
process = CrawlerProcess()
# Start the Spider (MJKQuotesToCsv) to scrape quotes
process.crawl(QuotesToCsv)
# Run the Spider
process.start()
