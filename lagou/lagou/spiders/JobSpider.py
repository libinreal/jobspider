# -*- coding: utf-8 -*-

import sys
import scrapy
import json

class JobSpider(scrapy.Spider):
    allowed_domains = ["lagou.com"]

    name = 'Job'

    '''paganation info'''
    pageCount = 0
    pageNo = 1

    #current request url 
    reqUrl = ''

    #current kd
    kd = ''

    header = {
        'Accept':'Accept:application/json, text/javascript, */*; q=0.01',
        'Accept-Language':'zh-CN,zh;q=0.9,en;q=0.8',
        'Accept-Encoding':'gzip, deflate, br',
        'Host':'www.lagou.com',
        'User-Agent':[
            'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.116 Safari/537.36 Edge/15.15063'
        ],
        'Referer':'https://www.lagou.com/jobs/list_PHP',
        'X-Requested-With':'XMLHttpRequest',
        'X-Anit-Forge-Token':'None',
        'X-Anit-Forge-Code':'0'
    }



    def start_requests(self):
        '''
        check job with multiple kd <key word> and multiple location
        '''
        

        #ajax query string spelled base on filterDict
        queryStr = ''

        #dict for spell query string
        filterDict = {
            'city':['上海'],#cannot use turple<元组>
            'jd':[],#融资阶段
            'px':'default',#排序方式
            'district':['徐汇区'],#行政区
            'bizArea':['漕宝路', '上海南站', '植物园', '上海师大', '田林', '龙华'],#商区
            'needAddtionalResult':'false',
            'isSchoolJob':0
        }

        #key word list for searching job
        kdList = ['PHP', 'Python', 'Go']

        for fk in filterDict:
            
            #current spelled string for value of fk in filterDict
            fks = ''

            #list type
            if type(filterDict[fk]) == list:
                #loop fki in filerDict[fk]:[fki … ]
                for fki in filterDict[fk]:
                    if type(fki) == str or type(fki) == unicode:
                        if fki.strip() == '':
                            continue
                        else:
                            fks = fks + '%s,' % fki
                if len(fks) > 0:
                    fks = fks[0:-1]

            #string type
            elif type(filterDict[fk]) == str or type(filterDict[fk]) == unicode:
                if fki.strip() == '':
                    continue
                fks = filterDict[fk]

            #other types e.g. int,boolean,object…
            else:
                fks = filterDict[fk]

            if type(fks) == str or type(fks) == unicode and len(fks) == 0:
                continue

            #spell query string such as: city=上海&…
            queryStr = queryStr + '%s=%s&' % (fk, fks)

        #constant request url
        urlWithQueryStr = 'https://www.lagou.com/jobs/positionAjax.json?%s' % queryStr[0:-1]
        self.reqUrl = urlWithQueryStr

        #dynamic form data
        for kd in kdList:
            self.kd = kd
            '''
            dc = {'url':self.reqUrl, 'formdata':{'pn':self.pageNo,'kd':self.kd,'first':False}, 'method':'POST', 'headers':self.header, 'callback':self.parse}
            print dc
            sys.exit()
            '''
            yield scrapy.http.FormRequest(url=self.reqUrl, formdata={'pn':str(self.pageNo),'kd':self.kd,'first':'false'}, method='POST', headers=self.header, callback=self.parse)

    def parse(self, response):
        fp = open('1.html','a+')
        fp.write(response.body)
        fp.close()
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
        print jsonData,jsonItems,' parse '
        self.pageCount = jsonResult['totalCount'] / jsonContent['pageSize'] + 1

        for e in jsonItems:
            print e['companyId'] #公司id
            print e['positionId'] #职位id
            print e['subwayline'] #地铁线
            print e['createTime']
            print e['district']
            print e['education']
            print e['industryField']

        if self.pageNo <= self.pageCount:
            yield scrapy.http.FormRequest(url=self.reqUrl, formdata={'pn':str(self.pageNo),'kd':self.kd,'first':'false'}, method='POST', headers=self.header, callback=self.parse)