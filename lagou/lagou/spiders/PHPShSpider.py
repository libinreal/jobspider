# -*- coding: utf-8 -*-

import scrapy

class PHPShSpider(scrapy.Spider):
    name = "PHPSh"
    allowed_domains = ["lagou.com"]
    start_urls = [
        "https://www.lagou.com/zhaopin/"
    ]#使用 start_urls 的url生成Request
    

    def parse(self, response):
        '''
        override处理下载的response的默认方法
        '''
        self.logger.info('Parse function called on %s', response.url)

        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)