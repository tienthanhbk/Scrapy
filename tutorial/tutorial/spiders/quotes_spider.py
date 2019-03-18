import scrapy
import json

class QuotesSpider (scrapy.Spider):
    name = 'quotes'

    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        path_quote = 'div.quote'
        path_text_from_quote = 'span.text::text'
        path_author_from_quote = '.author::text'
        path_tag_from_quote = '.tags .tag::text'
        path_next_page = 'nav ul.pager li.next a'

        for quote in response.css(path_quote):
            text = quote.css(path_text_from_quote).extract_first()
            author = quote.css(path_author_from_quote).extract_first()
            tag = quote.css(path_tag_from_quote).extract()
            yield {
                'text': text,
                'author': author,
                'tag': tag,
            }

        next_page = response.css(path_next_page)
        if next_page is not None:
            for a in next_page:
                yield response.follow(url=a, callback=self.parse)
