import scrapy
import json
# import scrapy_splash
import requests
from scrapy.selector import Selector
import numpy
from scrapy.crawler import CrawlerProcess

class CommentSpider (scrapy.Spider):
    name = 'comments'

    # url_start = 'https://www.thegioididong.com/dtdd/iphone-6-32gb-gold'
    # url_start = 'https://www.thegioididong.com/tai-nghe/tai-nghe-ep-kanen-ip-225'
    urls = ['https://www.thegioididong.com/tai-nghe/tai-nghe-ep-kanen-ip-225']
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
            str_numb_page = response.css('ul.listcomment div.pagcomment a')[-2].css('a::text').extract_first()
        except():
            str_numb_page = 1

        for page_numb in range(1, int(str_numb_page) + 1):
            try:
                formdata = {
                    'core[call]': 'cmt.listpaging',
                    'objectid': self.objectid,
                    'objecttype': '2',
                    'pageindex': str(page_numb),
                    'order': '1',
                }
                print(formdata)
                res_script = requests.post(self.url_api_list_comment, data=formdata).text
                struct_text = res_script.replace(self.start_replaced_str, '').replace(self.end_replaced_str, '')
                selector = Selector(text=struct_text)

                for qa in selector.css(path_list_QA):
                    if len(qa.css('div.listreply div.reply')) >= 1:
                        yield {
                            'id_cmt': qa.css(path_comment_id).extract_first(),
                            'question': qa.css('div.question::text').extract_first(),
                            'answers': [''.join(reply.css('div.cont::text').extract()) for reply in qa.css('div.listreply div.reply')],
                            # 'time': qa.css('li.comment_ask a.time::text').extract_first(),
                            # 'user_name': qa.css('li.comment_ask div.rowuser a strong::text').extract_first(),
                            # 'replier_name': qa.css('li.comment_ask div.rowuser a strong::text').extract_first(),
                        }
                    else:
                        continue
            except Exception as e:
                print(e)

#
# process = CrawlerProcess(settings={
#     'FEED_FORMAT': 'jl',
#     'FEED_URI': 'items.jl',
#     'FEED_EXPORT_ENCODING': 'utf-8'
# })
#
# process.crawl(CommentSpider)
# process.start()