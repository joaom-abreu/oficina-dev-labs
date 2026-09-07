import scrapy
from scrapy.crawler import CrawlerProcess
import json

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    start_urls = ['http://quotes.toscrape.com/']

    quotes_list = []

    def parse(self, response):
        for quote in response.css('div.quote'):
            quote_data = {
                'text': quote.css('span.text::text').get().strip(),
                'author': quote.css('small.author::text').get(),
                'tags': quote.css('div.tags a.tag::text').getall(),
            }
            self.quotes_list.append(quote_data)

        next_page = response.css('li.next a::attr(href)').get()
        if next_page is not None:
            yield response.follow(next_page, self.parse)
        else:
            with open('quotes.json', 'w', encoding='utf-8') as f:
                json.dump(self.quotes_list, f, ensure_ascii=False, indent=4)

process = CrawlerProcess()
process.crawl(QuotesSpider)
process.start()