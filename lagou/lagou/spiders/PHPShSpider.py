# -*- coding: utf-8 -*-

import scrapy

class PHPShSpider(LagouSpider):
    name = "PHPSh"

    start_urls = [
        "https://www.lagou.com/zhaopin/",
    ]#使用 start_urls 的url生成Request
    
    def start_requests(self):
        return super().start_requests()

    def parse(self, response):
        

