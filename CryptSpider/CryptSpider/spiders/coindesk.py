import scrapy
import requests

from bs4 import BeautifulSoup
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class CoindeskSpider(CrawlSpider):
    name = "coindesk"
    allowed_domains = ["coindesk.com"]
    start_urls = ["https://coindesk.com"]
    rules = (
        Rule(LinkExtractor(allow=(r'/markets/2024/01/03/')), callback = 'parse'),
    )

    def parse(self, response):
        data_scrapy = response.css('p::text').getall()
        soup = BeautifulSoup(response.text, 'html.parser')
        data_from_beautifulsoup = soup.find('p').text

        combined_data = {
            'data_scrapy': data_scrapy,
            'data_from_beautifulsoup': data_from_beautifulsoup,
            }

        yield combined_data
