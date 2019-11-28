import scrapy
import json
# import scrapy_splash
import requests
from scrapy.selector import Selector
import numpy

class CommentSpider2 (scrapy.Spider):
    name = 'qa'

    url_api_list_question = 'https://www.thegioididong.com/hoi-dap/aj/Subject/LoadMoreQuestion?titleurl=wiki-thuat-ngu&Suburl=&iPageIndex='

    def start_requests(self):
        for page_numb in range(0, 900):
            print('page: ', page_numb)
            req_url = self.url_api_list_question
            yield scrapy.Request(
                url = req_url + str(page_numb),
                callback=self.parse,
            )

    def parse(self, response):
        # print('response: ', response)
        for a_tag in response.css('a'):
            yield {
                'url_answer': a_tag.css('::attr(href)').extract_first(),
                'short_question': a_tag.css('p::text').extract_first(),
                'question': a_tag.css('p::text').extract_first(),
            }
