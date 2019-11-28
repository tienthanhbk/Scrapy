import scrapy
import json
import requests
from scrapy.selector import Selector
import numpy
# import jsonlines
import re

path_url = '/Users/tienthanh/Projects/ML/ScrapyTutorial/tutorial/data/short/wiki-thuat-ngu.jl'
path_url_parsed = '/Users/tienthanh/Projects/ML/ScrapyTutorial/tutorial/wiki-thuat-ngu-full.jl'


def get_id_pool(path):
    id_pool = []
    with jsonlines.open(path) as reader:
        for line in reader:
            id = line['id']
            id_pool.append(id)
    return id_pool



class CommentSpider2 (scrapy.Spider):

    name = 'q_detail'

    url_base = 'https://www.thegioididong.com'
    count = 0

    def start_requests(self):
        id_pool = get_id_pool(path_url_parsed)

        reader = jsonlines.open(path_url)
        for line in reader:
            href_url = line['url_answer']
            id = re.findall(r'\d+', href_url)[-1]
            if id not in id_pool:
                id_pool.append(id)
                yield scrapy.Request(
                    url=self.url_base + href_url,
                    callback=self.parse,
                )

    def parse(self, response):
        # print('response: ', response)
        self.count += 1
        print('count: ', self.count)
        url = response.request.url
        id = re.findall(r'\d+', url)[-1]

        question_title = response.css('.breadcrumb+h1::text').extract_first()
        if question_title is None:
            question_title = response.css('article h1::text').extract_first()
        # print(question_title)
        if question_title is None:
            return

        join_p = ''.join(response.css('.divContent p::text').extract())
        question = join_p + response.css('.divContent::text').extract_first()
        question = question.strip()

        # print(question)

        if question_title[-3::] == '...' and len(question) > len(question_title):
            yield {
                'id': id,
                # 'url': response.request.url,
                # 'title': question_title,
                'question': question,
                # 'answer': ''.join(response.css('.infocom_ask::text').extract()),
            }
        else:
            yield {
                'id': id,
                # 'url': response.request.url,
                # 'title': question_title,
                'question': question_title,
                # 'answer': ''.join(response.css('.infocom_ask::text').extract()),
            }
