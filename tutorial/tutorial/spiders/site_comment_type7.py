import scrapy
import json
# import scrapy_splash
import requests
from scrapy.selector import Selector
import numpy
from scrapy.crawler import CrawlerProcess
import jsonlines
import glob

def extract_urls(site_path):
    url_products = []
    with jsonlines.open(site_path) as lines:
        for line in lines:
            url_products.append(line['url'])
    return url_products

class SiteCommentProductSpider (scrapy.Spider):
    name = 'site-comments-type7'

    urls = ['https://www.thegioididong.com/tien-ich/thanh-toan-tra-gop?']

    url_api_list_comment = 'https://www.thegioididong.com/commentnew/cmt/index'

    start_replaced_str = """$("#comment").trigger("cmt.listpaging");$('.listcomment').html('"""
    end_replaced_str = """');"""

    objectid = 0

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
        # path_page_activate = 'div.pagcomment span.active'
        # path_next_page_numb = 'div.pagcomment span.active + a::text'

        path_list_QA = 'li.comment_ask'
        path_comment_id = 'li.comment_ask::attr(id)'

        path_object_id = 'div.wrap_comment::attr(detailid)'

        if response.css(path_object_id).extract_first() is not None:
            self.objectid = response.css(path_object_id).extract_first()

        str_numb_page = 0
        try:
            str_numb_page = response.css('ul.listcomment div.pagcomment span')[-2].css('::text').extract_first()
        except():
            str_numb_page = 1

        for page_numb in range(1, int(str_numb_page) + 1):
            try:
                formdata = {
                    'core[call]': 'cmt.listpaging',
                    'objectid': self.objectid,
                    'objecttype': '7',
                    'pageindex': str(page_numb),
                    'order': '1',
                }
                print("formdata: ")
                print(formdata)
                res_script = requests.post(self.url_api_list_comment, data=formdata).text
                struct_text = res_script.replace(self.start_replaced_str, '').replace(self.end_replaced_str, '')
                selector = Selector(text=struct_text)

                for qa in selector.css(path_list_QA):
                    if len(qa.css('div.listreply div.reply')) >= 1:
                        yield {
                            'id_cmt': qa.css(path_comment_id).extract_first(),
                            'question': qa.css('div.question::text').extract_first(),
                            # 'answer': ''.join(qa.css('div.listreply div.reply')[0].css('div.cont::text').extract()),
                            'answers': [''.join(reply.css('div.cont::text').extract()) for reply in qa.css('div.listreply div.reply')],
                            # 'time': qa.css('li.comment_ask a.time::text').extract_first(),
                            # 'user_name': qa.css('li.comment_ask div.rowuser a strong::text').extract_first(),
                            # 'replier_name': qa.css('li.comment_ask div.rowuser a strong::text').extract_first(),
                        }
                    else:
                        continue
            except Exception as e:
                print(e)
