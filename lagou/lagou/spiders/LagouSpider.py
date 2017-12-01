# -*- coding: utf-8 -*-

import scrapy

class LagouSpider(scrapy.Spider):
    allowed_domains = ["lagou.com"]

    GET_DATA = {
        city:'',#城市
        district:'',#商区
        gj:'',#工作经验 ','分割
        xl:'',#学历要求 ','分割
        jd:'',#融资阶段 ','分割
        hy:'',#行业领域 ','分割
        yx:'',#月薪 
        gx:''#工作性质
    }

    start_urls = [
        "https://www.lagou.com/jobs/positionAjax.json"
    ]#使用 start_urls 的url生成Request
    
    def start_requests():
        yield Request(self.start_urls)

    def parse(self, response):
        '''
        override处理下载的response的默认方法
        '''
        self.logger.info('Parse function called on %s', response.url)

        filename = response.url.split("/")[-2] + '.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

