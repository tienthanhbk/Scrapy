import scrapy
import json
# import scrapy_splash
import requests
from scrapy.selector import Selector
import numpy
from scrapy.crawler import CrawlerProcess

class SiteSpider (scrapy.Spider):
    name = 'links'

    urls = ['file:///home/tienthanh/Projects/Persional/Scrapy/tutorial/source/tablet.html']

    def start_requests(self):
        for url in self.urls:
            yield scrapy.Request(
                url=url,
                callback=self.parse,
            )
        # yield scrapy.Request(
        #     url=self.url_start,
        #     callback=self.parse,
        # )

    def parse(self, response):
        for selector in response.css('ul.homeproduct li a::attr(href)'):
            yield {
                'url': selector.extract()
            }