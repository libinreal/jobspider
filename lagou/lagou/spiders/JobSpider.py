# -*- coding: utf-8 -*-

import scrapy

class JobSpider(scrapy.Spider):
    allowed_domains = ["lagou.com"]

    name = 'Job'

    GET_DATA = {
        'city':'',#城市
        'district':'',#商区
        'gj':'',#工作经验 ','分割
        'xl':'',#学历要求 ','分割
        'jd':'',#融资阶段 ','分割
        'hy':'',#行业领域 ','分割
        'yx':'',#月薪 
        'gx':''#工作性质
    }

    pageCount = 0
    pageNo = 1

    start_urls = [
        "https://www.lagou.com/jobs/positionAjax.json"
    ]#使用 start_urls 的url生成Request
    
    def start_requests():
        for url in start_urls:
            yield Request(url=url, method='POST', body={'pn':str(self.pageNo),'first':False,'kd':'PHP'},callback=self.parse)

    def parse(self, response):
        '''
        override处理下载的response的默认方法

        json body:
        {
            content:{
                        pageNo:1
                        pageSize:15
                        positionResult:{
                                            result:{
                                                        companyId:47993
                                                        positionId:3287191
                                                    }
                                            resultSize:15
                                            totalCount:19
                                        }
                    }

        }
        '''
        


        jsonData = json.loads(response.body)
        jsonContent = jsonData['content']
        jsonResult = jsonContent['positionResult']
        jsonItems = jsonResult['result']

        self.pageCount = jsonResult['totalCount'] / jsonContent['pageSize'] + 1

        for e in jsonItems:
            print e['companyId'] #公司id
            print e['positionId'] #职位id
            print e['subwayline'] #地铁线
            print e['createTime']
            print e['district']
            print e['education']
            print e['industryField']

