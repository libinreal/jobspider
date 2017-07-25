# -*- coding: utf-8 -*-

import scrapy

class PHPShSpider(scrapy.Spider):
    name = "PHPSh"
    allowed_domains = ["lagou.com"]
    start_urls = [
        "https://www.lagou.com/zhaopin/"
    ]

    def parse(self, response):
        self.logger.info('Parse function called on %s', response.url)

        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)