import scrapy
import json
import scrapy_splash
import requests
from scrapy.selector import Selector
import numpy

class CommentSpider (scrapy.Spider):
    name = 'comments'

    url_start = 'https://www.thegioididong.com/dtdd/iphone-6-32gb-gold'
    url_api_list_comment = 'https://www.thegioididong.com/commentnew/cmt/index'

    start_replaced_str = """$("#comment").trigger("cmt.listpaging");$('.listcomment').html('"""
    end_replaced_str = """');"""

    objectid = 0

    def start_requests(self):

        yield scrapy.Request(
            url=self.url_start,
            callback=self.parse,
        )

    def parse(self, response):
        # path_page_activate = 'div.pagcomment span.active'
        # path_next_page_numb = 'div.pagcomment span.active + a::text'

        path_list_QA = 'li.comment_ask'
        path_comment_id = 'li.comment_ask::attr(id)'

        path_object_id = 'div.wrap_comment::attr(detailid)'


        if response.css(path_object_id).extract_first() is not None:
            self.objectid = response.css(path_object_id).extract_first()

        try:
            str_numb_page = response.css('ul.listcomment div.pagcomment a')[-2].css('a::text').extract_first()
        except(e,):
            str_numb_page = 1

        for page_numb in range(1, int(str_numb_page) + 1):
            formdata = {
                'core[call]': 'cmt.listpaging',
                'objectid': self.objectid,
                'objecttype': '2',
                'pageindex': str(page_numb),
                'order': '1',
            }
            res_script = requests.post(self.url_api_list_comment, data=formdata).text
            struct_text = res_script.replace(self.start_replaced_str, '').replace(self.end_replaced_str, '')
            selector = Selector(text=struct_text)

            for qa in selector.css(path_list_QA):
                if len(qa.css('div.listreply div.reply')):
                    yield {
                        'id_cmt': qa.css(path_comment_id).extract_first(),
                        'question': qa.css('div.question::text').extract_first(),
                        'answer': ''.join(qa.css('div.listreply div.reply')[0].css('div.cont::text').extract()),
                    }
                else:
                    continue


